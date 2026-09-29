"""Every controller: the model a handshake selects, the rules every model keeps, the points checked
against the manuals, and values through a simulated gateway."""
import csv
from collections import Counter
from collections.abc import AsyncGenerator, Mapping
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest
from modbus_event_connect import Client, Identity, Model, Point
from modbus_event_connect.micro_nabto import (
    DatapointRegister,
    MicroNabtoConnection,
    MicroNabtoDevice,
    SetpointRegister,
)
from modbus_event_connect.testing import assert_models_valid, resolve

from nilan_connect import (
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
    Alarm,
    Certainty,
    FilterChangeAlarm,
    OperationState,
    PointKey,
    Weekday,
    certainty,
    select_model,
)
from nilan_connect._certainty import section
from nilan_connect.testing import SimulatedMicroNabtoDevice

DOCS = Path(__file__).parent.parent / "docs" / "models"
EMAIL = "user@example.invalid"
SETPOINT_WRITE = 0x2B


def _cts602(slave_model: int) -> Identity:
    return {"device_model": 1140, "slave_device_number": 2763306, "slave_device_model": slave_model}


VARIANTS: dict[str, tuple[Model, Identity]] = {
    "CTS400": (CTS400, {"device_model": 1140, "slave_device_number": 72270, "slave_device_model": 1}),
    **{f"CTS602/{n}": (CTS602, _cts602(n)) for n in (0, 3, 9, 13, 20, 23, 44, 144, 244)},
    "CTS602_LIGHT": (CTS602_LIGHT, _cts602(2)),
    "OPTIMA_250": (OPTIMA_250, {"device_model": 1040, "slave_device_number": 79250, "slave_device_model": 1}),
    "OPTIMA_251": (OPTIMA_251, {"device_model": 1040, "slave_device_number": 79250, "slave_device_model": 8}),
    "OPTIMA_260": (OPTIMA_260, {"device_model": 1040, "slave_device_number": 70810, "slave_device_model": 26}),
    "OPTIMA_270": (OPTIMA_270, {"device_model": 2010, "device_number": 79265}),
    "OPTIMA_301": (OPTIMA_301, {"device_model": 1040, "slave_device_number": 79250, "slave_device_model": 5}),
    "OPTIMA_312": (OPTIMA_312, {"device_model": 1040, "slave_device_number": 79250, "slave_device_model": 9}),
    "OPTIMA_314": (OPTIMA_314, {"device_model": 2020, "device_number": 79280}),
}
"""A handshake of each controller, and of each CTS602 variant its sections tell apart."""

GROUP_STARTS: dict[str, dict[tuple[str, int], int]] = {
    "CTS602": {("IR", 200): 31, ("IR", 400): 64, ("IR", 1000): 84, ("IR", 1100): 98, ("HR", 1000): 136,
             ("HR", 1100): 154, ("HR", 1200): 170, ("HR", 1700): 189, ("HR", 1800): 201},
    "CTS602_LIGHT": {("IR", 200): 30, ("IR", 400): 63, ("IR", 1000): 83, ("IR", 1100): 97, ("HR", 1000): 132,
                   ("HR", 1100): 148},
}
"""The gateway address of the first register of each of a manual's groups, by controller."""

MANUALS: dict[str, tuple[str, ...]] = {
    "CTS602": ("nilan-cts602", "nilan-cts602-hmi350t"), "CTS602_LIGHT": ("nilan-cts602-light",)}

HANDSHAKE_ZEROS = {"device_number": 0, "device_model": 0, "slave_device_number": 0, "slave_device_model": 0}
"""What a simulated gateway's handshake says for a number the test does not care about."""


def _points(variant: str) -> list[Point[Any]]:
    return list(resolve(*VARIANTS[variant]).points.values())


def _point(variant: str, key: str) -> Point[Any]:
    return resolve(*VARIANTS[variant]).point(key)


def _manual(folder: str) -> dict[tuple[str, int], dict[str, str]]:
    with (DOCS / folder / "registers.csv").open(encoding="utf-8") as rows:
        return {(row["table"], int(row["address"])): row for row in csv.DictReader(rows)}


# ============================================================================== selection


@pytest.mark.parametrize("variant", sorted(VARIANTS))
def test_a_handshake_selects_its_model(variant: str) -> None:
    model, identity = VARIANTS[variant]
    assert select_model(identity) is model


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


# ================================================================================== rules


@pytest.mark.parametrize("model", sorted({name.split("/")[0] for name in VARIANTS}))
def test_each_model_is_valid_for_its_variants(model: str) -> None:
    """Every section of a model must be one some variant has."""
    variants = [VARIANTS[name] for name in VARIANTS if name.split("/")[0] == model]
    assert_models_valid(variants[0][0], identities=[identity for _, identity in variants])


