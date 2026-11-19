"""Every controller: the model a handshake selects, the rules every model keeps, the points checked
against the manuals, and values through a simulated gateway."""
import csv
import dataclasses
import json
from collections import Counter
from collections.abc import AsyncGenerator, Mapping
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest
from modbus_event_connect import Fixed, Retry, Section, Steps, Within
from modbus_event_connect.micro_nabto import DatapointRegister, RereadZeros, SetpointRegister
from modbus_event_connect.testing import ResolvedModel, assert_models_valid, resolve

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
    Candidate,
    Certainty,
    Client,
    ElectricCoil,
    FilterReplaceInterval,
    MODELS,
    Identity,
    Level,
    Limits,
    MicroNabtoModel,
    ModelError,
    OperationState,
    Point,
    PointKey,
    PollRate,
    Unit,
    Weekday,
    model_points,
    select_model,
)
from nilan_connect._points import (
    alarm_bit,
    choice,
    command,
    reading,
    section,
    setpoint_bit,
    setpoint_reading,
    setting,
    state,
    switch,
    temperature,
)
from nilan_connect.testing import SimulatedMicroNabtoDevice, client_for

DOCS = Path(__file__).parent.parent / "docs" / "models"
EMAIL = "user@example.invalid"
SETPOINT_WRITE = 0x2B


def _cts602(slave_model: int) -> Identity:
    return {"device_model": 1140, "slave_device_number": 2763306, "slave_device_model": slave_model}


