"""Nilan's and Genvex's controllers as models: every point's key, where each point's address
comes from, and the CTS400's registers.

Sources:
    Nilan, "Protocol description Nilan CTS400 Modbus version 1.0", doc. version 1.10,
    22-08-2024: the addresses, decimals, data types and limits of every CTS400 register.
    Nilan, "Software instructions Comfort CTS400" (S75), version 1.30, 20-01-2025: the sensors,
    T1 outdoor, T2 supply, T3 extract and T4 discharge air.
    Both are in this repository's docs/models/nilan-cts400.

Over micro_nabto a CTS400 is read at the manual's own addresses: the datapoints are its input
registers, the setpoints its holding registers.
"""
from __future__ import annotations

from collections.abc import Callable, Collection, Sequence
from dataclasses import replace
from typing import Any

from modbus_event_connect import (
    DataType,
    Identity,
    Key,
    Limits,
    Model,
    Point,
    PollRate,
    Refresh,
    Section,
    Transform,
    Transforms,
    Unit,
    WriteKind,
)
from modbus_event_connect.micro_nabto import DatapointRegister, MicroNabtoOptions, SetpointRegister

# ================================================================================== keys
#
# Every point has its key here, with the type of its value. A consumer's stored entities are
# built on the key strings, so they never change.


def _members[K](namespace: type, kind: type[K]) -> tuple[K, ...]:
    return tuple(value for value in vars(namespace).values() if isinstance(value, kind))


