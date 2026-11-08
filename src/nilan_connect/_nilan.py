"""Using a Nilan controller: the profile of every model, and creating a client for it."""
from __future__ import annotations

from modbus_event_connect import CircuitBreaker, Client, Clock, Fixed, Retry, Within
from modbus_event_connect.micro_nabto import MicroNabtoDevice, MicroNabtoProfile

from ._cts400 import CTS400_MICRO_NABTO
from ._cts602 import CTS602_LIGHT_MICRO_NABTO, CTS602_MICRO_NABTO
from ._optima import (
    OPTIMA_250_MICRO_NABTO,
    OPTIMA_251_MICRO_NABTO,
    OPTIMA_260_MICRO_NABTO,
    OPTIMA_270_MICRO_NABTO,
    OPTIMA_301_MICRO_NABTO,
    OPTIMA_312_MICRO_NABTO,
    OPTIMA_314_MICRO_NABTO,
)
from ._select import select_model

PROFILES: tuple[MicroNabtoProfile, ...] = (
    CTS400_MICRO_NABTO,
    CTS602_MICRO_NABTO,
    CTS602_LIGHT_MICRO_NABTO,
    OPTIMA_250_MICRO_NABTO,
    OPTIMA_251_MICRO_NABTO,
    OPTIMA_260_MICRO_NABTO,
    OPTIMA_270_MICRO_NABTO,
    OPTIMA_301_MICRO_NABTO,
    OPTIMA_312_MICRO_NABTO,
    OPTIMA_314_MICRO_NABTO,
)
"""How each model `select_model` chooses is talked to over micro_nabto."""

# Asked again every 5 s after a failed handshake: shorter than the 10 s between reads, so the next
# read reaches the gateway instead of failing unsent.
_RECONNECT = CircuitBreaker(after=1, retry=Retry(Fixed(5.0)))

# A CTS400's gateway answered 0x63 and 0x85 to writes it took on a later try.
_WRITE_RETRY = Retry(Fixed(0.5), Within(15.0))


def create_client(email: str, *, host: str | None = None, device_id: str | None = None, port: int = 5570,
                  read_only: bool = False, clock: Clock | None = None) -> Client:
    """A client for the controller behind a Nilan gateway, with its own connection; call
    `connect()` on it.

    Args:
        email: the account the gateway is paired with in Nilan's app; it is never logged.
        host, device_id: where to reach the gateway; with only `device_id`, it is discovered.
        port: the gateway's UDP port; 5570 is micro_nabto's standard one.
        read_only: refuse every write before it reaches the controller.
        clock: the time the client plans by; None is the system's.

    After a failed handshake, one is tried again every 5 s. A write the controller did not take is
    sent again every 0.5 s, for up to 15 s after it was first sent. `connect()` raises
    `UnsupportedDeviceError` for a controller no model matches.
    """
    device = MicroNabtoDevice.udp(email, host=host, device_id=device_id, reconnect=_RECONNECT, profiles=PROFILES,
                                  port=port, clock=clock)
    return Client(device, select_model, write_retry=_WRITE_RETRY, clock=clock, read_only=read_only)
