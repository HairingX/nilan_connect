"""The CTS400 model: its points as consumers know them, and what a real unit's registers decode
to through the client and a simulated gateway."""
import asyncio
import json
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

import pytest
import pytest_asyncio
from modbus_event_connect import Client, DataType, DataValue, InvalidValueError, Key, Point, Quality, ReadOnlyError, Transforms, Unit
from modbus_event_connect.micro_nabto import (
    DatapointRegister,
    MicroNabtoConnection,
    MicroNabtoDevice,
    SetpointRegister,
)
from modbus_event_connect.testing import assert_models_valid

from nilan_connect import CTS400, Alarm, PointKey, create_client, select_model
from nilan_connect._model import CTS400_POINTS
from nilan_connect.testing import FakeClock, SimulatedMicroNabtoDevice

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
    assert set(POINTS) <= {str(key) for key in PointKey.all()}


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
            # The filter alarm was active, yet the unit listed no alarm code.
            PointKey.ALARM_1: Alarm.NONE,
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


def _value[T](client: Client, key: Key[T]) -> T | None:
    current = client.value(key)
    return current.value if current is not None else None


def _polled(key: Key[Any], old: DataValue[Any] | None, new: DataValue[Any]) -> None:
    """A subscriber that only makes its key read."""


async def _clocked(gateway: SimulatedMicroNabtoDevice) -> tuple[Client, FakeClock]:
    """A client on the gateway whose time moves only when the test advances it."""
    clock = FakeClock()
    host, port = gateway.address
    connection = MicroNabtoConnection(EMAIL, host=host, port=port, timeout=0.2, retries=1, clock=clock)
    client = Client(MicroNabtoDevice(connection, owns_connection=True), select_model, clock=clock)
    await client.connect()
    return client, clock


async def test_a_filter_reset_reads_the_filters_status_and_timers_again_two_seconds_later(
        gateway: SimulatedMicroNabtoDevice) -> None:
    """A CTS400 was seen changing them all within 1.0 s of the reset."""
    client, clock = await _clocked(gateway)
    try:
        client.subscribe(PointKey.FILTER_OK, _polled)
        client.subscribe(PointKey.ALARM_STATUS, _polled)
        client.subscribe(PointKey.FILTER_REPLACE_TIME_AGO, _polled)
        client.subscribe(PointKey.FILTER_REPLACE_TIME_REMAIN, _polled)
        await client.write(PointKey.FILTER_REPLACE_RESET, True)
        # What the controller does once it has taken the reset.
        gateway.datapoint_registers.update({(0, 49): 0, (0, 50): 0, (0, 77): 0, (0, 110): 90})
        clock.advance(1.9)
        await client.poll()
        assert _value(client, PointKey.FILTER_OK) is False
        clock.advance(0.1)
        await client.poll()
        assert [_value(client, PointKey.FILTER_OK), _value(client, PointKey.ALARM_STATUS),
                _value(client, PointKey.FILTER_REPLACE_TIME_AGO),
                _value(client, PointKey.FILTER_REPLACE_TIME_REMAIN)] == [True, False, 0.0, 90]
    finally:
        await client.disconnect()


async def test_a_fan_level_reads_the_fans_level_and_speeds_again_three_seconds_later(
        gateway: SimulatedMicroNabtoDevice) -> None:
    """A CTS400 was seen changing them 1.3 to 1.8 s after the level was written."""
    client, clock = await _clocked(gateway)
    try:
        client.subscribe(PointKey.FAN_LEVEL_CURRENT, _polled)
        client.subscribe(PointKey.FAN_DUTYCYCLE_EXTRACT, _polled)
        client.subscribe(PointKey.FAN_DUTYCYCLE_SUPPLY, _polled)
        await client.write(PointKey.FAN_LEVEL, 2)
        # What the controller does once it has taken the level.
        gateway.datapoint_registers.update({(0, 63): 2, (0, 24): 410, (0, 25): 400})
        clock.advance(2.9)
        await client.poll()
        assert _value(client, PointKey.FAN_LEVEL_CURRENT) == 1
        clock.advance(0.1)
        await client.poll()
        assert [_value(client, PointKey.FAN_LEVEL_CURRENT), _value(client, PointKey.FAN_DUTYCYCLE_EXTRACT),
                _value(client, PointKey.FAN_DUTYCYCLE_SUPPLY)] == [2, 41.0, 40.0]
    finally:
        await client.disconnect()


async def test_a_filter_interval_reads_the_days_left_again_two_seconds_later(
        gateway: SimulatedMicroNabtoDevice) -> None:
    """A CTS400 was seen changing them 1.0 s after the interval was written."""
    client, clock = await _clocked(gateway)
    try:
        client.subscribe(PointKey.FILTER_REPLACE_TIME_REMAIN, _polled)
        await client.write(PointKey.FILTER_REPLACE_INTERVAL, 91)
        # What the controller does once it has taken the interval.
        gateway.datapoint_registers[(0, 110)] = 91
        clock.advance(1.9)
        await client.poll()
        assert _value(client, PointKey.FILTER_REPLACE_TIME_REMAIN) == 0
        clock.advance(0.1)
        await client.poll()
        assert _value(client, PointKey.FILTER_REPLACE_TIME_REMAIN) == 91
    finally:
        await client.disconnect()


async def test_a_created_client_sends_a_write_again_until_the_gateway_takes_it(
        gateway: SimulatedMicroNabtoDevice) -> None:
    """A CTS400's gateway answered 0x63 and 0x85 to writes it took on a later try."""
    host, port = gateway.address
    client = create_client(EMAIL, host=host, port=port)
    await client.connect()
    try:
        gateway.write_statuses = [0x63, 0x85]
        assert await client.write(PointKey.FAN_LEVEL, 2) is True
        assert len(gateway.received(SETPOINT_WRITE)) == 3
        assert gateway.setpoint_registers[(0, 69)] == 2
    finally:
        await client.disconnect()


async def test_a_created_client_with_write_retry_for_0_sends_a_write_once(
        gateway: SimulatedMicroNabtoDevice) -> None:
    host, port = gateway.address
    client = create_client(EMAIL, host=host, port=port, write_retry_for=0)
    await client.connect()
    try:
        gateway.write_statuses = [0x63]
        assert await client.write(PointKey.FAN_LEVEL, 2) is False
        assert len(gateway.received(SETPOINT_WRITE)) == 1
        assert gateway.setpoint_registers[(0, 69)] == 1
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


async def test_a_client_reaches_a_gateway_on_the_port_it_is_given(gateway: SimulatedMicroNabtoDevice) -> None:
    host, port = gateway.address
    client = create_client(EMAIL, host=host, port=port, read_only=True)
    await client.connect()
    try:
        assert client.model is CTS400
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