class PointKey:
    """The key of each point a Nilan or Genvex controller can have."""
    ALARM_1_CODE = Key("alarm_1_code", int)
    ALARM_2_CODE = Key("alarm_2_code", int)
    ALARM_3_CODE = Key("alarm_3_code", int)
    ALARM_1_INFO = Key("alarm_1_info", int)
    ALARM_2_INFO = Key("alarm_2_info", int)
    ALARM_3_INFO = Key("alarm_3_info", int)
    ALARM_STATUS = Key("alarm_status", bool)
    """True while an alarm is active."""
    BYPASS_ACTIVE = Key("bypass_active", bool)
    """True while the bypass damper is open."""
    CO2_LEVEL = Key("co2_level", int)
    DEFROST_ACTIVE = Key("defrost_active", bool)
    FAN_DUTYCYCLE_EXTRACT = Key("fan_dutycycle_extract", float)
    FAN_DUTYCYCLE_SUPPLY = Key("fan_dutycycle_supply", float)
    FAN_LEVEL_CURRENT = Key("fan_level_current", int)
    """The fan level currently active."""
    FILTER_OK = Key("filter_ok", bool)
    """False when the filter must be changed."""
    FILTER_REPLACE_TIME_AGO = Key("filter_replace_time_ago", float)
    FILTER_REPLACE_TIME_REMAIN = Key("filter_replace_time_remain", int)
    HUMIDITY = Key("humidity", float)
    HUMIDITY_AVG = Key("humidity_average", float)
    HUMIDITY_HIGH_ACTIVE = Key("humidity_high_active", bool)
    """The CTS400's "average level humidity 24 hours OK", the other way round."""
    HUMIDITY_HIGH_LEVEL = Key("humidity_high_level", float)
    HUMIDITY_HIGH_LEVEL_TIME = Key("humidity_high_level_time", float)
    """How long the high humidity function has been active."""
    TEMP_EXHAUST = Key("temp_exhaust", float)
    """Air leaving the unit to the outside."""
    TEMP_EXTRACT = Key("temp_extract", float)
    """Air taken from the rooms into the unit."""
    TEMP_OUTSIDE = Key("temp_outside", float)
    TEMP_SUPPLY = Key("temp_supply", float)
    """Air supplied to the rooms."""
    VOC_LEVEL = Key("voc_level", int)
    WINTER_MODE_ACTIVE = Key("winter_mode_active", bool)

    ALARM_RESET = Key("alarm_reset", bool)
    CO2_THRESHOLD = Key("co2_threshold", int)
    DEFROST_BREAK_TIME = Key("defrost_break_time", int)
    DEFROST_MAX_TIME = Key("defrost_max_time", int)
    ENABLE = Key("enable", bool)
    """True while the unit runs."""
    FAN_LEVEL = Key("fan_level", int)
    FAN_LEVEL_HIGH_CO2 = Key("fan_level_high_co2", int)
    FAN_LEVEL_HIGH_HUMIDITY = Key("fan_level_high_humidity", int)
    FAN_LEVEL_HIGH_HUMIDITY_TIME = Key("fan_level_high_humidity_time", int)
    FAN_LEVEL_LOW_HUMIDITY = Key("fan_level_low_humidity", int)
    FAN_LEVEL1_EXTRACT_PRESET = Key("fan_level1_extract_preset", float)
    FAN_LEVEL1_SUPPLY_PRESET = Key("fan_level1_supply_preset", float)
    FAN_LEVEL2_EXTRACT_PRESET = Key("fan_level2_extract_preset", float)
    FAN_LEVEL2_SUPPLY_PRESET = Key("fan_level2_supply_preset", float)
    FAN_LEVEL3_EXTRACT_PRESET = Key("fan_level3_extract_preset", float)
    FAN_LEVEL3_SUPPLY_PRESET = Key("fan_level3_supply_preset", float)
    FAN_LEVEL4_EXTRACT_PRESET = Key("fan_level4_extract_preset", float)
    FAN_LEVEL4_SUPPLY_PRESET = Key("fan_level4_supply_preset", float)
    FILTER_REPLACE_INTERVAL = Key("filter_replace_interval", int)
    FILTER_REPLACE_RESET = Key("filter_replace_reset", bool)
    HUMIDITY_LOW_THRESHOLD = Key("humidity_low_threshold", float)
    TEMP_DEFROST_HIGH_THRESHOLD = Key("temp_defrost_high_threshold", float)
    """Defrosting stops above this discharge air temperature."""
    TEMP_DEFROST_LOW_THRESHOLD = Key("temp_defrost_low_threshold", float)
    """Defrosting starts below this discharge air temperature."""
    TEMP_REGULATION_DEAD_BAND = Key("temp_regulation_dead_band", float)
    TEMP_SUPPLY_MAX = Key("temp_supply_max", float)
    TEMP_SUPPLY_MIN = Key("temp_supply_min", float)
    TEMP_TARGET = Key("temp_target", float)
    TEMP_WINTER_MODE_THRESHOLD = Key("temp_winter_mode_threshold", float)
    """Winter below this outdoor temperature, summer above it."""
    VOC_THRESHOLD = Key("voc_threshold", int)

    AIR_EXCHANGE_MODE = Key("air_exchange_mode", int)
    ALARM_1_DATE = Key("alarm_1_date", int)
    ALARM_1_TIME = Key("alarm_1_time", int)
    ALARM_2_DATE = Key("alarm_2_date", int)
    ALARM_2_TIME = Key("alarm_2_time", int)
    ALARM_3_DATE = Key("alarm_3_date", int)
    ALARM_3_TIME = Key("alarm_3_time", int)
    ALARM_BITS = Key("alarm_bits", int)
    ALARM_BITS_HIGH = Key("alarm_bits_high", int)
    ANTILEGIONELLA_DAY = Key("antilegionella_day", int)
    BOOST_ENABLE = Key("boost_enable", bool)
    BOOST_TIME = Key("boost_time", int)
    BYPASS_FAN_LEVEL = Key("bypass_fan_level", int)
    BYPASS_POSITION = Key("bypass_position", int)
    BYPASS_TURNOFF = Key("bypass_turnoff", int)
    CENTRAL_HEAT_CURVE = Key("central_heat_curve", int)
    CENTRAL_HEAT_PUMP_MODE = Key("central_heat_pump_mode", int)
    CENTRAL_HEAT_REGULATION_TIME = Key("central_heat_regulation_time", int)
    CENTRAL_HEAT_SELECT = Key("central_heat_select", int)
    CENTRAL_HEAT_TYPE = Key("central_heat_type", int)
    CO2_LEVEL_CALCULATED = Key("co2_level_calculated", int)
    COMPRESSOR_PRIORITY = Key("compressor_priority", bool)
    CONTROL_SENSOR = Key("control_sensor", int)
    COOLING_ENABLE = Key("cooling_enable", bool)
    DAMPER_TEST_DAY = Key("damper_test_day", int)
    DAMPER_TEST_LAST_DATE = Key("damper_test_last_date", int)
    DAMPER_TEST_STATE = Key("damper_test_state", int)
    DISCHARGE_PRESSURE = Key("discharge_pressure", int)
    FACTORY_PRESET = Key("factory_preset", int)
    FAN_LEVEL_COOLING = Key("fan_level_cooling", int)
    FAN_LEVEL_EXTRACT = Key("fan_level_extract", int)
    FAN_LEVEL_SUPPLY = Key("fan_level_supply", int)
    FAN_RPM_EXTRACT = Key("fan_rpm_extract", int)
    FAN_RPM_SUPPLY = Key("fan_rpm_supply", int)
    HEAT_PUMP_ACTIVE = Key("heat_pump_active", bool)
    HEAT_PUMP_CAPACITY = Key("heat_pump_capacity", float)
    HEAT_PUMP_HEATER_ACTIVE = Key("heat_pump_heater_active", bool)
    HEAT_PUMP_ROOM_HEATING = Key("heat_pump_room_heating", bool)
    HEAT_PUMP_STATE = Key("heat_pump_state", int)
    HEAT_PUMP_WATER_HEATING = Key("heat_pump_water_heating", bool)
    HEAT_SOURCE = Key("heat_source", int)
    HOTWATER_HEAT_TYPE = Key("hotwater_heat_type", int)
    HOTWATER_HEATER_ENABLE = Key("hotwater_heater_enable", bool)
    HUMIDITY_CONTROL_ENABLE = Key("humidity_control_enable", bool)
    MACHINE_TYPE = Key("machine_type", int)
    OPERATION_MODE = Key("operation_mode", int)
    OPERATION_MODE_CURRENT = Key("operation_mode_current", int)
    PREHEAT_ENABLE = Key("preheat_enable", bool)
    PREHEAT_OUTPUT = Key("preheat_output", float)
    REHEAT_ACTIVE = Key("reheat_active", bool)
    REHEAT_ENABLE = Key("reheat_enable", bool)
    REHEAT_OUTPUT = Key("reheat_output", float)
    ROTOR_SPEED = Key("rotor_speed", int)
    RUNNING = Key("running", bool)
    SACRIFICIAL_ANODE_OK = Key("sacrificial_anode_ok", bool)
    SERVICE_CAPACITY = Key("service_capacity", float)
    SERVICE_MODE = Key("service_mode", int)
    STATE_CODE = Key("state_code", int)
    STATE_TIME = Key("state_time", int)
    SUCTION_PRESSURE = Key("suction_pressure", int)
    TEMP_AFTER_CONDENSER = Key("temp_after_condenser", float)
    TEMP_AUX = Key("temp_aux", float)
    TEMP_BEFORE_CONDENSER = Key("temp_before_condenser", float)
    TEMP_BUFFER_TANK = Key("temp_buffer_tank", float)
    TEMP_BYPASS_FORCE = Key("temp_bypass_force", float)
    TEMP_BYPASS_OPEN_OFFSET = Key("temp_bypass_open_offset", float)
    TEMP_CENTRAL_HEAT_COMPENSATION = Key("temp_central_heat_compensation", float)
    TEMP_CENTRAL_HEAT_OFFSET = Key("temp_central_heat_offset", float)
    TEMP_CENTRAL_HEAT_RETURN = Key("temp_central_heat_return", float)
    TEMP_CENTRAL_HEAT_SUPPLY = Key("temp_central_heat_supply", float)
    TEMP_CENTRAL_HEAT_SUPPLY_MAX = Key("temp_central_heat_supply_max", float)
    TEMP_CENTRAL_HEAT_SUPPLY_MIN = Key("temp_central_heat_supply_min", float)
    TEMP_CONDENSER = Key("temp_condenser", float)
    TEMP_CONTROLLER = Key("temp_controller", float)
    TEMP_COOLING_START_OFFSET = Key("temp_cooling_start_offset", float)
    TEMP_EVAPORATOR = Key("temp_evaporator", float)
    TEMP_FROST_PROTECTION = Key("temp_frost_protection", float)
    TEMP_HEAT_PUMP_OUTDOOR = Key("temp_heat_pump_outdoor", float)
    TEMP_HEATER = Key("temp_heater", float)
    TEMP_HOTWATER = Key("temp_hotwater", float)
    TEMP_HOTWATER_BOOST = Key("temp_hotwater_boost", float)
    TEMP_HOTWATER_BOTTOM = Key("temp_hotwater_bottom", float)
    TEMP_HOTWATER_BYPASS_OFFSET = Key("temp_hotwater_bypass_offset", float)
    TEMP_HOTWATER_MAX = Key("temp_hotwater_max", float)
    TEMP_HOTWATER_TOP = Key("temp_hotwater_top", float)
    TEMP_INTAKE = Key("temp_intake", float)
    TEMP_NIGHT_COOLING_DAY_LIMIT = Key("temp_night_cooling_day_limit", float)
    TEMP_NIGHT_COOLING_TARGET = Key("temp_night_cooling_target", float)
    TEMP_PREHEAT_INTAKE = Key("temp_preheat_intake", float)
    TEMP_PRESSURE_PIPE = Key("temp_pressure_pipe", float)
    TEMP_PRESSURE_PIPE_CALCULATED = Key("temp_pressure_pipe_calculated", float)
    TEMP_ROOM = Key("temp_room", float)
    TEMP_ROOM_PANEL = Key("temp_room_panel", float)
    TEMP_SUMMER_SUPPLY_MAX = Key("temp_summer_supply_max", float)
    TEMP_SUMMER_SUPPLY_MIN = Key("temp_summer_supply_min", float)
    TEMP_SUPPLY_AFTER_HEATER = Key("temp_supply_after_heater", float)
    TEMP_WINTER_SUPPLY_MAX = Key("temp_winter_supply_max", float)
    TEMP_WINTER_SUPPLY_MIN = Key("temp_winter_supply_min", float)

    @classmethod
    def all(cls) -> tuple[Key[Any], ...]:
        """Every key, in the order declared."""
        kind: type[Key[Any]] = Key
        return _members(cls, kind)