VARIANTS: dict[str, tuple[MicroNabtoModel, Identity]] = {
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


def _resolved(variant: str, level: Level = Level.DOCUMENTED) -> ResolvedModel:
    model, identity = VARIANTS[variant]
    return resolve(model, identity, level)


def _points(variant: str, level: Level = Level.DOCUMENTED) -> list[Point[Any]]:
    """Every point of `variant` but the candidates below `level` Test, those left out for their
    certainty included."""
    return list(_resolved(variant, level).points.values())


def _point(variant: str, key: str, level: Level = Level.DOCUMENTED) -> Point[Any]:
    return _resolved(variant, level).point(key)


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


def test_the_models_are_every_model_a_handshake_selects() -> None:
    assert set(MODELS) == {model for model, _ in VARIANTS.values()}
    assert_models_valid(MODELS, identities=[identity for _, identity in VARIANTS.values()])


@pytest.mark.parametrize("model", sorted({name.split("/")[0] for name in VARIANTS}))
def test_each_model_is_valid_for_its_variants(model: str) -> None:
    """Every section of a model must be one some variant has."""
    variants = [VARIANTS[name] for name in VARIANTS if name.split("/")[0] == model]
    assert_models_valid([variants[0][0]], identities=[identity for _, identity in variants])


@pytest.mark.parametrize("model", MODELS, ids=lambda model: model.name)
def test_a_models_points_are_every_point_it_declares_at_any_level(model: MicroNabtoModel) -> None:
    """A model's sections are fixed: none repeats its points per instance."""
    assert all(isinstance(section, Section) for section in model.sections)
    assert {point.key for point in model_points(model)} == model.keys


def test_the_points_of_a_model_with_candidates_hold_them_beside_the_points_they_replace() -> None:
    bypass = [point for point in model_points(OPTIMA_250) if point.key == PointKey.BYPASS_ACTIVE]
    assert [point.candidate for point in bypass] == [None, Candidate(replaces=PointKey.BYPASS_ACTIVE)]
    assert {point.certainty for point in model_points(CTS602)} == set(Certainty)


@pytest.mark.parametrize("model", MODELS, ids=lambda model: model.name)
def test_every_models_readings_are_read_every_10_s_its_settings_every_180_s_and_a_write_read_back_after_1_s(
        model: MicroNabtoModel) -> None:
    assert (model.poll_intervals[PollRate.FAST], model.poll_intervals[PollRate.SLOW]) == (10.0, 180.0)
    assert model.read_back_after == 1.0


def test_only_a_cts400_checks_what_it_scanned_and_does_so_every_900_s() -> None:
    """Whether a CO2 or VOC sensor is fitted can change, so the CTS400 scans for it again."""
    assert {model.name: model.scan_check for model in MODELS} == {
        model.name: PollRate.RARE if model is CTS400 else None for model in MODELS}
    assert {model.name: set(model.poll_intervals) for model in MODELS} == {
        model.name: {PollRate.FAST, PollRate.SLOW, *([PollRate.RARE] if model is CTS400 else [])} for model in MODELS}
    assert CTS400.poll_intervals[PollRate.RARE] == 900.0


@pytest.mark.parametrize("model", MODELS, ids=lambda model: model.name)
def test_only_a_cts400_keeps_a_read_sent_again_open_shorter_than_5_s(model: MicroNabtoModel) -> None:
    assert model.later_answer_wait == (1.0 if model is CTS400 else 5.0)


@pytest.mark.parametrize("model", MODELS, ids=lambda model: model.name)
def test_every_gateway_is_asked_for_64_registers_and_takes_its_zeros_after_7_5_s(model: MicroNabtoModel) -> None:
    assert model.max_registers == 64
    assert model.zeros == RereadZeros(within=7.5, wait=Steps(0.5, then=Fixed(1.0)), at_once=True, halves=True)


@pytest.mark.parametrize("model", MODELS, ids=lambda model: model.name)
def test_every_gateway_is_given_two_seconds_to_answer_a_request_it_has_acknowledged(model: MicroNabtoModel) -> None:
    assert model.answer_wait == 2.0


@pytest.mark.parametrize("model", MODELS, ids=lambda model: model.name)
def test_every_model_sends_a_write_not_taken_again_every_half_second_for_15_s(model: MicroNabtoModel) -> None:
    assert model.write_retry == Retry(Fixed(0.5), Within(15.0))


@pytest.mark.parametrize("model", MODELS, ids=lambda model: model.name)
def test_an_optima_270_and_314_name_0x01_as_a_write_taken_and_every_model_names_0(
        model: MicroNabtoModel) -> None:
    assert model.write_taken == (frozenset({0, 1}) if model in (OPTIMA_270, OPTIMA_314) else frozenset({0}))


@pytest.mark.parametrize("model", MODELS, ids=lambda model: model.name)
def test_every_model_reads_what_follows_a_fan_level_again_3_s_after_it_is_written(model: MicroNabtoModel) -> None:
    variant = next(name for name, (found, _) in VARIANTS.items() if found is model)
    on_write = _point(variant, PointKey.FAN_LEVEL).on_write
    assert on_write is not None and on_write.after == 3.0


def test_every_key_is_declared() -> None:
    declared = {str(key) for key in PointKey.all()}
    assert {point.key for variant in VARIANTS for point in _points(variant)} <= declared


def test_only_the_cts400_the_optima_270_and_four_cts602_temperatures_are_verified() -> None:
    verified = {(variant.split("/")[0], point.key) for variant in VARIANTS for point in _points(variant)
                if point.certainty is Certainty.VERIFIED}
    assert {model for model, _ in verified} == {"CTS400", "OPTIMA_270", "CTS602"}
    assert {key for model, key in verified if model == "CTS602"} == {
        "temp_supply", "temp_extract", "temp_exhaust", "temp_outside"}
    assert all(point.certainty is Certainty.VERIFIED for point in _points("CTS400"))


def test_an_optima_270s_alarm_bits_are_reported_and_its_alarm_words_verified() -> None:
    """A running Optima 270 with no alarm on its panel read an external stop in them
    (HairingX/nilan_connect#31)."""
    bits = {point.key: point.certainty for point in _points("OPTIMA_270") if point.data_type.bit_index is not None}
    assert len(bits) == 23 and set(bits.values()) == {Certainty.REPORTED}
    assert _point("OPTIMA_270", PointKey.ALARM_BITS).certainty is Certainty.VERIFIED
    assert _point("OPTIMA_270", PointKey.ALARM_BITS_HIGH).certainty is Certainty.VERIFIED


@pytest.mark.parametrize(("variant", "key", "expected"), [
    ("CTS602/0", PointKey.TEMP_SUPPLY, Certainty.VERIFIED),
    ("CTS602/0", PointKey.TEMP_ROOM, Certainty.REPORTED),
    ("CTS602/0", PointKey.TEMP_CONTROLLER, Certainty.INFERRED),
    ("CTS602/3", PointKey.TEMP_EXTRACT, Certainty.REPORTED),
    ("CTS602/13", PointKey.TEMP_EXTRACT, Certainty.VERIFIED),
    ("OPTIMA_314", PointKey.TEMP_SUPPLY, Certainty.REPORTED),
])
def test_a_point_is_as_certain_as_its_section_gives_it(variant: str, key: str, expected: Certainty) -> None:
    assert _point(variant, key).certainty is expected


def test_one_point_given_under_two_certainties_in_two_sections_has_each_in_its_own() -> None:
    point = Point(PointKey.TEMP_SUPPLY, read=SetpointRegister(1), poll_rate=PollRate.SLOW)
    verified, inferred = section(verified=[point]), section(inferred=[point])
    assert [p.certainty for p in (*verified.points, *inferred.points)] == [Certainty.VERIFIED, Certainty.INFERRED]


def test_a_point_built_to_replace_another_is_refused_outside_the_candidates() -> None:
    with pytest.raises(ModelError, match="preheat_enable"):
        section(reported=[switch(PointKey.PREHEAT_ENABLE, 16, replaces=PointKey.PREHEAT_ENABLE)])


def test_a_candidate_keeps_the_certainty_it_was_built_with_and_replaces_what_it_was_built_to() -> None:
    new, replacing = section(candidates=[
        switch(PointKey.PREHEAT_ENABLE, 16), state(PointKey.BYPASS_ACTIVE, 107, replaces=PointKey.BYPASS_ACTIVE)]).points
    assert (new.candidate, new.certainty) == (Candidate(), Certainty.REPORTED)
    assert (replacing.candidate, replacing.certainty) == (Candidate(replaces=PointKey.BYPASS_ACTIVE), Certainty.REPORTED)


@pytest.mark.parametrize("built", [
    reading(PointKey.TEMP_SUPPLY, 1, replaces=PointKey.TEMP_SUPPLY),
    temperature(PointKey.TEMP_SUPPLY, 1, scale=0.1, replaces=PointKey.TEMP_SUPPLY),
    state(PointKey.BYPASS_ACTIVE, 1, replaces=PointKey.TEMP_SUPPLY),
    alarm_bit(PointKey.BYPASS_ACTIVE, 1, 0, replaces=PointKey.TEMP_SUPPLY),
    setpoint_reading(PointKey.TEMP_SUPPLY, 1, replaces=PointKey.TEMP_SUPPLY),
    setting(PointKey.TEMP_SUPPLY, 1, None, replaces=PointKey.TEMP_SUPPLY),
    setpoint_bit(PointKey.BYPASS_ACTIVE, 1, 0, replaces=PointKey.TEMP_SUPPLY),
    choice(PointKey.ELECTRIC_COIL, 1, replaces=PointKey.TEMP_SUPPLY),
    switch(PointKey.BYPASS_ACTIVE, 1, replaces=PointKey.TEMP_SUPPLY),
    command(PointKey.BYPASS_ACTIVE, 1, replaces=PointKey.TEMP_SUPPLY),
], ids=["reading", "temperature", "state", "alarm_bit", "setpoint_reading", "setting", "setpoint_bit", "choice",
        "switch", "command"])
def test_every_kind_of_point_can_be_built_to_replace_another(built: Point[Any]) -> None:
    assert built.candidate == Candidate(replaces=PointKey.TEMP_SUPPLY)


def test_a_model_refuses_a_candidate_replacing_a_point_it_does_not_have() -> None:
    """An Optima 301 has no reheat switch."""
    candidate = section(candidates=[switch(PointKey.REHEAT_ENABLE, 16, replaces=PointKey.REHEAT_ENABLE)])
    with pytest.raises(ModelError, match="reheat_enable"):
        dataclasses.replace(OPTIMA_301, sections=(*OPTIMA_301.sections, candidate))


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
            if point.certainty is not Certainty.INFERRED:
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
async def test_a_cts602s_filter_interval_is_one_of_the_manuals_periods(variant: str, address: int) -> None:
    """By its group the setpoint is HR 1105 AirFlow.FiltAlmType: "0: Pressure guard 1: 30 days 2: 90 days ..."."""
    async for client, _ in _client(VARIANTS[variant][1], {}, {address: 2}):
        assert _value(client, PointKey.FILTER_REPLACE_INTERVAL_CHOICE) is FilterReplaceInterval.DAYS_90
        assert not client.has(PointKey.FILTER_REPLACE_INTERVAL)


def test_an_optima_301_neither_reads_nor_writes_its_minimum_air_volume_as_preheat() -> None:
    """Genvex's workbook gives setpoint 20 as "24) Min air volume (%)"; preheat is setpoint 16."""
    at_20 = [point.key for point in _points("OPTIMA_301") if SetpointRegister(20) in (point.read, point.write)]
    assert at_20 == []
    assert PointKey.PREHEAT_ENABLE not in {point.key for point in _points("OPTIMA_301")}


def test_an_optima_301s_cooling_setting_is_3_to_10_c_in_tenths() -> None:
    """Genvex's workbook: 4x0001 "02) Cooling (°C)", 30-100 at a resolution of 0.1."""
    point = _point("OPTIMA_301", PointKey.COOLING_TEMPERATURE)
    assert (point.limits, point.unit, point.scale) == (Limits(3, 10, step=0.1), Unit.CELSIUS, 0.1)


async def test_an_optima_301s_cooling_setting_reads_and_writes_tenths_of_a_degree() -> None:
    async for client, simulated in _client(VARIANTS["OPTIMA_301"][1], {}, {1: 55}):
        assert _value(client, PointKey.COOLING_TEMPERATURE) == pytest.approx(5.5)
        assert await client.write(PointKey.COOLING_TEMPERATURE, 7.0) is True
        assert [c.items for c in simulated.received(SETPOINT_WRITE)] == [((0, 1, 70),)]


@pytest.mark.parametrize("variant", ["OPTIMA_270", "OPTIMA_314"])
async def test_an_optima_270s_and_314s_setpoint_100_is_the_days_since_the_filter_was_changed(variant: str) -> None:
    """The user manual's EF1 counter: two Optima 270s count to about 90 days, then show 250 once a
    change is due (superrob/genvexconnect#52); it is never written."""
    async for client, _ in _client(VARIANTS[variant][1], {}, {100: 250}):
        assert _value(client, PointKey.FILTER_REPLACE_TIME_AGO) == 250
        assert not client.has(PointKey.FILTER_REPLACE_INTERVAL)
    point = _point(variant, PointKey.FILTER_REPLACE_TIME_AGO)
    assert (point.read, point.write, point.unit) == (SetpointRegister(100), None, Unit.DAYS)
    assert point.certainty is Certainty.REPORTED


@pytest.mark.parametrize(("raw", "coil", "reheater", "preheater"), [
    (0, ElectricCoil.NONE, False, False), (1, ElectricCoil.REHEAT, True, False), (2, ElectricCoil.PREHEAT, False, True)])
async def test_an_optima_312s_setpoint_21_is_the_electric_coil_fitted(
        raw: int, coil: ElectricCoil, reheater: bool, preheater: bool) -> None:
    """The user manual's item 25: "0 = No electric heating coil installed, 1 = Electric reheater
    installed, 2 = Electric preheater installed"."""
    async for client, _ in _client(VARIANTS["OPTIMA_312"][1], {}, {21: raw}):
        assert _value(client, PointKey.ELECTRIC_COIL) is coil
        assert _value(client, PointKey.REHEAT_COIL_FITTED) is reheater
        assert _value(client, PointKey.PREHEAT_COIL_FITTED) is preheater


def test_an_optima_312s_electric_coil_is_only_read() -> None:
    """Writing it would tell the controller another coil is installed."""
    at_21 = {point.key: point.write for point in _points("OPTIMA_312") if point.read == SetpointRegister(21)}
    assert at_21 == {PointKey.ELECTRIC_COIL: None, PointKey.REHEAT_COIL_FITTED: None,
                     PointKey.PREHEAT_COIL_FITTED: None}


@pytest.mark.parametrize(("variant", "address"), [("OPTIMA_301", 4), ("OPTIMA_312", 4), ("OPTIMA_314", 65)])
def test_an_optimas_sensor_t5_is_the_air_before_the_evaporator(variant: str, address: int) -> None:
    """The Optima 312's user manual: "T5 Before cooling coil, T6 Cooling coil"."""
    at_t5 = [point.key for point in _points(variant) if point.read == DatapointRegister(address)]
    assert at_t5 == [PointKey.TEMP_BEFORE_EVAPORATOR]


@pytest.mark.parametrize("variant", ["OPTIMA_301", "OPTIMA_312"])
def test_an_optimas_sensor_t2_is_the_room_at_its_panel(variant: str) -> None:
    """Genvex's workbook: 3x0009 "T2 Panel"."""
    at_9 = [point.key for point in _points(variant) if point.read == DatapointRegister(9)]
    assert at_9 == [PointKey.TEMP_ROOM_PANEL]


def test_an_optima_314s_datapoint_24_is_the_hot_water_tanks_bottom() -> None:
    """The user manual calls sensor T8 the tank bottom."""
    at_24 = [point.key for point in _points("OPTIMA_314") if point.read == DatapointRegister(24)]
    assert at_24 == [PointKey.TEMP_HOTWATER_BOTTOM]


# ================================================================== levels and candidates

POINTS: dict[str, dict[str, str]] = json.loads((Path(__file__).parent / "points.json").read_text(encoding="utf-8"))
"""Every point of each variant, by key, as it was before the first candidate, inferred ones included."""

CANDIDATES: dict[str, dict[str, str]] = {
    "OPTIMA_250": {"bypass_active": "reported DatapointRegister(address=107, obj=0) None DataType.BOOL x1+0"},
    "OPTIMA_251": {"bypass_active": "reported DatapointRegister(address=107, obj=0) None DataType.BOOL x1+0"},
    "OPTIMA_301": {
        "preheat_enable": "reported SetpointRegister(address=16, obj=0) SetpointRegister(address=16, obj=0) "
                          "DataType.BOOL x1+0",
        "min_air_volume": "reported SetpointRegister(address=20, obj=0) SetpointRegister(address=20, obj=0) "
                          "DataType.UINT16 x1+0",
    },
}
"""What each variant's candidates put in place at the Test level."""


def _described(point: Point[Any]) -> str:
    return f"{point.certainty} {point.read!r} {point.write!r} {point.data_type} x{point.scale:g}{point.offset:+g}"


def _used(variant: str, level: Level) -> dict[str, str]:
    return {key: _described(point) for key, point in _resolved(variant, level).used.items()}


@pytest.mark.parametrize("level", [Level.VERIFIED, Level.DOCUMENTED])
@pytest.mark.parametrize("variant", sorted(VARIANTS))
def test_below_the_test_level_a_variant_has_the_points_it_had_before_the_candidates_that_the_level_admits(
        variant: str, level: Level) -> None:
    assert _used(variant, level) == {
        key: described for key, described in POINTS[variant].items() if level.admits(Certainty(described.split()[0]))}


@pytest.mark.parametrize("variant", sorted(VARIANTS))
def test_at_the_test_level_a_variant_has_every_point_it_had_with_its_candidates_in_place(variant: str) -> None:
    assert _used(variant, Level.TEST) == {**POINTS[variant], **CANDIDATES.get(variant, {})}


def test_the_candidates_are_those_read_on_no_unit_whose_registers_genvexs_workbook_gives() -> None:
    found = {variant: {key: point.candidate.replaces for key, point in _resolved(variant, Level.TEST).used.items()
                       if point.candidate is not None} for variant in VARIANTS}
    assert {variant: candidates for variant, candidates in found.items() if candidates} == {
        "OPTIMA_250": {"bypass_active": PointKey.BYPASS_ACTIVE},
        "OPTIMA_251": {"bypass_active": PointKey.BYPASS_ACTIVE},
        "OPTIMA_301": {"preheat_enable": None, "min_air_volume": None},
    }


@pytest.mark.parametrize("variant", ["OPTIMA_250", "OPTIMA_251"])
async def test_at_the_test_level_an_optima_250s_bypass_is_open_by_its_on_off_datapoint_107(variant: str) -> None:
    """Genvex's workbook: 3x0107 "Bypass ON/OFF"; 3x0104 is the bypass's opening, 0-100 %."""
    async for client, _ in _client(VARIANTS[variant][1], {104: 63, 107: 0}, {}, Level.TEST):
        assert _value(client, PointKey.BYPASS_ACTIVE) is False
        assert _value(client, PointKey.BYPASS_POSITION) == 63
    async for client, _ in _client(VARIANTS[variant][1], {104: 63, 107: 0}, {}):
        assert _value(client, PointKey.BYPASS_ACTIVE) is True


async def test_at_the_test_level_an_optima_301_reads_and_writes_its_preheat_at_setpoint_16() -> None:
    """Genvex's workbook: 4x0016 "20) Preheat (on/off)"."""
    async for client, simulated in _client(VARIANTS["OPTIMA_301"][1], {}, {16: 1}, Level.TEST):
        assert _value(client, PointKey.PREHEAT_ENABLE) is True
        assert await client.write(PointKey.PREHEAT_ENABLE, False) is True
        assert [c.items for c in simulated.received(SETPOINT_WRITE)] == [((0, 16, 0),)]


async def test_at_the_test_level_an_optima_301_reads_and_writes_its_minimum_air_volume_at_setpoint_20() -> None:
    """Genvex's workbook: 4x0020 "24) Min air volume (%)", 0-100."""
    async for client, simulated in _client(VARIANTS["OPTIMA_301"][1], {}, {20: 30}, Level.TEST):
        assert _value(client, PointKey.MIN_AIR_VOLUME) == 30
        assert client.points[PointKey.MIN_AIR_VOLUME].limits == Limits(0, 100, step=1)
        assert await client.write(PointKey.MIN_AIR_VOLUME, 40) is True
        assert [c.items for c in simulated.received(SETPOINT_WRITE)] == [((0, 20, 40),)]


async def test_below_the_test_level_an_optima_301_has_neither_preheat_nor_a_minimum_air_volume() -> None:
    async for client, _ in _client(VARIANTS["OPTIMA_301"][1], {}, {16: 1, 20: 30}):
        assert not client.has(PointKey.PREHEAT_ENABLE) and not client.has(PointKey.MIN_AIR_VOLUME)


# =================================================================== through a simulated gateway


async def _client(identity: Mapping[str, Any], datapoints: dict[int, int], setpoints: dict[int, int],
                  level: Level = Level.DOCUMENTED) -> AsyncGenerator[tuple[Client, SimulatedMicroNabtoDevice], None]:
    simulated = SimulatedMicroNabtoDevice(
        emails=frozenset({EMAIL}), identity={**HANDSHAKE_ZEROS, **identity},
        datapoint_registers={(0, a): v for a, v in datapoints.items()},
        setpoint_registers={(0, a): v for a, v in setpoints.items()})
    async with simulated:
        client = client_for(simulated, email=EMAIL, timeout=0.2, retries=1, level=level)
        await client.connect()
        try:
            yield client, simulated
        finally:
            await client.disconnect()


def _value(client: Client, key: Any) -> object:
    current = client.value(key)
    return None if current is None else current.value


@pytest.mark.parametrize("variant", sorted(VARIANTS))
async def test_every_point_a_client_has_is_as_certain_as_its_model_gives_it(variant: str) -> None:
    every_register = {address: 0 for address in range(300)}
    async for client, _ in _client(VARIANTS[variant][1], every_register, every_register):
        assert client.points
        model = {point.key: point.certainty for point in _points(variant)}
        assert {key: point.certainty for key, point in client.points.items()} == {
            key: model[key] for key in client.points}


async def test_an_optima_reads_its_offset_temperatures_and_writes_where_it_takes_writes() -> None:
    async for client, simulated in _client(VARIANTS["OPTIMA_270"][1], {20: 500}, {1: 110}):
        assert _value(client, PointKey.TEMP_SUPPLY) == pytest.approx(20.0)
        assert _value(client, PointKey.TEMP_TARGET) == pytest.approx(21.0)
        assert await client.write(PointKey.TEMP_TARGET, 22.0) is True
        assert [c.items for c in simulated.received(SETPOINT_WRITE)] == [((0, 12, 120),)]


async def test_a_write_an_optima_270s_gateway_answers_0x01_is_taken_and_not_sent_again() -> None:
    """An Optima 270's gateway answered 0x01 to every write it took."""
    async for client, simulated in _client(VARIANTS["OPTIMA_270"][1], {}, {1: 110}):
        simulated.write_taken = frozenset({1})
        simulated.write_statuses = [1]
        assert await client.write(PointKey.TEMP_TARGET, 22.0) is True
        assert [c.items for c in simulated.received(SETPOINT_WRITE)] == [((0, 12, 120),)]


async def test_a_write_an_optima_314s_gateway_answers_0x01_is_taken_and_not_sent_again() -> None:
    async for client, simulated in _client(VARIANTS["OPTIMA_314"][1], {}, {1: 110}):
        simulated.write_taken = frozenset({1})
        simulated.write_statuses = [1]
        assert await client.write(PointKey.TEMP_TARGET, 22.0) is True
        assert len(simulated.received(SETPOINT_WRITE)) == 1


@pytest.mark.parametrize(("variant", "address"), [
    ("OPTIMA_250", 104), ("OPTIMA_251", 104), ("OPTIMA_301", 104), ("OPTIMA_312", 104), ("OPTIMA_260", 11)])
async def test_an_optimas_bypass_opening_is_read_in_percent_beside_whether_it_is_open(
        variant: str, address: int) -> None:
    """Genvex's workbook gives the register as the bypass's opening, 0-100 %."""
    async for client, _ in _client(VARIANTS[variant][1], {address: 63}, {}):
        assert _value(client, PointKey.BYPASS_POSITION) == 63
        assert _value(client, PointKey.BYPASS_ACTIVE) is True
    assert _point(variant, PointKey.BYPASS_POSITION).unit is Unit.PERCENT


@pytest.mark.parametrize(("slave_model", "address"), [(13, 34), (3, 41)])
async def test_a_cts602_reads_its_extract_air_where_its_variant_has_it(slave_model: int, address: int) -> None:
    async for client, _ in _client(_cts602(slave_model), {address: 2150}, {}):
        assert _value(client, PointKey.TEMP_EXTRACT) == pytest.approx(21.5)


async def test_a_cts602_lights_supply_air_is_read_after_its_heater() -> None:
    """By its group, gateway 37 is IR 207 Input.T7_Inlet, "Inlet temperature (after heater)"; the
    Light's manual lists no T2."""
    async for client, _ in _client(VARIANTS["CTS602_LIGHT"][1], {37: 2150}, {}):
        assert _value(client, PointKey.TEMP_SUPPLY_AFTER_HEATER) == pytest.approx(21.5)
        assert not client.has(PointKey.TEMP_SUPPLY)


async def test_an_inferred_alarm_status_is_the_bit_the_manual_names_for_an_active_alarm() -> None:
    async for client, _ in _client(VARIANTS["CTS602_LIGHT"][1], {63: 0x80}, {}, Level.TEST):
        assert _value(client, PointKey.ALARM_STATUS) is True


async def test_an_inferred_alarms_time_is_its_dos_date_and_time() -> None:
    date_word, time_word = (46 << 9) | (9 << 5) | 29, (13 << 11) | (37 << 5) | 21
    async for client, _ in _client(VARIANTS["CTS602/0"][1], {66: date_word, 67: time_word}, {}, Level.TEST):
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


async def test_a_heat_pump_states_code_is_kept_beside_the_state_it_means() -> None:
    """Codes 6 and 10 both mean the heat pump has stopped; only the code tells them apart."""
    async for client, _ in _client(VARIANTS["CTS602/44"][1], {198: 10}, {}):
        assert _value(client, PointKey.HEAT_PUMP_STATE_CODE) == 10
        assert _value(client, PointKey.HEAT_PUMP_STATE) is OperationState.HEAT_PUMP_STOP


def test_heat_pump_states_that_share_a_text_are_one_state() -> None:
    heat_pump = _point("CTS602/44", PointKey.HEAT_PUMP_STATE)
    assert heat_pump.codes is not None
    assert heat_pump.codes[6] is heat_pump.codes[10] is OperationState.HEAT_PUMP_STOP


async def test_a_cts602s_electric_hot_water_supplement_is_a_switch() -> None:
    """HR 1704 HotWater.HeatType: "Use of electricity supplement: 0=OFF, 1=El"."""
    async for client, simulated in _client(VARIANTS["CTS602/9"][1], {}, {193: 1}, Level.TEST):
        assert _value(client, PointKey.HOTWATER_HEATER_ENABLE) is True
        assert await client.write(PointKey.HOTWATER_HEATER_ENABLE, False) is True
        assert [c.items for c in simulated.received(SETPOINT_WRITE)] == [((0, 193, 0),)]


async def test_a_weekday_is_numbered_as_the_manual_numbers_it() -> None:
    """HotWater.LegioType: "0=OFF, 1=Mandag, ..., 7=sondag"."""
    async for client, simulated in _client(VARIANTS["CTS602/9"][1], {}, {194: 1}, Level.TEST):
        assert _value(client, PointKey.ANTILEGIONELLA_DAY) is Weekday.MONDAY
        assert await client.write(PointKey.ANTILEGIONELLA_DAY, Weekday.SUNDAY) is True
        assert [c.items for c in simulated.received(SETPOINT_WRITE)] == [((0, 194, 7),)]
