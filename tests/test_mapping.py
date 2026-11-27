"""Mapping a controller: the gateway's own registers, found once and then read where they answered."""
import json
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
import pytest_asyncio

from nilan_connect import (
    CTS400,
    MODELS,
    UNRECOGNISED,
    Area,
    Level,
    RawAddress,
    RegisterChange,
    UnsupportedDeviceError,
    difference,
    model_points,
)
from nilan_connect.testing import SimulatedMicroNabtoDevice, client_for

EMAIL = "user@example.invalid"
WRITE = 0x2B
CTS400_IDENTITY = {"device_number": 72280, "device_model": 1140, "slave_device_number": 72270, "slave_device_model": 1}
READ: dict[str, dict[str, int]] = json.loads(
    (Path(__file__).parent / "cts400_read_2026_09_27.json").read_text(encoding="utf-8"))
"""What a real CTS400's gateway answered on 2026-09-27; datapoints 79, 80, 82 and 89 are in no list."""
FIRST_READ = 672
"""Requests of the first read: about one for each of the 508 absent addresses of 0-299."""


@pytest_asyncio.fixture  # pyright: ignore[reportUntypedFunctionDecorator, reportUnknownMemberType]
async def gateway() -> AsyncGenerator[SimulatedMicroNabtoDevice, None]:
    async with SimulatedMicroNabtoDevice(
            emails=frozenset({EMAIL}), identity=CTS400_IDENTITY,
            datapoint_registers={(0, int(a)): v for a, v in READ["datapoints"].items()},
            setpoint_registers={(0, int(a)): v for a, v in READ["setpoints"].items()}) as simulated:
        yield simulated


async def test_a_cts400_is_mapped_in_its_gateways_numbers_at_every_address_up_to_the_limit(
        gateway: SimulatedMicroNabtoDevice) -> None:
    client = client_for(gateway, email=EMAIL, timeout=0.2, retries=1, level=Level.TEST, read_only=True)
    await client.connect()
    assert client.model is CTS400
    assert client.mapping_areas(limit=300) == (Area("datapoint", 0, 300), Area("setpoint", 0, 300))
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
    assert set(found.values) | found.missing == {
        RawAddress(space, a) for space in ("datapoint", "setpoint") for a in range(300)}
    assert first == FIRST_READ
    assert len(gateway.commands) == 2
    assert difference(found, again) == (RegisterChange(RawAddress("setpoint", 82), 1, 0, (0,)),)
    assert not gateway.received(WRITE)


UNKNOWN_IDENTITY = {"device_number": 79299, "device_model": 2030, "slave_device_number": 1, "slave_device_model": 1}
"""Numbers no model knows, as a model not supported yet would report them."""


async def test_a_unit_no_model_matches_is_refused_unless_unrecognised_units_are_accepted() -> None:
    async with SimulatedMicroNabtoDevice(emails=frozenset({EMAIL}), identity=UNKNOWN_IDENTITY) as gateway:
        refused = client_for(gateway, email=EMAIL, timeout=0.2, retries=1)
        with pytest.raises(UnsupportedDeviceError) as raised:
            await refused.connect()
        assert raised.value.identity == UNKNOWN_IDENTITY


async def test_an_unrecognised_unit_has_no_points_reports_its_numbers_and_is_mapped_like_any_other() -> None:
    async with SimulatedMicroNabtoDevice(
            emails=frozenset({EMAIL}), identity=UNKNOWN_IDENTITY,
            datapoint_registers={(0, 0): 15, (0, 21): 17, (0, 299): 3},
            setpoint_registers={(0, 5): 59}) as gateway:
        client = client_for(gateway, email=EMAIL, timeout=0.2, retries=1, unrecognised=True)
        await client.connect()
        assert client.model is UNRECOGNISED and dict(client.identity) == UNKNOWN_IDENTITY
        assert client.points == {} and client.values == {}
        assert client.mapping_areas(limit=300) == (Area("datapoint", 0, 300), Area("setpoint", 0, 300))
        found = await client.map_areas(limit=300)
        again = await client.read_mapped(found)
        await client.disconnect()
    assert {str(address): word for address, word in found.values.items()} == {
        "datapoint 0": 15, "datapoint 21": 17, "datapoint 299": 3, "setpoint 5": 59}
    assert difference(found, again) == ()
    assert not gateway.received(WRITE)


async def test_a_unit_a_model_matches_keeps_its_model_where_unrecognised_units_are_accepted(
        gateway: SimulatedMicroNabtoDevice) -> None:
    client = client_for(gateway, email=EMAIL, timeout=0.2, retries=1, unrecognised=True)
    await client.connect()
    await client.disconnect()
    assert client.model is CTS400


def test_the_unrecognised_unit_is_no_model_a_unit_is_chosen_as() -> None:
    assert UNRECOGNISED not in MODELS
    assert UNRECOGNISED.name == "Unrecognised unit" and model_points(UNRECOGNISED) == ()
