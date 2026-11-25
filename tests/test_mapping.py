"""Mapping a controller: the gateway's own registers, found once and then read where they answered."""
import json
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest_asyncio

from nilan_connect import CTS400, Area, Level, RawAddress, RegisterChange, difference
from nilan_connect.testing import SimulatedMicroNabtoDevice, client_for

EMAIL = "user@example.invalid"
WRITE = 0x2B
CTS400_IDENTITY = {"device_number": 72280, "device_model": 1140, "slave_device_number": 72270, "slave_device_model": 1}
READ: dict[str, dict[str, int]] = json.loads(
    (Path(__file__).parent / "cts400_read_2026_09_27.json").read_text(encoding="utf-8"))
"""What a real CTS400's gateway answered on 2026-09-27; datapoints 79, 80, 82 and 89 are in no list."""


@pytest_asyncio.fixture  # pyright: ignore[reportUntypedFunctionDecorator, reportUnknownMemberType]
async def gateway() -> AsyncGenerator[SimulatedMicroNabtoDevice, None]:
    async with SimulatedMicroNabtoDevice(
            emails=frozenset({EMAIL}), identity=CTS400_IDENTITY,
            datapoint_registers={(0, int(a)): v for a, v in READ["datapoints"].items()},
            setpoint_registers={(0, int(a)): v for a, v in READ["setpoints"].items()}) as simulated:
        yield simulated


async def test_a_cts400_is_mapped_in_its_gateways_numbers_from_its_points_up_to_the_limit(
        gateway: SimulatedMicroNabtoDevice) -> None:
    client = client_for(gateway, email=EMAIL, timeout=0.2, retries=1, level=Level.TEST, read_only=True)
    await client.connect()
    assert client.model is CTS400
    assert client.mapping_areas(limit=300) == (Area("datapoint", 20, 91), Area("datapoint", 111, 189),
                                               Area("setpoint", 30, 51), Area("setpoint", 81, 219))
    gateway.commands.clear()
    found = await client.map_areas(limit=300)
    first = len(gateway.commands)
    gateway.commands.clear()
    gateway.setpoint_registers[(0, 82)] = 0
    again = await client.read_mapped(found)
    await client.disconnect()
    every = {RawAddress("datapoint", int(a)) for a in READ["datapoints"]} | {
        RawAddress("setpoint", int(a)) for a in READ["setpoints"]}
    assert set(found.values) == every
    assert first == 251
    assert len(gateway.commands) == 2
    assert difference(found, again) == (RegisterChange(RawAddress("setpoint", 82), 1, 0, (0,)),)
    assert not gateway.received(WRITE)
