"""Read-only tests against a real Nilan controller.

    Configure it either way:
        set NILAN_HOST=<gateway-ip>             (environment variables)
        set NILAN_EMAIL=you@example.com

        NILAN_HOST = "<gateway-ip>"             (or in mysecrets.py, which is gitignored)
        NILAN_EMAIL = "you@example.com"

    Run:
        pytest tests/test_live_nilan.py -v -s

NOTHING HERE WRITES TO THE CONTROLLER: the client is read-only, and the one path a write could
take fails the test.
"""
from collections.abc import AsyncGenerator
from typing import Any, NoReturn

import pytest
import pytest_asyncio
from modbus_event_connect import Client, Quality
from modbus_event_connect.micro_nabto import MicroNabtoConnection, MicroNabtoDevice

from conftest import live_or_skip, live_setting
from nilan_connect import CTS400, PointKey, select_model
from nilan_connect._cts400 import CTS400_POINTS

HOST = live_setting("NILAN_HOST")
EMAIL = live_setting("NILAN_EMAIL")

pytestmark = [
    pytest.mark.asyncio(loop_scope="module"),
    *live_or_skip("Nilan", NILAN_HOST=HOST, NILAN_EMAIL=EMAIL),
]


@pytest_asyncio.fixture(scope="module", loop_scope="module")  # pyright: ignore[reportUntypedFunctionDecorator, reportUnknownMemberType]
async def client() -> AsyncGenerator[Client, None]:
    assert HOST is not None and EMAIL is not None   # guarded by the skip above
    connection = MicroNabtoConnection(EMAIL, host=HOST)

    async def refuse(command: bytes) -> NoReturn:
        raise AssertionError("a write was attempted; these tests are read-only")
    setattr(connection, "send", refuse)
    client = Client(MicroNabtoDevice(connection, owns_connection=True), select_model, read_only=True)
    await client.connect()
    yield client
    await client.disconnect()


async def test_the_controller_is_a_cts400(client: Client) -> None:
    assert client.model is CTS400


async def test_every_readable_point_reads_a_value(client: Client) -> None:
    readable = [p.key for p in CTS400_POINTS if p.readable and p.key in client.points]
    qualities: dict[str, Any] = {key: (v.quality if (v := client.value(key)) is not None else None)
                                 for key in readable}
    for key in readable:
        current = client.value(key)
        print(f"  {key:30} {current.value if current is not None else None}")
    assert {key: q for key, q in qualities.items() if q is not Quality.GOOD} == {}


async def test_the_temperatures_are_temperatures(client: Client) -> None:
    for key in (PointKey.TEMP_OUTSIDE, PointKey.TEMP_SUPPLY, PointKey.TEMP_EXTRACT, PointKey.TEMP_EXHAUST):
        current = client.value(key)
        assert current is not None and isinstance(current.value, float) and -40.0 < current.value < 70.0