# ================================================================================ sources


class Source:
    """Where a point's address comes from; every point carries one under the label `SOURCE`."""
    TESTED = "tested"
    """Read on a unit of the model."""
    UNTESTED = "untested"
    """Found in material published online, and not tested on a unit of the model."""
    CALCULATED = "calculated"
    """Placed from the model's Modbus manual by the order of its register group; only read, and
    not tested on a unit of the model."""


SOURCE = "source"
"""The label a point's `Source` is under: `Labels(source=Source.CALCULATED)` selects those points."""


def labelled(source: str, points: Sequence[Point[Any]]) -> tuple[Point[Any], ...]:
    return tuple(replace(point, labels={**point.labels, SOURCE: source}) for point in points)


def slave_model_in(models: Collection[int]) -> Callable[[Identity], bool]:
    """Whether the handshake names one of `models` as its slave device model."""
    chosen = frozenset(models)
    return lambda identity: identity.get("slave_device_model") in chosen


def slave_model_not_in(models: Collection[int]) -> Callable[[Identity], bool]:
    """Whether the handshake names none of `models` as its slave device model."""
    excluded = frozenset(models)
    return lambda identity: identity.get("slave_device_model") not in excluded


# ============================================================================ point types


def reading[T](key: Key[T], address: int, *, data_type: DataType = DataType.UINT16, scale: float = 1,
                offset: float = 0, unit: Unit | None = None, transform: Transform | None = None) -> Point[T]:
    """A datapoint: an input register of the controller."""
    return Point(key, read=DatapointRegister(address), data_type=data_type, scale=scale, offset=offset,
                 unit=unit, transform=transform, poll_rate=PollRate.FAST)


