"""The CTS400 model: its points as consumers know them, and what a real unit's registers decode
to through the client and a simulated gateway."""
import asyncio
import json
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

import pytest
import pytest_asyncio
from modbus_event_connect import Client, DataType, InvalidValueError, Key, Point, Quality, ReadOnlyError, Transforms, Unit
from modbus_event_connect.micro_nabto import (
    DatapointRegister,
    MicroNabtoConnection,
    MicroNabtoDevice,
    SetpointRegister,
)
from modbus_event_connect.testing import assert_models_valid

from nilan_connect import CTS400, PointKey, select_model
from nilan_connect._model import CTS400_POINTS
from nilan_connect.testing import SimulatedMicroNabtoDevice

EMAIL = "user@example.invalid"
SETPOINT_WRITE = 0x2B
CTS400_IDENTITY = {"device_number": 72280, "device_model": 1140, "slave_device_number": 72270, "slave_device_model": 1}

POINTS: dict[str, dict[str, Any]] = json.loads(
    (Path(__file__).parent / "cts400_points.json").read_text(encoding="utf-8"))
"""Every CTS400 point by key, as consumers have stored it: a change here changes what they have."""

READ: dict[str, dict[str, int]] = json.loads(
    (Path(__file__).parent / "cts400_read_2026_09_27.json").read_text(encoding="utf-8"))
"""Every register the manual lists, as a CTS400 answered them on 2026-09-27, bypass open and
its filter alarm active."""

_TRANSFORMS = {"invert_bool": Transforms.INVERT_BOOL, "seconds_as_minutes": Transforms.SECONDS_AS_MINUTES,
               "hours_as_days": Transforms.HOURS_AS_DAYS}


def _point(key: str) -> Point[Any]:
    return next(p for p in CTS400_POINTS if p.key == key)


# ================================================================================== points


def test_the_keys_are_the_ones_consumers_have() -> None:
    """A consumer's stored entities are built on these strings."""
    assert sorted(p.key for p in CTS400_POINTS) == sorted(POINTS)
    assert sorted(PointKey.all()) == sorted(POINTS)


@pytest.mark.parametrize("key", sorted(POINTS))
def test_each_point_is_read_and_written_as_described(key: str) -> None:
    expected, point = POINTS[key], _point(key)
    space = DatapointRegister if expected["space"] == "datapoint" else SetpointRegister
    assert point.read == (space(expected["read"]) if expected["read"] is not None else None)
    assert point.write == (SetpointRegister(expected["write"]) if expected["write"] is not None else None)
    assert point.scale == pytest.approx(expected["scale"])
    assert (point.data_type is DataType.INT16) == expected["signed"]
    assert point.transform is _TRANSFORMS.get(expected["transform"])
    assert point.unit == (Unit(expected["unit"]) if expected["unit"] is not None else None)
    limits = expected.get("limits")
    if limits is None:
        assert point.limits is None
    else:
        assert point.limits is not None
        assert (point.limits.min, point.limits.max, point.limits.step) == pytest.approx(tuple(limits))


# ============================================================================== the model


def test_the_model_is_valid_for_a_cts400() -> None:
    assert_models_valid(CTS400, identities=[CTS400_IDENTITY])


def test_a_cts400_handshake_selects_the_cts400() -> None:
    assert select_model(CTS400_IDENTITY) is CTS400


@pytest.mark.parametrize("identity", [
    {"device_model": 1140, "slave_device_number": 2763306, "slave_device_model": 2},
    {"device_model": 1140, "slave_device_number": 72270, "slave_device_model": 2},
    {"device_model": 2010, "device_number": 79265},
    {"device_model": 1040, "slave_device_number": 79250, "slave_device_model": 1},
], ids=["cts602-light", "cts400-other-slave-model", "optima-270", "optima-250"])
def test_no_model_is_selected_for_a_controller_not_supported_yet(identity: dict[str, int]) -> None:
    assert select_model(identity) is None


# ================================================================== through a simulated gateway


@pytest_asyncio.fixture  # pyright: ignore[reportUntypedFunctionDecorator, reportUnknownMemberType]
async def gateway() -> AsyncGenerator[SimulatedMicroNabtoDevice, None]:
    simulated = SimulatedMicroNabtoDevice(
        emails=frozenset({EMAIL}), identity=CTS400_IDENTITY,
        datapoint_registers={(0, int(a)): v for a, v in READ["datapoints"].items()},
        setpoint_registers={(0, int(a)): v for a, v in READ["setpoints"].items()})
    async with simulated:
        yield simulated


def _client(gateway: SimulatedMicroNabtoDevice, *, read_only: bool = False) -> Client:
    host, port = gateway.address
    connection = MicroNabtoConnection(EMAIL, host=host, port=port, timeout=0.2, retries=1)
    return Client(MicroNabtoDevice(connection, owns_connection=True), select_model, read_only=read_only)


