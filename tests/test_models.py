"""Every controller besides the CTS400: the model a handshake selects, the points each model and
variant has, where each point's address comes from, and values through a simulated gateway."""
import csv
import json
from datetime import datetime
from collections.abc import AsyncGenerator, Mapping
from pathlib import Path
from typing import Any

import pytest
from modbus_event_connect import Client, Model, Point, Section
from modbus_event_connect.micro_nabto import MicroNabtoConnection, MicroNabtoDevice, SetpointRegister

from nilan_connect import (
    CTS400,
    Alarm,
    OperationState,
    Weekday,
    CTS602,
    CTS602_LIGHT,
    OPTIMA_250,
    OPTIMA_251,
    OPTIMA_260,
    OPTIMA_270,
    OPTIMA_301,
    OPTIMA_312,
    OPTIMA_314,
    SOURCE,
    PointKey,
    Source,
    select_model,
)
from nilan_connect.testing import SimulatedMicroNabtoDevice

HERE = Path(__file__).parent
DOCS = HERE.parent / "docs" / "models"
EMAIL = "user@example.invalid"
SETPOINT_WRITE = 0x2B

MODELS: dict[str, Model] = {
    "CTS602": CTS602, "CTS602_LIGHT": CTS602_LIGHT, "OPTIMA_250": OPTIMA_250, "OPTIMA_251": OPTIMA_251,
    "OPTIMA_260": OPTIMA_260, "OPTIMA_270": OPTIMA_270, "OPTIMA_301": OPTIMA_301, "OPTIMA_312": OPTIMA_312,
    "OPTIMA_314": OPTIMA_314,
}

PINNED: dict[str, dict[str, Any]] = json.loads((HERE / "models_points.json").read_text(encoding="utf-8"))
"""Every point of every model, per device variant, as consumers get it: a change here changes
what they have."""

GROUP_STARTS: dict[str, dict[tuple[str, int], int]] = {
    "CTS602": {("IR", 200): 31, ("IR", 400): 64, ("IR", 1000): 84, ("IR", 1100): 98, ("HR", 1000): 136,
               ("HR", 1100): 154, ("HR", 1200): 170, ("HR", 1700): 189, ("HR", 1800): 201},
    "CTS602_LIGHT": {("IR", 200): 30, ("IR", 400): 63, ("IR", 1000): 83, ("IR", 1100): 97, ("HR", 1000): 132,
                     ("HR", 1100): 148},
}
"""The gateway address of the first register of each of a manual's groups."""

HANDSHAKE_ZEROS = {"device_number": 0, "device_model": 0, "slave_device_number": 0, "slave_device_model": 0}
"""What a simulated gateway's handshake says for a number the test does not care about."""

MANUALS = {"CTS602": ("nilan-cts602", "nilan-cts602-hmi350t"), "CTS602_LIGHT": ("nilan-cts602-light",)}


def _points(model: Model, identity: Mapping[str, int]) -> list[Point[Any]]:
    return [point for section in model.sections if isinstance(section, Section)
            if section.when is None or section.when(identity) for point in section.points]


def _describe(point: Point[Any]) -> dict[str, Any]:
    read, write, limits = point.read, point.write, point.limits
    return {
        "space": None if read is None else ("setpoint" if isinstance(read, SetpointRegister) else "datapoint"),
        "read": None if read is None else read.address,
        "write": None if write is None else write.address,
        "scale": point.scale, "offset": point.offset, "type": point.data_type.kind.name,
        "bit": point.data_type.bit_index, "unit": None if point.unit is None else point.unit.value,
        "limits": None if limits is None else [limits.min, limits.max, limits.step],
        "source": point.labels[SOURCE],
        "codes": None if point.codes is None else {str(code): state.name for code, state in point.codes.items()},
    }


def _every_point() -> list[tuple[str, Point[Any]]]:
    return [(variant, point) for variant, pinned in PINNED.items()
            for point in _points(MODELS[variant.split("/")[0]], pinned["identity"])]


# ============================================================================== selection


@pytest.mark.parametrize("variant", sorted(PINNED))
def test_a_handshake_selects_its_model(variant: str) -> None:
    assert select_model(PINNED[variant]["identity"]) is MODELS[variant.split("/")[0]]


@pytest.mark.parametrize("device_model", [1140, 1141])
def test_both_nilan_device_models_select_the_cts400(device_model: int) -> None:
    identity = {"device_model": device_model, "slave_device_number": 72270, "slave_device_model": 1}
    assert select_model(identity) is CTS400