def temperature(key: Key[float], address: int, *, scale: float = 0.1, offset: float = 0) -> Point[float]:
    return reading(key, address, data_type=DataType.INT16, scale=scale, offset=offset, unit=Unit.CELSIUS)


def state(key: Key[bool], address: int, *, transform: Transform | None = None) -> Point[bool]:
    return reading(key, address, data_type=DataType.BOOL, transform=transform)


def setting[T](key: Key[T], address: int, limits: Limits, *, write_address: int | None = None,
                data_type: DataType = DataType.UINT16, scale: float = 1, offset: float = 0,
                unit: Unit | None = None, on_write: Refresh | None = None) -> Point[T]:
    """A setpoint: a holding register of the controller, written at `address` unless the controller
    takes writes at another."""
    return Point(key, read=SetpointRegister(address),
                 write=SetpointRegister(address if write_address is None else write_address),
                 data_type=data_type, scale=scale, offset=offset, unit=unit, limits=limits,
                 poll_rate=PollRate.SLOW, on_write=on_write)


def temperature_setting(key: Key[float], address: int, minimum: float, maximum: float) -> Point[float]:
    return setting(key, address, Limits(minimum, maximum, step=0.5), data_type=DataType.INT16, scale=0.1,
                    unit=Unit.CELSIUS)


