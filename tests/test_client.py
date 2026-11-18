"""The client `create_client` makes, and discovery: how they reach a gateway before its model is known."""
from collections.abc import AsyncGenerator
from dataclasses import fields
from typing import Any

import pytest
import pytest_asyncio
from event_connect import ModelInfo
from modbus_event_connect import CircuitBreaker, Fixed, Retry
from modbus_event_connect.micro_nabto import BROADCAST, DiscoveredDevice as FoundDevice, MicroNabtoDevice

import nilan_connect._nilan
from nilan_connect import (
    CTS400,
    MODELS,
    PORT,
    Client,
    DeviceClient,
    DiscoveredDevice,
    NotConnectedError,
    create_client,
    discover,
)
from nilan_connect.testing import FakeClock, SimulatedMicroNabtoDevice

EMAIL = "user@example.invalid"
CTS400_IDENTITY = {"device_number": 72280, "device_model": 1140, "slave_device_number": 72270, "slave_device_model": 1}


@pytest_asyncio.fixture  # pyright: ignore[reportUntypedFunctionDecorator, reportUnknownMemberType]
async def gateway() -> AsyncGenerator[SimulatedMicroNabtoDevice, None]:
    async with SimulatedMicroNabtoDevice(device_id="gateway.example.invalid", emails=frozenset({EMAIL}),
                                         identity=CTS400_IDENTITY) as simulated:
        yield simulated


def _udp_told(monkeypatch: pytest.MonkeyPatch, **settings: Any) -> dict[str, Any]:
    """What `create_client(**settings)` tells the device it makes."""
    told: dict[str, Any] = {}
    udp = MicroNabtoDevice.udp

    def recording(*args: Any, **kwargs: Any) -> MicroNabtoDevice:
        told.update(kwargs, email=args[0])
        return udp(*args, **kwargs)

    monkeypatch.setattr(MicroNabtoDevice, "udp", recording)
    create_client(**settings)
    return told


def test_a_created_client_talks_to_each_model_as_it_says_on_the_standard_port(monkeypatch: pytest.MonkeyPatch) -> None:
    told = _udp_told(monkeypatch, email=EMAIL, host="192.0.2.1")
    assert (told["email"], told["host"], told["device_id"], told["port"]) == (EMAIL, "192.0.2.1", None, 5570)
    assert told["models"] is MODELS


def test_a_created_client_reaches_a_gateway_by_its_id_by_discovery_on_the_local_network(
        monkeypatch: pytest.MonkeyPatch) -> None:
    told = _udp_told(monkeypatch, email=EMAIL, device_id="gateway.example.invalid", port=5571)
    assert (told["host"], told["device_id"], told["port"]) == (None, "gateway.example.invalid", 5571)
    assert told["discovery_target"] == BROADCAST
    assert (told["rediscovery_timeout"], told["rediscovery_resend"]) == (3.0, 0.5)


def test_a_created_client_gives_a_request_1_s_to_be_acknowledged_and_sends_it_twice_more(
        monkeypatch: pytest.MonkeyPatch) -> None:
    told = _udp_told(monkeypatch, email=EMAIL, host="192.0.2.1")
    assert (told["timeout"], told["retries"]) == (1.0, 2)


def test_a_created_client_takes_a_session_as_ended_after_12_s_without_a_request(monkeypatch: pytest.MonkeyPatch) -> None:
    """A CTS402's gateway was measured ending a session between 15 and 20 s without a request."""
    assert _udp_told(monkeypatch, email=EMAIL, host="192.0.2.1")["session_idle"] == 12.0


def test_a_created_client_waits_5_s_for_an_acknowledged_write_or_first_handshake(
        monkeypatch: pytest.MonkeyPatch) -> None:
    assert _udp_told(monkeypatch, email=EMAIL, host="192.0.2.1")["answer_wait"] == 5.0


def test_after_a_failed_handshake_a_client_tries_one_again_every_five_seconds(monkeypatch: pytest.MonkeyPatch) -> None:
    told = _udp_told(monkeypatch, email=EMAIL, host="192.0.2.1")
    assert told["reconnect"] == CircuitBreaker(after=1, retry=Retry(Fixed(5.0), None))


def test_a_created_client_counts_a_gateway_as_not_answering_after_one_missed_fast_read(
        monkeypatch: pytest.MonkeyPatch) -> None:
    told: dict[str, Any] = {}

    def recording(*args: Any, **kwargs: Any) -> Client:
        told.update(kwargs)
        return Client(*args, **kwargs)

    monkeypatch.setattr(nilan_connect._nilan, "Client", recording)
    create_client(email=EMAIL, host="192.0.2.1")
    assert told["offline_after_intervals"] == 1


def test_a_client_needs_the_gateways_address_or_its_id() -> None:
    with pytest.raises(ValueError):
        create_client(email=EMAIL)


def test_a_created_client_is_the_client_every_device_library_shares() -> None:
    client: DeviceClient = create_client(email=EMAIL, host="192.0.2.1")
    assert isinstance(client, DeviceClient)


async def test_a_created_client_tells_its_model_once_connected(gateway: SimulatedMicroNabtoDevice) -> None:
    host, port = gateway.address
    client = create_client(email=EMAIL, host=host, port=port, clock=FakeClock())
    with pytest.raises(NotConnectedError):
        client.model
    await client.connect()
    try:
        model: ModelInfo = client.model
        assert model is CTS400 and (model.name, model.manufacturer) == ("CTS 400", "Nilan")
    finally:
        await client.disconnect()


async def test_a_disconnected_client_reads_nothing_until_it_is_connected_again(
        gateway: SimulatedMicroNabtoDevice) -> None:
    host, port = gateway.address
    client = create_client(email=EMAIL, host=host, port=port)
    await client.connect()
    await client.disconnect()
    with pytest.raises(NotConnectedError):
        await client.poll()


def test_a_discovered_gateway_says_where_it_answered_from_before_who_it_is() -> None:
    assert [field.name for field in fields(DiscoveredDevice)] == ["host", "port", "device_id"]


async def test_discovery_finds_the_gateway_asked(gateway: SimulatedMicroNabtoDevice,
                                                 monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(nilan_connect._nilan, "_DISCOVERY_TIMEOUT", 0.3)
    host, port = gateway.address
    assert await discover(target=host, port=port) == [DiscoveredDevice(host, port, "gateway.example.invalid")]


@pytest.mark.parametrize(("settings", "target"), [
    ({}, ("255.255.255.255", PORT)),
    ({"port": 5571}, ("255.255.255.255", 5571)),
    ({"target": "192.0.2.1"}, ("192.0.2.1", PORT)),
], ids=["broadcast", "broadcast-on-a-port", "one-host"])
async def test_discovery_waits_2_s_for_answers_sending_again_every_half_second(
        monkeypatch: pytest.MonkeyPatch, settings: dict[str, Any], target: tuple[str, int]) -> None:
    told: dict[str, Any] = {}

    async def recording(**kwargs: Any) -> list[FoundDevice]:
        told.update(kwargs)
        return [FoundDevice("gateway.example.invalid", "192.0.2.1", PORT)]

    monkeypatch.setattr(nilan_connect._nilan, "discover_devices", recording)
    assert await discover(**settings) == [DiscoveredDevice("192.0.2.1", PORT, "gateway.example.invalid")]
    assert told == {"timeout": 2.0, "resend": 0.5, "target": target}