def test_every_key_is_declared() -> None:
    declared = {str(key) for key in PointKey.all()}
    assert {point.key for variant in VARIANTS for point in _points(variant)} <= declared


@pytest.mark.parametrize("variant", sorted(VARIANTS))
def test_every_point_has_a_certainty(variant: str) -> None:
    assert all(certainty(point) in Certainty for point in _points(variant))


def test_only_the_cts400_the_optima_270_and_four_cts602_temperatures_are_verified() -> None:
    verified = {(variant.split("/")[0], point.key) for variant in VARIANTS for point in _points(variant)
                if certainty(point) is Certainty.VERIFIED}
    assert {model for model, _ in verified} == {"CTS400", "OPTIMA_270", "CTS602"}
    assert {key for model, key in verified if model == "CTS602"} == {
        "temp_supply", "temp_extract", "temp_exhaust", "temp_outside"}
    assert all(certainty(point) is Certainty.VERIFIED for point in _points("CTS400"))


def test_a_point_given_two_certainties_is_refused() -> None:
    point = Point(PointKey.TEMP_SUPPLY, read=SetpointRegister(1))
    section(verified=[point])
    with pytest.raises(ValueError, match="both"):
        section(inferred=[point])


def test_a_point_of_no_model_has_no_certainty() -> None:
    with pytest.raises(KeyError):
        certainty(Point(PointKey.TEMP_SUPPLY, read=SetpointRegister(1)))


@pytest.mark.parametrize("variant", sorted(VARIANTS))
def test_no_two_keys_are_written_to_one_register(variant: str) -> None:
    written = Counter((type(point.write).__name__, point.write.address)
                      for point in _points(variant) if point.write is not None)
    assert [register for register, count in written.items() if count > 1] == []


# =========================================================================== against the manuals


@pytest.mark.parametrize("point", _points("CTS400"), ids=lambda point: point.key)
def test_a_cts400_point_is_its_register_as_the_manual_gives_it(point: Point[Any]) -> None:
    """A CTS400 is read at its manual's own addresses."""
    access = point.read or point.write
    assert access is not None
    row = _manual("nilan-cts400")[("HR" if isinstance(access, SetpointRegister) else "IR", access.address)]
    decimals = int(row["decimals"] or 0)
    assert point.scale == pytest.approx(10 ** -decimals)
    assert (point.data_type.kind.name == "INT16") == row["data_type"].startswith("Signed")
    manual_range = None if not row["min"] else (int(row["min"]) * 10 ** -decimals, int(row["max"]) * 10 ** -decimals)
    if point.writable and point.key.type is bool:
        assert manual_range in (None, (0, 1))
    elif point.writable and point.states:
        assert manual_range is not None
        assert all(manual_range[0] <= state <= manual_range[1] for state in point.states)
    elif point.writable:
        assert point.limits is not None and manual_range is not None
        assert (point.limits.min, point.limits.max) == pytest.approx(manual_range)