def switch(key: Key[bool], address: int, *, write_address: int | None = None) -> Point[bool]:
    return Point(key, read=SetpointRegister(address),
                 write=SetpointRegister(address if write_address is None else write_address),
                 data_type=DataType.BOOL, poll_rate=PollRate.SLOW)


def command(key: Key[bool], address: int, *, on_write: Refresh | None = None) -> Point[bool]:
    """A holding register written to make the controller act; nothing to show once it has."""
    return Point(key, write=SetpointRegister(address), data_type=DataType.BOOL, write_kind=WriteKind.COMMAND,
                 on_write=on_write)


def calculated[T](key: Key[T], address: int, *, setpoint: bool = False, data_type: DataType = DataType.UINT16,
                   scale: float = 1, unit: Unit | None = None) -> Point[T]:
    """A register placed by the order of its group in the manual: never written, and read slowly."""
    access = SetpointRegister(address) if setpoint else DatapointRegister(address)
    return Point(key, read=access, data_type=data_type, scale=scale, unit=unit, poll_rate=PollRate.SLOW)


# ================================================================================= CTS400

FILTER_RESET_REREADS = Refresh(
    [PointKey.FILTER_OK, PointKey.ALARM_STATUS, PointKey.FILTER_REPLACE_TIME_AGO, PointKey.FILTER_REPLACE_TIME_REMAIN],
    after=2.0)
"""What a filter reset changes, read again once the controller has taken the reset; the wait leaves
room for a unit slower than the one it was measured on."""

FILTER_INTERVAL_REREADS = Refresh([PointKey.FILTER_REPLACE_TIME_REMAIN], after=2.0)
"""The days left until the filter change follow the interval, once the controller has taken it."""

FAN_LEVEL_REREADS = Refresh(
    [PointKey.FAN_LEVEL_CURRENT, PointKey.FAN_DUTYCYCLE_EXTRACT, PointKey.FAN_DUTYCYCLE_SUPPLY], after=3.0)
"""The level the fans run at, and their speeds, follow the chosen level, once the controller has taken it."""