@pytest.mark.parametrize("identity", [
    {"device_model": 1140, "slave_device_number": 72270, "slave_device_model": 2},
    {"device_model": 1040, "slave_device_number": 79250, "slave_device_model": 3},
    {"device_model": 1040, "slave_device_number": 70810, "slave_device_model": 1},
    {"device_model": 2010, "device_number": 1},
    {"device_model": 9999},
], ids=["cts400-other-slave-model", "optima-other-slave-model", "optima-260-other-slave-model",
        "optima-270-other-device", "unknown"])
def test_no_model_is_selected_for_a_controller_not_supported(identity: dict[str, int]) -> None:
    assert select_model(identity) is None


# ================================================================================= points


@pytest.mark.parametrize("variant", sorted(PINNED))
def test_each_models_points_are_the_ones_pinned(variant: str) -> None:
    pinned = PINNED[variant]
    points = _points(MODELS[variant.split("/")[0]], pinned["identity"])
    assert len({p.key for p in points}) == len(points), "a key twice in one variant"
    assert {p.key: _describe(p) for p in points} == pinned["points"]


def test_every_key_is_declared() -> None:
    declared = {str(key) for key in PointKey.all()}
    assert {point.key for _, point in _every_point()} <= declared


def test_every_point_says_where_its_address_comes_from() -> None:
    sources = {Source.TESTED, Source.UNTESTED, Source.CALCULATED}
    assert all(point.labels.get(SOURCE) in sources for _, point in _every_point())
    cts400 = {"device_model": 1140, "slave_device_number": 72270, "slave_device_model": 1}
    assert all(point.labels.get(SOURCE) == Source.TESTED for point in _points(CTS400, cts400))


def test_only_the_optima_270_and_the_confirmed_cts602_temperatures_are_tested_besides_the_cts400() -> None:
    tested = {(variant.split("/")[0], point.key) for variant, point in _every_point()
              if point.labels[SOURCE] == Source.TESTED}
    assert {model for model, _ in tested} == {"OPTIMA_270", "CTS602"}
    assert {key for model, key in tested if model == "CTS602"} == {
        "temp_supply", "temp_extract", "temp_exhaust", "temp_outside"}


def test_a_calculated_point_can_never_be_written() -> None:
    calculated = [point for _, point in _every_point() if point.labels[SOURCE] == Source.CALCULATED]
    assert calculated
    assert all(point.write is None and point.readable for point in calculated)


@pytest.mark.parametrize("model", sorted(GROUP_STARTS))
def test_a_calculated_address_is_a_manual_register_placed_by_its_group(model: str) -> None:
    """Within one of a manual's groups the gateway keeps the manual's order and spacing."""
    documented: set[tuple[str, int]] = set()
    for folder in MANUALS[model]:
        with (DOCS / folder / "registers.csv").open(encoding="utf-8") as rows:
            documented |= {(row["table"], int(row["address"])) for row in csv.DictReader(rows)}
    placed = {}
    for (table, base), start in GROUP_STARTS[model].items():
        for table_, address in documented:
            if table_ == table and address // 100 * 100 == base:
                placed[(table, start + address - base)] = address
    variants = [v for v in PINNED if v.split("/")[0] == model]
    for variant in variants:
        for point in _points(MODELS[model], PINNED[variant]["identity"]):
            if point.labels[SOURCE] != Source.CALCULATED:
                continue
            assert point.read is not None
            table = "HR" if isinstance(point.read, SetpointRegister) else "IR"
            assert (table, point.read.address) in placed, point.key


# =================================================================== through a simulated gateway


async def _client(identity: Mapping[str, int], datapoints: dict[int, int],
                  setpoints: dict[int, int]) -> AsyncGenerator[tuple[Client, SimulatedMicroNabtoDevice], None]:
    simulated = SimulatedMicroNabtoDevice(
        emails=frozenset({EMAIL}), identity={**HANDSHAKE_ZEROS, **identity},
        datapoint_registers={(0, a): v for a, v in datapoints.items()},
        setpoint_registers={(0, a): v for a, v in setpoints.items()})
    async with simulated:
        host, port = simulated.address
        connection = MicroNabtoConnection(EMAIL, host=host, port=port, timeout=0.2, retries=1)
        client = Client(MicroNabtoDevice(connection, owns_connection=True), select_model)
        await client.connect()
        try:
            yield client, simulated
        finally:
            await client.disconnect()


def _value(client: Client, key: Any) -> object:
    current = client.value(key)
    return None if current is None else current.value


