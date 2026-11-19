"""Every model, a client for the controller behind a Nilan gateway, and finding the gateways."""
from __future__ import annotations

from dataclasses import dataclass

from modbus_event_connect import CircuitBreaker, Client, Clock, Fixed, Level, Retry
from modbus_event_connect.micro_nabto import BROADCAST, PORT, MicroNabtoDevice, MicroNabtoModel
from modbus_event_connect.micro_nabto import discover as discover_devices

from ._cts400 import CTS400
from ._cts602 import CTS602
from ._cts602_light import CTS602_LIGHT
from ._optima_250 import OPTIMA_250
from ._optima_251 import OPTIMA_251
from ._optima_260 import OPTIMA_260
from ._optima_270 import OPTIMA_270
from ._optima_301 import OPTIMA_301
from ._optima_312 import OPTIMA_312
from ._optima_314 import OPTIMA_314
from ._select import select_model

MODELS: tuple[MicroNabtoModel, ...] = (
    CTS400,
    CTS602,
    CTS602_LIGHT,
    OPTIMA_250,
    OPTIMA_251,
    OPTIMA_260,
    OPTIMA_270,
    OPTIMA_301,
    OPTIMA_312,
    OPTIMA_314,
)
"""Every model `select_model` chooses from."""

_TIMEOUT = 1.0  # guess
"""Seconds a request is given to be acknowledged before it is sent again."""

_RETRIES = 2  # guess
"""Times a request not acknowledged is sent again before the session is established anew."""

_SESSION_IDLE = 12.0  # measured on a CTS402: a session ended between 15 and 20 s without a request
"""Seconds without a request after which the session is taken to have ended."""

_ANSWER_WAIT = 5.0  # guess
"""Seconds an acknowledged write, or a handshake before the first read, is waited for; a read waits
as long as its model says."""

_REDISCOVERY_RESEND = 0.5  # guess
"""Seconds between two discoveries sent to find a gateway known only by its id."""

# A failed handshake is tried again after 5 s: shorter than the 10 s between reads, so the next
# read reaches the gateway instead of failing unsent.
_RECONNECT = CircuitBreaker(
    after=1,  # measured on a CTS602: one read left unanswered every 33 min (HairingX/ha_nilan_connect#23)
    retry=Retry(Fixed(5.0), None),  # measured on a CTS602: one read left unanswered every 33 min (HairingX/ha_nilan_connect#23)
)

# One missed read keeps the last values; a gateway that leaves the next unanswered too, 10 s
# after the first, counts as not answering.
_OFFLINE_AFTER_INTERVALS = 1  # measured on a CTS602: one read left unanswered every 33 min (HairingX/ha_nilan_connect#23)

_DISCOVERY_TIMEOUT = 2.0  # guess
"""Seconds discovery waits for gateways to answer."""

_DISCOVERY_RESEND = 0.5  # guess
"""Seconds between two discoveries sent, as a datagram can be lost."""


def create_client(*, email: str, host: str | None = None, device_id: str | None = None, port: int = PORT,
                  level: Level = Level.DOCUMENTED, read_only: bool = False, clock: Clock | None = None) -> Client:
    """A client for the controller behind a Nilan gateway, with its own connection; nothing is sent
    until `connect()`.

    Args:
        email: the account the gateway is paired with in Nilan's app; it is never logged.
        host: where to reach the gateway; without it, the gateway is found by `device_id`.
        device_id: the id the gateway answers discovery with; with it, a gateway that has moved is
            found again.
        port: the gateway's UDP port.
        level: which points the unit has: those read on a unit of its model (VERIFIED), also those
            its documentation states (DOCUMENTED), or every point, with each candidate in place of
            the point it replaces (TEST).
        read_only: refuse every write before it reaches the controller.
        clock: the time the client plans by; None is the system's.

    Raises:
        ValueError: neither `host` nor `device_id` is given.

    `connect()` raises `UnsupportedDeviceError` for a controller no model matches.
    """
    return build_client(email, host=host, device_id=device_id, port=port, timeout=_TIMEOUT, retries=_RETRIES,
                        level=level, read_only=read_only, clock=clock)


def build_client(email: str, *, host: str | None, device_id: str | None, port: int, timeout: float, retries: int,
                 level: Level, read_only: bool, clock: Clock | None) -> Client:
    """A client as `create_client` makes it, but whose requests are given `timeout` seconds to be
    acknowledged and are sent again `retries` times."""
    device = MicroNabtoDevice.udp(
        email, host=host, device_id=device_id, port=port, reconnect=_RECONNECT, models=MODELS,
        timeout=timeout, retries=retries, session_idle=_SESSION_IDLE,
        rediscovery_timeout=timeout * (retries + 1),  # guess: as long as a request is tried
        rediscovery_resend=_REDISCOVERY_RESEND, answer_wait=_ANSWER_WAIT, discovery_target=BROADCAST, clock=clock)
    return Client(device, select_model, offline_after_intervals=_OFFLINE_AFTER_INTERVALS, level=level,
                  read_only=read_only, clock=clock)


@dataclass(frozen=True)
class DiscoveredDevice:
    """A gateway that answered discovery."""

    host: str
    """The address it answered from."""
    port: int
    """The port it answered from."""
    device_id: str
    """The id it answers discovery with: `create_client(device_id=...)` finds it by it."""


async def discover(*, target: str | None = None, port: int = PORT) -> list[DiscoveredDevice]:
    """The gateways that answer a discovery sent to the host `target`, or to every host on the local
    network when it is None.

    Returns:
        Each gateway that answered, once.
    """
    found = await discover_devices(timeout=_DISCOVERY_TIMEOUT, resend=_DISCOVERY_RESEND,
                                   target=(BROADCAST[0] if target is None else target, port))
    return [DiscoveredDevice(device.host, device.port, device.device_id) for device in found]