@pytest.mark.parametrize("model", sorted(GROUP_STARTS))
def test_an_inferred_address_is_a_manual_register_placed_by_its_group(model: str) -> None:
    """Within one of a manual's groups the gateway keeps the manual's order and spacing."""
    documented = {register for folder in MANUALS[model] for register in _manual(folder)}
    placed = {(table, start + address - base): address
              for (table, base), start in GROUP_STARTS[model].items()
              for table_, address in documented if table_ == table and address // 100 * 100 == base}
    for variant in (name for name in VARIANTS if name.split("/")[0] == model):
        for point in _points(variant):
            if certainty(point) is not Certainty.INFERRED:
                continue
            assert point.read is not None
            table = "HR" if isinstance(point.read, SetpointRegister) else "IR"
            assert (table, point.read.address) in placed, point.key


# =============================================================================== decisions


@pytest.mark.parametrize("variant", ["CTS602/0", "CTS602/244", "CTS602_LIGHT"])
def test_a_cts602_has_no_filter_reset(variant: str) -> None:
    """None of the three CTS602 manuals documents one, and the address found elsewhere is untested."""
    assert PointKey.FILTER_REPLACE_RESET not in {point.key for point in _points(variant)}


@pytest.mark.parametrize("variant", ["CTS602/0", "CTS602/244"])
def test_a_cts602_has_no_damper_test_day(variant: str) -> None:
    """Its two manuals number HR 1102 differently: 1 is "Wednesday 0400" in one, Monday in the other."""
    assert PointKey.DAMPER_TEST_DAY not in {point.key for point in _points(variant)}


def test_the_damper_test_day_is_only_read_as_choosing_one_cannot_be_undone() -> None:
    assert _point("CTS602_LIGHT", PointKey.DAMPER_TEST_DAY).write is None


@pytest.mark.parametrize(("variant", "address"), [("CTS602/0", 159), ("CTS602_LIGHT", 153)])
async def test_a_cts602s_filter_alarm_period_is_one_of_the_manuals_periods(variant: str, address: int) -> None:
    """By its group the setpoint is HR 1105 AirFlow.FiltAlmType: "0: Pressure guard 1: 30 days 2: 90 days ..."."""
    async for client, _ in _client(VARIANTS[variant][1], {}, {address: 2}):
        assert _value(client, PointKey.FILTER_CHANGE_ALARM) is FilterChangeAlarm.DAYS_90
        assert not client.has(PointKey.FILTER_REPLACE_INTERVAL)


def test_an_optima_314s_datapoint_24_is_the_hot_water_tanks_bottom() -> None:
    """The user manual calls sensor T8 the tank bottom."""
    at_24 = [point.key for point in _points("OPTIMA_314") if point.read == DatapointRegister(24)]
    assert at_24 == [PointKey.TEMP_HOTWATER_BOTTOM]


# =================================================================== through a simulated gateway


async def _client(identity: Mapping[str, Any], datapoints: dict[int, int],
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


@pytest.mark.parametrize("variant", sorted(VARIANTS))
async def test_every_point_a_client_has_has_a_certainty(variant: str) -> None:
    """A certainty is found by the point itself, so the client must hand out the model's points."""
    every_register = {address: 0 for address in range(300)}
    async for client, _ in _client(VARIANTS[variant][1], every_register, every_register):
        assert client.points
        assert all(certainty(point) in Certainty for point in client.points.values())


async def test_an_optima_reads_its_offset_temperatures_and_writes_where_it_takes_writes() -> None:
    async for client, simulated in _client(VARIANTS["OPTIMA_270"][1], {20: 500}, {1: 110}):
        assert _value(client, PointKey.TEMP_SUPPLY) == pytest.approx(20.0)
        assert _value(client, PointKey.TEMP_TARGET) == pytest.approx(21.0)
        assert await client.write(PointKey.TEMP_TARGET, 22.0) is True
        assert [c.items for c in simulated.received(SETPOINT_WRITE)] == [((0, 12, 120),)]


@pytest.mark.parametrize(("slave_model", "address"), [(13, 34), (3, 41)])
async def test_a_cts602_reads_its_extract_air_where_its_variant_has_it(slave_model: int, address: int) -> None:
    async for client, _ in _client(_cts602(slave_model), {address: 2150}, {}):
        assert _value(client, PointKey.TEMP_EXTRACT) == pytest.approx(21.5)


async def test_an_inferred_alarm_status_is_the_bit_the_manual_names_for_an_active_alarm() -> None:
    async for client, _ in _client(VARIANTS["CTS602_LIGHT"][1], {63: 0x80}, {}):
        assert _value(client, PointKey.ALARM_STATUS) is True


async def test_an_inferred_alarms_time_is_its_dos_date_and_time() -> None:
    date_word, time_word = (46 << 9) | (9 << 5) | 29, (13 << 11) | (37 << 5) | 21
    async for client, _ in _client(VARIANTS["CTS602/0"][1], {66: date_word, 67: time_word}, {}):
        assert _value(client, PointKey.ALARM_1_TIME) == datetime(2026, 9, 29, 13, 37, 42)


# =============================================================================== shared states


def test_the_same_alarm_is_one_state_whichever_code_a_controller_gives_it() -> None:
    """A CTS400 calls its filter alarm 1, a CTS602 19; to a CTS602, 1 is a hardware fault."""
    cts400_alarm = _point("CTS400", PointKey.ALARM_1)
    assert cts400_alarm.codes is not None and cts400_alarm.codes[1] is Alarm.CHANGE_FILTER
    cts602_alarm = _point("CTS602/0", PointKey.ALARM_1)
    assert cts602_alarm.codes is not None
    assert cts602_alarm.codes[19] is Alarm.CHANGE_FILTER and cts602_alarm.codes[1] is Alarm.HARDWARE


async def test_an_alarm_code_stays_the_code_and_its_alarm_is_a_key_of_its_own() -> None:
    async for client, _ in _client(VARIANTS["CTS602/0"][1], {65: 19}, {}):
        assert _value(client, PointKey.ALARM_1_CODE) == 19
        assert _value(client, PointKey.ALARM_1) is Alarm.CHANGE_FILTER


async def test_an_optimas_alarm_bits_are_alarms_of_their_own_with_the_filter_as_filter_ok() -> None:
    async for client, _ in _client(VARIANTS["OPTIMA_270"][1], {114: 0b11, 115: 1 << 6}, {}):
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
    async for client, simulated in _client(VARIANTS["CTS602/9"][1], {}, {194: 1}):
        assert _value(client, PointKey.ANTILEGIONELLA_DAY) is Weekday.MONDAY
        assert await client.write(PointKey.ANTILEGIONELLA_DAY, Weekday.SUNDAY) is True
        assert [c.items for c in simulated.received(SETPOINT_WRITE)] == [((0, 194, 7),)]