CTS400_POINTS: tuple[Point[Any], ...] = labelled(Source.TESTED, (
    state(PointKey.BYPASS_ACTIVE, 23),
    reading(PointKey.FAN_DUTYCYCLE_EXTRACT, 24, scale=0.1, unit=Unit.PERCENT),
    reading(PointKey.FAN_DUTYCYCLE_SUPPLY, 25, scale=0.1, unit=Unit.PERCENT),
    temperature(PointKey.TEMP_OUTSIDE, 27),                                        # T1
    temperature(PointKey.TEMP_SUPPLY, 28),                                         # T2
    temperature(PointKey.TEMP_EXTRACT, 29),                                        # T3
    temperature(PointKey.TEMP_EXHAUST, 30),                                        # T4
    reading(PointKey.HUMIDITY, 31, scale=0.1, unit=Unit.PERCENT),
    reading(PointKey.HUMIDITY_AVG, 46, scale=0.1, unit=Unit.PERCENT),
    reading(PointKey.CO2_LEVEL, 47, unit=Unit.PPM),
    reading(PointKey.VOC_LEVEL, 48, unit=Unit.PPM),
    state(PointKey.FILTER_OK, 49, transform=Transforms.INVERT_BOOL),               # 1 = filter change must be made
    state(PointKey.ALARM_STATUS, 50),
    reading(PointKey.ALARM_1_CODE, 51),
    reading(PointKey.ALARM_2_CODE, 52),
    reading(PointKey.ALARM_3_CODE, 53),
    reading(PointKey.ALARM_1_INFO, 56),
    reading(PointKey.ALARM_2_INFO, 57),
    reading(PointKey.ALARM_3_INFO, 58),
    reading(PointKey.FAN_LEVEL_CURRENT, 63),
    state(PointKey.HUMIDITY_HIGH_ACTIVE, 64, transform=Transforms.INVERT_BOOL),    # 1 = the 24 hour average is OK
    reading(PointKey.HUMIDITY_HIGH_LEVEL, 66, scale=0.1),
    reading(PointKey.HUMIDITY_HIGH_LEVEL_TIME, 70, unit=Unit.MINUTES, transform=Transforms.SECONDS_AS_MINUTES),
    state(PointKey.WINTER_MODE_ACTIVE, 72),                                        # 0 = summer, 1 = winter
    reading(PointKey.FILTER_REPLACE_TIME_AGO, 77, unit=Unit.DAYS, transform=Transforms.HOURS_AS_DAYS),
    state(PointKey.DEFROST_ACTIVE, 91),
    reading(PointKey.FILTER_REPLACE_TIME_REMAIN, 110, unit=Unit.DAYS),

    command(PointKey.ALARM_RESET, 30),
    setting(PointKey.HUMIDITY_LOW_THRESHOLD, 31, Limits(15, 45, step=0.5), scale=0.1, unit=Unit.PERCENT),
    setting(PointKey.FAN_LEVEL_LOW_HUMIDITY, 32, Limits(0, 3, step=1)),
    setting(PointKey.FAN_LEVEL_HIGH_HUMIDITY, 33, Limits(2, 4, step=1)),
    setting(PointKey.FAN_LEVEL_HIGH_HUMIDITY_TIME, 34, Limits(0, 180, step=1), unit=Unit.MINUTES),
    setting(PointKey.CO2_THRESHOLD, 35, Limits(500, 2000, step=1), unit=Unit.PPM),
    setting(PointKey.VOC_THRESHOLD, 36, Limits(500, 2000, step=1), unit=Unit.PPM),
    temperature_setting(PointKey.TEMP_TARGET, 37, 10, 30),
    temperature_setting(PointKey.TEMP_REGULATION_DEAD_BAND, 38, 0, 4),
    temperature_setting(PointKey.TEMP_DEFROST_LOW_THRESHOLD, 39, 1, 5),
    temperature_setting(PointKey.TEMP_DEFROST_HIGH_THRESHOLD, 40, 5, 10),
    setting(PointKey.DEFROST_MAX_TIME, 41, Limits(5, 60, step=1), unit=Unit.MINUTES),
    setting(PointKey.DEFROST_BREAK_TIME, 43, Limits(15, 760, step=1), unit=Unit.MINUTES),
    temperature_setting(PointKey.TEMP_WINTER_MODE_THRESHOLD, 45, 5, 20),
    setting(PointKey.FILTER_REPLACE_INTERVAL, 50, Limits(0, 360, step=1), unit=Unit.DAYS,
             on_write=FILTER_INTERVAL_REREADS),
    command(PointKey.FILTER_REPLACE_RESET, 51, on_write=FILTER_RESET_REREADS),
    temperature_setting(PointKey.TEMP_SUPPLY_MIN, 57, 10, 20),
    temperature_setting(PointKey.TEMP_SUPPLY_MAX, 58, 10, 50),
    setting(PointKey.FAN_LEVEL1_SUPPLY_PRESET, 59, Limits(20, 100, step=1), scale=0.1, unit=Unit.PERCENT),
    setting(PointKey.FAN_LEVEL2_SUPPLY_PRESET, 60, Limits(20, 100, step=1), scale=0.1, unit=Unit.PERCENT),
    setting(PointKey.FAN_LEVEL3_SUPPLY_PRESET, 61, Limits(20, 100, step=1), scale=0.1, unit=Unit.PERCENT),
    setting(PointKey.FAN_LEVEL4_SUPPLY_PRESET, 62, Limits(20, 100, step=1), scale=0.1, unit=Unit.PERCENT),
    setting(PointKey.FAN_LEVEL1_EXTRACT_PRESET, 63, Limits(20, 100, step=1), scale=0.1, unit=Unit.PERCENT),
    setting(PointKey.FAN_LEVEL2_EXTRACT_PRESET, 64, Limits(20, 100, step=1), scale=0.1, unit=Unit.PERCENT),
    setting(PointKey.FAN_LEVEL3_EXTRACT_PRESET, 65, Limits(20, 100, step=1), scale=0.1, unit=Unit.PERCENT),
    setting(PointKey.FAN_LEVEL4_EXTRACT_PRESET, 66, Limits(20, 100, step=1), scale=0.1, unit=Unit.PERCENT),
    setting(PointKey.FAN_LEVEL, 69, Limits(1, 4, step=1), on_write=FAN_LEVEL_REREADS),
    switch(PointKey.ENABLE, 70),                                                   # 1 = operation
    setting(PointKey.FAN_LEVEL_HIGH_CO2, 80, Limits(2, 4, step=1)),
))

CTS400 = Model(
    "CTS 400", "Nilan", [Section(CTS400_POINTS)],
    options=MicroNabtoOptions(),
    # Readings every 10 s; settings, which change only when written, every 180 s.
    poll_intervals={PollRate.FAST: 10.0, PollRate.SLOW: 180.0},
    read_back_after=1.0,
)