async def _connected(gateway: SimulatedMicroNabtoDevice, *, read_only: bool = False) -> Client:
    client = _client(gateway, read_only=read_only)
    await client.connect()
    return client


async def _written(gateway: SimulatedMicroNabtoDevice) -> list[tuple[int, ...]]:
    """A write gets no answer to wait for, so wait for the gateway to have received it."""
    for _ in range(100):
        if gateway.received(SETPOINT_WRITE):
            break
        await asyncio.sleep(0.01)
    return [item for command in gateway.received(SETPOINT_WRITE) for item in command.items]


async def test_a_real_units_registers_read_as_what_they_mean(gateway: SimulatedMicroNabtoDevice) -> None:
    client = await _connected(gateway)
    try:
        expected: dict[Key[Any], object] = {
            PointKey.TEMP_OUTSIDE: 15.2, PointKey.TEMP_SUPPLY: 16.4, PointKey.TEMP_EXTRACT: 23.1,
            PointKey.TEMP_EXHAUST: 23.9, PointKey.HUMIDITY: 56.0,
            PointKey.FAN_DUTYCYCLE_EXTRACT: 26.0, PointKey.FAN_DUTYCYCLE_SUPPLY: 24.0,
            PointKey.FAN_LEVEL_CURRENT: 1, PointKey.FAN_LEVEL: 1,
            PointKey.FAN_LEVEL1_EXTRACT_PRESET: 26.0, PointKey.FAN_LEVEL1_SUPPLY_PRESET: 24.0,
            PointKey.BYPASS_ACTIVE: True, PointKey.ALARM_STATUS: True, PointKey.FILTER_OK: False,
            PointKey.FILTER_REPLACE_TIME_AGO: 139.0, PointKey.FILTER_REPLACE_TIME_REMAIN: 0,
            PointKey.FILTER_REPLACE_INTERVAL: 90, PointKey.WINTER_MODE_ACTIVE: False,
            PointKey.TEMP_WINTER_MODE_THRESHOLD: 12.0, PointKey.HUMIDITY_HIGH_ACTIVE: False,
            PointKey.HUMIDITY_HIGH_LEVEL: 64.6, PointKey.HUMIDITY_HIGH_LEVEL_TIME: 0.0,
            PointKey.ENABLE: True, PointKey.TEMP_TARGET: 23.0, PointKey.HUMIDITY_LOW_THRESHOLD: 30.0,
        }
        found = {key: current.value for key in expected if (current := client.value(key)) is not None}
        assert found == pytest.approx(expected)
    finally:
        await client.disconnect()


async def test_every_readable_point_of_a_real_unit_is_read(gateway: SimulatedMicroNabtoDevice) -> None:
    client = await _connected(gateway)
    try:
        readable = {p.key for p in CTS400_POINTS if p.readable}
        assert {key for key in readable if (v := client.value(key)) is not None and v.quality is Quality.GOOD} == readable
        assert not client.unavailable_reasons
    finally:
        await client.disconnect()


@pytest.mark.parametrize("key,value,register", [
    (PointKey.ENABLE, False, 0),
    (PointKey.TEMP_TARGET, 21.5, 215),
    (PointKey.FAN_LEVEL, 3, 3),
    (PointKey.ALARM_RESET, True, 1),
    (PointKey.FILTER_REPLACE_RESET, True, 1),
], ids=["enable", "temp_target", "fan_level", "alarm_reset", "filter_replace_reset"])
async def test_a_write_reaches_its_setpoint(gateway: SimulatedMicroNabtoDevice, key: str, value: object,
                                            register: int) -> None:
    client = await _connected(gateway)
    try:
        await client.write(_point(key).key, value)
        write = _point(key).write
        assert isinstance(write, SetpointRegister)
        assert (0, write.address, register) in await _written(gateway)
    finally:
        await client.disconnect()


async def test_a_value_outside_the_manuals_limits_is_refused(gateway: SimulatedMicroNabtoDevice) -> None:
    client = await _connected(gateway)
    try:
        with pytest.raises(InvalidValueError):
            await client.write(PointKey.TEMP_TARGET, 30.5)
        assert not gateway.received(SETPOINT_WRITE)
    finally:
        await client.disconnect()


async def test_a_read_only_client_writes_nothing(gateway: SimulatedMicroNabtoDevice) -> None:
    client = await _connected(gateway, read_only=True)
    try:
        with pytest.raises(ReadOnlyError):
            await client.write(PointKey.ENABLE, False)
        assert not gateway.received(SETPOINT_WRITE)
    finally:
        await client.disconnect()