async def test_an_optima_reads_its_offset_temperatures_and_writes_where_it_takes_writes() -> None:
    async for client, simulated in _client(PINNED["OPTIMA_270"]["identity"], {20: 500}, {1: 110}):
        assert _value(client, PointKey.TEMP_SUPPLY) == pytest.approx(20.0)
        assert _value(client, PointKey.TEMP_TARGET) == pytest.approx(21.0)
        assert await client.write(PointKey.TEMP_TARGET, 22.0) is True
        assert [c.items for c in simulated.received(SETPOINT_WRITE)] == [((0, 12, 120),)]


@pytest.mark.parametrize(("slave_model", "address"), [(13, 34), (3, 41)])
async def test_a_cts602_reads_its_extract_air_where_its_variant_has_it(slave_model: int, address: int) -> None:
    identity = dict(PINNED["CTS602/0"]["identity"], slave_device_model=slave_model)
    async for client, _ in _client(identity, {address: 2150}, {}):
        assert _value(client, PointKey.TEMP_EXTRACT) == pytest.approx(21.5)


async def test_a_calculated_alarm_status_is_the_bit_the_manual_names_for_an_active_alarm() -> None:
    async for client, _ in _client(PINNED["CTS602_LIGHT"]["identity"], {63: 0x80}, {}):
        assert _value(client, PointKey.ALARM_STATUS) is True


async def test_a_calculated_alarms_time_is_its_dos_date_and_time() -> None:
    date_word, time_word = (46 << 9) | (9 << 5) | 29, (13 << 11) | (37 << 5) | 21
    async for client, _ in _client(PINNED["CTS602/0"]["identity"], {66: date_word, 67: time_word}, {}):
        assert _value(client, PointKey.ALARM_1_TIME) == datetime(2026, 9, 29, 13, 37, 42)


# =============================================================================== shared states


def _point(variant: str, key: str) -> Point[Any]:
    return next(p for p in _points(MODELS[variant.split("/")[0]], PINNED[variant]["identity"]) if p.key == key)


def test_the_same_alarm_is_one_state_whichever_code_a_controller_gives_it() -> None:
    """A CTS400 calls its filter alarm 1, a CTS602 19; to a CTS602, 1 is a hardware fault."""
    cts400 = {"device_model": 1140, "slave_device_number": 72270, "slave_device_model": 1}
    cts400_alarm = next(p for p in _points(CTS400, cts400) if p.key == PointKey.ALARM_1)
    assert cts400_alarm.codes is not None and cts400_alarm.codes[1] is Alarm.CHANGE_FILTER
    cts602_alarm = _point("CTS602/0", PointKey.ALARM_1)
    assert cts602_alarm.codes is not None
    assert cts602_alarm.codes[19] is Alarm.CHANGE_FILTER and cts602_alarm.codes[1] is Alarm.HARDWARE


async def test_an_alarm_code_stays_the_code_and_its_alarm_is_a_key_of_its_own() -> None:
    async for client, _ in _client(PINNED["CTS602/0"]["identity"], {65: 19}, {}):
        assert _value(client, PointKey.ALARM_1_CODE) == 19
        assert _value(client, PointKey.ALARM_1) is Alarm.CHANGE_FILTER


async def test_an_optimas_alarm_bits_are_alarms_of_their_own_with_the_filter_as_filter_ok() -> None:
    async for client, _ in _client(PINNED["OPTIMA_270"]["identity"], {114: 0b11, 115: 1 << 6}, {}):
        assert _value(client, PointKey.FILTER_OK) is False
        assert _value(client, PointKey.ALARM_EXTERNAL_STOP) is True
        assert _value(client, PointKey.ALARM_ROTOR) is True
        assert _value(client, PointKey.ALARM_SENSOR_T1_ERROR) is False


def test_the_state_code_names_only_the_control_states_of_the_manual() -> None:
    state = _point("CTS602/0", PointKey.OPERATION_STATE)
    assert state.states[-1] is OperationState.HEATING_HOT_WATER and len(state.states) == 18


def test_heat_pump_states_that_share_a_text_are_one_state() -> None:
    heat_pump = _point("CTS602/44", PointKey.HEAT_PUMP_STATE)
    assert heat_pump.codes is not None
    assert heat_pump.codes[6] is heat_pump.codes[10] is OperationState.HEAT_PUMP_STOP


async def test_a_weekday_is_numbered_as_the_manual_numbers_it() -> None:
    """HotWater.LegioType: "0=OFF, 1=Mandag, ..., 7=sondag"."""
    async for client, simulated in _client(PINNED["CTS602/9"]["identity"], {}, {194: 1}):
        assert _value(client, PointKey.ANTILEGIONELLA_DAY) is Weekday.MONDAY
        assert await client.write(PointKey.ANTILEGIONELLA_DAY, Weekday.SUNDAY) is True
        assert [c.items for c in simulated.received(SETPOINT_WRITE)] == [((0, 194, 7),)]
