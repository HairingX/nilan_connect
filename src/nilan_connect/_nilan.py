"""Using a Nilan controller: creating a client for it."""
from __future__ import annotations

from modbus_event_connect import Client, Clock
from modbus_event_connect.micro_nabto import MicroNabtoDevice

from ._model import select_model

WRITE_RETRY_FOR = 15.0
"""Seconds a write the controller did not take is sent again: a CTS400's gateway answered 0x63
and 0x85 to writes it took on a later try."""


def create_client(email: str, *, host: str | None = None, device_id: str | None = None,
                  port: int | None = None, read_only: bool = False, clock: Clock | None = None,
                  write_retry_for: float = WRITE_RETRY_FOR) -> Client:
    """A client for the controller behind a Nilan gateway, with its own connection; call
    `connect()` on it.

    Args:
        email: the account the gateway is paired with in Nilan's app; it is never logged.
        host, device_id: where to reach the gateway; with only `device_id`, it is discovered.
        port: the gateway's UDP port, when it is not micro_nabto's standard one.
        read_only: refuse every write before it reaches the controller.
        write_retry_for: seconds after its first sending that a write the controller did not
            take is still sent again; 0 sends every write once.

    `connect()` raises `UnsupportedDeviceError` for a controller no model matches.
    """
    connection: dict[str, int] = {} if port is None else {"port": port}
    return Client(MicroNabtoDevice.udp(email, host=host, device_id=device_id, clock=clock, **connection),
                  select_model, clock=clock, read_only=read_only, write_retry_for=write_retry_for)
