"""What a test of code that uses a Nilan controller needs: a simulated gateway on a local port,
and a clock the test moves."""
from modbus_event_connect.testing import FakeClock, SimulatedMicroNabtoDevice

__all__ = [
    "FakeClock",
    "SimulatedMicroNabtoDevice",
]
