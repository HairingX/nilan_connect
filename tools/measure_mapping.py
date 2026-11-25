"""Measure, read-only, how far a Nilan gateway's datapoint and setpoint numbering goes, and what
reading it costs.

    Configure the gateway as the live tests do:
        set NILAN_HOST=<gateway-ip>             (environment variables)
        set NILAN_EMAIL=you@example.com
    or put NILAN_HOST and NILAN_EMAIL in mysecrets.py (gitignored) in the directory you run from.

    Run, from a checkout with `pip install -e .`:
        python tools/measure_mapping.py

For each table it reads, through the client's own requests: every address from 0 to the highest
the unit's model reads or writes, as a mapping does; then above it one address at a time up to
511, stopping after 100 absent addresses in a row; then once more only the addresses that
answered. It prints which answered and what each read cost, and a summary to paste back. It
never writes, and it stops at once when the gateway answers busy or does not answer. The email
and the host are never printed.
"""
from __future__ import annotations

import asyncio
import os
import runpy
import sys
import time
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import cast

from modbus_event_connect._device import ReadResult
from modbus_event_connect.micro_nabto import DatapointRegister, MicroNabtoDevice, MicroNabtoModel, SetpointRegister
from nilan_connect import Client, Key, Point, PollRate, create_client, model_points

TOP = 512
"""The first address not read in any table."""
STOP_AFTER = 100
"""Absent addresses in a row above the known span after which a table is taken to end: the manuals
lay their registers out in groups of 100, and the gateway keeps each group's spacing, so a run of
100 absent addresses is longer than any gap inside one group."""
TABLES = {"datapoint": DatapointRegister, "setpoint": SetpointRegister}


class Stopped(Exception):
    """The gateway answered busy, or not at all."""


def setting(name: str) -> str | None:
    """`name` from the environment, else from mysecrets.py in the directory run from."""
    value = os.environ.get(name)
    if value:
        return value
    path = Path.cwd() / "mysecrets.py"
    if not path.exists():
        return None
    found = runpy.run_path(str(path)).get(name)
    return str(found) if found else None


def known_span(client: Client, table: str) -> range:
    """From 0 to the highest address the unit's model reads or writes in `table`, as a mapping
    reads it."""
    space = TABLES[table]
    addresses = [access.address + i for p in model_points(cast(MicroNabtoModel, client.model))
                 for access in (p.read, p.write) if isinstance(access, space) for i in range(p.registers)]
    return range(0, max(addresses) + 1)


def ranges(addresses: Iterable[int]) -> str:
    """`addresses` as runs: "20-32,45,47-53"."""
    runs: list[list[int]] = []
    for address in sorted(addresses):
        if runs and address == runs[-1][1] + 1:
            runs[-1][1] = address
        else:
            runs.append([address, address])
    return ",".join(f"{a}" if a == b else f"{a}-{b}" for a, b in runs) or "-"


class Meter:
    """Reads addresses as raw registers through the client's device, counting requests and time."""

    def __init__(self, client: Client) -> None:
        self._client = client
        # The device the client reads through: its batching, halving of refused requests and pacing.
        self._device = cast(MicroNabtoDevice, getattr(client, "_device"))

    def _exchanges(self) -> int:
        return cast(int, self._client.diagnostics()["exchanges"])

    async def read(self, table: str, addresses: Sequence[int]) -> tuple[set[int], set[int], int, float]:
        """The addresses that answered and those refused, the requests sent and the seconds taken.

        Raises:
            Stopped: the gateway answered busy, or not at all.
        """
        points = [Point(Key(f"{table}_{a}", int), read=TABLES[table](a), poll_rate=PollRate.STATIC)
                  for a in addresses]
        before, started = self._exchanges(), time.monotonic()
        answers: Mapping[str, ReadResult] = await self._device.read(points) if points else {}
        present: set[int] = set()
        absent: set[int] = set()
        for address, point in zip(addresses, points):
            outcome = answers[point.key].outcome.name
            if outcome == "OK":
                present.add(address)
            elif outcome == "MISSING":
                absent.add(address)
            else:
                raise Stopped(f"{table} {address}: {outcome.lower()}")
        return present, absent, self._exchanges() - before, time.monotonic() - started


async def measure(client: Client, meter: Meter, table: str, lines: list[str]) -> None:
    span = known_span(client, table)
    present, absent, requests, seconds = await meter.read(table, list(span))
    print(f"{table} known span {span.start}-{span.stop - 1}: {requests} requests, {seconds:.1f} s")
    above_requests, above_seconds, in_a_row, address = 0, 0.0, 0, span.stop
    while address < TOP and in_a_row < STOP_AFTER:
        found, _, sent, took = await meter.read(table, [address])
        above_requests, above_seconds = above_requests + sent, above_seconds + took
        if found:
            present.add(address)
            in_a_row = 0
        else:
            absent.add(address)
            in_a_row += 1
        address += 1
    print(f"{table} above, {span.stop}-{address - 1}, one at a time: {above_requests} requests, {above_seconds:.1f} s")
    _, _, again, again_seconds = await meter.read(table, sorted(present))
    print(f"{table} again, only the {len(present)} that answered: {again} requests, {again_seconds:.1f} s")
    print(f"{table} answered: {ranges(present)}")
    print(f"{table} refused: {ranges(absent)}")
    lines.append(f"{table}: span {span.start}-{span.stop - 1} {requests}req/{seconds:.1f}s; "
                 f"above to {address - 1} {above_requests}req/{above_seconds:.1f}s; "
                 f"again {again}req/{again_seconds:.1f}s; answered {ranges(present)}")


async def main() -> int:
    host, email = setting("NILAN_HOST"), setting("NILAN_EMAIL")
    if not host or not email:
        print("Set NILAN_HOST and NILAN_EMAIL, as environment variables or in mysecrets.py.")
        return 2
    client = create_client(email=email, host=host, read_only=True)
    await client.connect()
    lines = [f"model {client.model.name}; identity {dict(client.identity)}"]
    try:
        meter = Meter(client)
        for table in TABLES:
            await measure(client, meter, table, lines)
    except Stopped as stop:
        lines.append(f"stopped: {stop}")
        print(f"Stopped: {stop}")
    finally:
        diagnostics = client.diagnostics()
        lines.append(f"latency average {diagnostics.get('average_latency')} s, max {diagnostics.get('max_latency')} s")
        await client.disconnect()
    print("\n--- summary, to paste back ---")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
