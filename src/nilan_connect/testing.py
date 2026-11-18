"""What a test of code that uses a Nilan controller needs: a simulated gateway on a local port, a
client of it, and a clock the test moves."""
from modbus_event_connect import Client, Clock
from modbus_event_connect.testing import FakeClock, SimulatedMicroNabtoDevice

from ._nilan import build_client

__all__ = [
    "FakeClock",
    "SimulatedMicroNabtoDevice",
    "client_for",
]


def client_for(gateway: SimulatedMicroNabtoDevice, *, email: str, timeout: float, retries: int,
               clock: Clock | None = None, read_only: bool = False) -> Client:
    """A client of the started `gateway` as `create_client` makes it, but whose requests are given
    `timeout` seconds to be acknowledged and are sent again `retries` times, so that a test need
    not wait for a request the gateway leaves unanswered."""
    host, port = gateway.address
    return build_client(email, host=host, device_id=None, port=port, timeout=timeout, retries=retries,
                        read_only=read_only, clock=clock)
