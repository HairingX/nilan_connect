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

from collections.abc import Callable, Collection, Mapping, Sequence
from dataclasses import replace
from datetime import date, datetime
from enum import IntEnum
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

from ._states import (
    AirExchangeMode,
    Alarm,
    CentralHeatMode,
    CirculationPumpMode,
    CompressorPriority,
    ControlSensor,
    CoolingSetpoint,
    DamperTestState,
    HeatSource,
    OperationMode,
    OperationState,
    ServiceMode,
    Weekday,
)

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

    # The keys below are the other controllers'.
    ALARM_1 = Key("alarm_1", Alarm)
    """The alarm `alarm_1_code` holds, whichever controller reports it."""
    ALARM_2 = Key("alarm_2", Alarm)
    ALARM_3 = Key("alarm_3", Alarm)
    ALARM_1_TIME = Key("alarm_1_time", datetime)
    """When alarm 1 was raised, by the controller's clock, without a time zone."""
    ALARM_2_TIME = Key("alarm_2_time", datetime)
    ALARM_3_TIME = Key("alarm_3_time", datetime)
    ALARM_BITS = Key("alarm_bits", int)
    """The alarm register as it is: one bit per alarm."""
    ALARM_BITS_HIGH = Key("alarm_bits_high", int)
    """The second alarm register, where a controller has one."""
    ALARM_EXTERNAL_FILTER = Key("alarm_external_filter", bool)
    ALARM_EXTERNAL_STOP = Key("alarm_external_stop", bool)
    ALARM_EXTRACT_FAN_ERROR = Key("alarm_extract_fan_error", bool)
    ALARM_FAN_ERROR = Key("alarm_fan_error", bool)
    ALARM_FIRE_BOX_1_ERROR = Key("alarm_fire_box_1_error", bool)
    ALARM_FIRE_BOX_2_ERROR = Key("alarm_fire_box_2_error", bool)
    ALARM_FIRE_DAMPER_1_ERROR = Key("alarm_fire_damper_1_error", bool)
    ALARM_FIRE_DAMPER_2_ERROR = Key("alarm_fire_damper_2_error", bool)
    ALARM_FIRE_DAMPER_3_ERROR = Key("alarm_fire_damper_3_error", bool)
    ALARM_FIRE_DAMPER_4_ERROR = Key("alarm_fire_damper_4_error", bool)
    ALARM_FIRE_TEST_ERROR = Key("alarm_fire_test_error", bool)
    ALARM_FLOW_TEMPERATURE_ERROR = Key("alarm_flow_temperature_error", bool)
    ALARM_FROST_FAILURE = Key("alarm_frost_failure", bool)
    ALARM_HIGH_PRESSURE = Key("alarm_high_pressure", bool)
    ALARM_HUMIDITY_SENSOR_ERROR = Key("alarm_humidity_sensor_error", bool)
    ALARM_INTERNAL_MODBUS = Key("alarm_internal_modbus", bool)
    ALARM_LOW_PRESSURE = Key("alarm_low_pressure", bool)
    ALARM_PANEL_COMMUNICATION = Key("alarm_panel_communication", bool)
    ALARM_RETURN_TEMPERATURE_ERROR = Key("alarm_return_temperature_error", bool)
    ALARM_ROTOR = Key("alarm_rotor", bool)
    ALARM_SENSOR_ERROR = Key("alarm_sensor_error", bool)
    ALARM_SENSOR_T1_ERROR = Key("alarm_sensor_t1_error", bool)
    ALARM_SENSOR_T2_ERROR = Key("alarm_sensor_t2_error", bool)
    ALARM_SENSOR_T3_ERROR = Key("alarm_sensor_t3_error", bool)
    ALARM_SENSOR_T4_ERROR = Key("alarm_sensor_t4_error", bool)
    ALARM_SENSOR_T5_ERROR = Key("alarm_sensor_t5_error", bool)
    ALARM_SENSOR_T6_ERROR = Key("alarm_sensor_t6_error", bool)
    ALARM_SENSOR_T7_ERROR = Key("alarm_sensor_t7_error", bool)
    ALARM_SENSOR_T8_ERROR = Key("alarm_sensor_t8_error", bool)
    ALARM_SENSOR_T9_ERROR = Key("alarm_sensor_t9_error", bool)
    ALARM_SENSOR_T10_ERROR = Key("alarm_sensor_t10_error", bool)
    ALARM_SENSOR_T11_ERROR = Key("alarm_sensor_t11_error", bool)
    ALARM_SUPPLY_FAN_ERROR = Key("alarm_supply_fan_error", bool)
    AIR_EXCHANGE_MODE = Key("air_exchange_mode", AirExchangeMode)
    ANTILEGIONELLA_DAY = Key("antilegionella_day", Weekday)
    """The day hot water is heated against legionella."""
    BOOST_ENABLE = Key("boost_enable", bool)
    BOOST_TIME = Key("boost_time", int)
    BYPASS_FAN_INCREASE = Key("bypass_fan_increase", int)
    """How much faster the fans run while the bypass cools the rooms."""
    BYPASS_POSITION = Key("bypass_position", int)
    CENTRAL_HEAT_CURVE = Key("central_heat_curve", int)
    """The outdoor temperature compensation curve, 1-10."""
    CENTRAL_HEAT_MODE = Key("central_heat_mode", CentralHeatMode)
    CENTRAL_HEAT_PUMP_MODE = Key("central_heat_pump_mode", CirculationPumpMode)
    CENTRAL_HEAT_REGULATION_TIME = Key("central_heat_regulation_time", int)
    CENTRAL_HEAT_SOURCE = Key("central_heat_source", HeatSource)
    COMPRESSOR_PRIORITY = Key("compressor_priority", CompressorPriority)
    CONTROL_SENSOR = Key("control_sensor", ControlSensor)
    COOLING_ENABLE = Key("cooling_enable", bool)
    COOLING_TEMPERATURE = Key("cooling_temperature", int)
    """An Optima 301's cooling setting, whose meaning no public description gives."""
    DAMPER_TEST_DAY = Key("damper_test_day", Weekday)
    """The day the air damper tests itself."""
    DAMPER_TEST_LAST_DATE = Key("damper_test_last_date", date)
    DAMPER_TEST_STATE = Key("damper_test_state", DamperTestState)
    DISCHARGE_PRESSURE = Key("discharge_pressure", float)
    FAN_LEVEL_COOLING = Key("fan_level_cooling", int)
    """The fan level while the unit cools."""
    FAN_LEVEL_EXTRACT = Key("fan_level_extract", int)
    """The level the extract fan runs at."""
    FAN_LEVEL_SUPPLY = Key("fan_level_supply", int)
    """The level the supply fan runs at."""
    FAN_RPM_EXTRACT = Key("fan_rpm_extract", int)
    FAN_RPM_SUPPLY = Key("fan_rpm_supply", int)
    HEAT_PUMP_ACTIVE = Key("heat_pump_active", bool)
    HEAT_PUMP_CAPACITY = Key("heat_pump_capacity", float)
    HEAT_PUMP_HEATER_ACTIVE = Key("heat_pump_heater_active", bool)
    HEAT_PUMP_ROOM_HEATING = Key("heat_pump_room_heating", bool)
    HEAT_PUMP_STATE = Key("heat_pump_state", OperationState)
    HEAT_PUMP_WATER_HEATING = Key("heat_pump_water_heating", bool)
    HEAT_SOURCE = Key("heat_source", HeatSource)
    """What heats the supply air."""
    HOTWATER_HEATER_ENABLE = Key("hotwater_heater_enable", bool)
    HOTWATER_SUPPLEMENT = Key("hotwater_supplement", HeatSource)
    """What supplements the heat pump for hot water."""
    HUMIDITY_CONTROL_ENABLE = Key("humidity_control_enable", bool)
    OPERATION_MODE = Key("operation_mode", OperationMode)
    """The operation mode chosen."""
    OPERATION_MODE_CURRENT = Key("operation_mode_current", OperationMode)
    """The operation mode the unit runs in."""
    OPERATION_STATE = Key("operation_state", OperationState)
    """The state `state_code` holds."""
    PREHEAT_ENABLE = Key("preheat_enable", bool)
    PREHEAT_OUTPUT = Key("preheat_output", float)
    REHEAT_ACTIVE = Key("reheat_active", bool)
    REHEAT_ENABLE = Key("reheat_enable", bool)
    REHEAT_OUTPUT = Key("reheat_output", float)
    ROTOR_SPEED = Key("rotor_speed", int)
    RUNNING = Key("running", bool)
    """True while the unit runs; `enable` is whether it is asked to."""
    SACRIFICIAL_ANODE_OK = Key("sacrificial_anode_ok", bool)
    SERVICE_CAPACITY = Key("service_capacity", float)
    SERVICE_MODE = Key("service_mode", ServiceMode)
    STATE_CODE = Key("state_code", int)
    """The control state as the controller numbers it."""
    SUCTION_PRESSURE = Key("suction_pressure", float)
    TEMP_AFTER_CONDENSER = Key("temp_after_condenser", float)
    TEMP_AUX = Key("temp_aux", float)
    TEMP_BEFORE_CONDENSER = Key("temp_before_condenser", float)
    TEMP_BUFFER_TANK = Key("temp_buffer_tank", float)
    TEMP_BYPASS_CLOSE_OFFSET = Key("temp_bypass_close_offset", float)
    """How far below the target temperature the outdoor air may be before the bypass stays
    closed; 0 for no limit."""
    TEMP_BYPASS_FAN_INCREASE_OFFSET = Key("temp_bypass_fan_increase_offset", float)
    """How far above the target temperature the fans run faster while the bypass cools."""
    TEMP_BYPASS_OPEN_OFFSET = Key("temp_bypass_open_offset", float)
    TEMP_CENTRAL_HEAT_COMPENSATION = Key("temp_central_heat_compensation", float)
    TEMP_CENTRAL_HEAT_OFFSET = Key("temp_central_heat_offset", float)
    TEMP_CENTRAL_HEAT_RETURN = Key("temp_central_heat_return", float)
    TEMP_CENTRAL_HEAT_SUPPLY = Key("temp_central_heat_supply", float)
    TEMP_CENTRAL_HEAT_SUPPLY_MAX = Key("temp_central_heat_supply_max", float)
    TEMP_CENTRAL_HEAT_SUPPLY_MIN = Key("temp_central_heat_supply_min", float)
    TEMP_CONDENSER = Key("temp_condenser", float)
    TEMP_CONTROLLER = Key("temp_controller", float)
    """The controller board's own temperature."""
    TEMP_COOLING_START_OFFSET = Key("temp_cooling_start_offset", CoolingSetpoint)
    TEMP_EVAPORATOR = Key("temp_evaporator", float)
    TEMP_FROST_PROTECTION = Key("temp_frost_protection", float)
    TEMP_HEAT_PUMP_OUTDOOR = Key("temp_heat_pump_outdoor", float)
    TEMP_HEATER = Key("temp_heater", float)
    """The heating surface."""
    TEMP_HOTWATER = Key("temp_hotwater", float)
    TEMP_HOTWATER_BOOST = Key("temp_hotwater_boost", float)
    TEMP_HOTWATER_BOTTOM = Key("temp_hotwater_bottom", float)
    TEMP_HOTWATER_BYPASS_OFFSET = Key("temp_hotwater_bypass_offset", float)
    TEMP_HOTWATER_SCALD_PROTECTION = Key("temp_hotwater_scald_protection", float)
    TEMP_HOTWATER_TOP = Key("temp_hotwater_top", float)
    TEMP_INTAKE = Key("temp_intake", float)
    """Fresh air as it enters the unit."""
    TEMP_NIGHT_COOLING_DAY_LIMIT = Key("temp_night_cooling_day_limit", float)
    TEMP_NIGHT_COOLING_TARGET = Key("temp_night_cooling_target", float)
    TEMP_PREHEAT_INTAKE = Key("temp_preheat_intake", float)
    """Air entering the preheater or earth tube."""
    TEMP_PRESSURE_PIPE = Key("temp_pressure_pipe", float)
    TEMP_ROOM = Key("temp_room", float)
    TEMP_ROOM_PANEL = Key("temp_room_panel", float)
    """The room temperature at the user panel."""
    TEMP_SUMMER_SUPPLY_MAX = Key("temp_summer_supply_max", float)
    TEMP_SUMMER_SUPPLY_MIN = Key("temp_summer_supply_min", float)
    TEMP_SUPPLY_AFTER_HEATER = Key("temp_supply_after_heater", float)
    TEMP_WINTER_SUPPLY_MAX = Key("temp_winter_supply_max", float)
    TEMP_WINTER_SUPPLY_MIN = Key("temp_winter_supply_min", float)
    TIME_IN_STATE = Key("time_in_state", int)
    """Seconds the unit has been in its current control state."""

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
            offset: float = 0, unit: Unit | None = None, transform: Transform | None = None,
            codes: Mapping[int, IntEnum] | None = None) -> Point[T]:
    """A datapoint: an input register of the controller."""
    return Point(key, read=DatapointRegister(address), data_type=data_type, scale=scale, offset=offset,
                 unit=unit, transform=transform, codes=codes, poll_rate=PollRate.FAST)


def alarm_bit(key: Key[bool], address: int, bit: int, *, inverted: bool = False) -> Point[bool]:
    """One alarm of an alarm register: true while it is raised, or, `inverted`, while it is not."""
    return Point(key, read=DatapointRegister(address), data_type=DataType.bit(bit),
                 transform=Transforms.INVERT_BOOL if inverted else None, poll_rate=PollRate.FAST)


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


def choice[T: IntEnum](key: Key[T], address: int, *, write_address: int | None = None,
                       codes: Mapping[int, IntEnum] | None = None) -> Point[T]:
    """A setting that is one of the states its key names: a holding register, written at `address`
    unless the controller takes writes at another."""
    return Point(key, read=SetpointRegister(address),
                 write=SetpointRegister(address if write_address is None else write_address),
                 codes=codes, poll_rate=PollRate.SLOW)


def switch(key: Key[bool], address: int, *, write_address: int | None = None) -> Point[bool]:
    return Point(key, read=SetpointRegister(address),
                 write=SetpointRegister(address if write_address is None else write_address),
                 data_type=DataType.BOOL, poll_rate=PollRate.SLOW)


def command(key: Key[bool], address: int, *, on_write: Refresh | None = None) -> Point[bool]:
    """A holding register written to make the controller act; nothing to show once it has."""
    return Point(key, write=SetpointRegister(address), data_type=DataType.BOOL, write_kind=WriteKind.COMMAND,
                 on_write=on_write)


def calculated[T](key: Key[T], address: int, *, setpoint: bool = False, data_type: DataType = DataType.UINT16,
                  scale: float = 1, unit: Unit | None = None, codes: Mapping[int, IntEnum] | None = None) -> Point[T]:
    """A register placed by the order of its group in the manual: never written, and read slowly."""
    access = SetpointRegister(address) if setpoint else DatapointRegister(address)
    return Point(key, read=access, data_type=data_type, scale=scale, unit=unit, codes=codes, poll_rate=PollRate.SLOW)


# ================================================================================= CTS400

CTS400_ALARMS: Mapping[int, Alarm] = {
    0: Alarm.NONE, 1: Alarm.CHANGE_FILTER, 15: Alarm.DEFROST_TIMEOUT_EXCHANGER,
    16: Alarm.SENSOR_T1_OPEN, 17: Alarm.SENSOR_T1_SHORT, 18: Alarm.SENSOR_T2_OPEN, 19: Alarm.SENSOR_T2_SHORT,
    20: Alarm.SENSOR_T3_OPEN, 21: Alarm.SENSOR_T3_SHORT, 22: Alarm.SENSOR_T4_OPEN, 23: Alarm.SENSOR_T4_SHORT,
    24: Alarm.SENSOR_T7_OPEN, 25: Alarm.SENSOR_T7_SHORT, 26: Alarm.HUMIDITY_SENSOR_ERROR, 27: Alarm.CO2_SENSOR_ERROR,
    28: Alarm.AFTERHEAT_FROST_THERMOSTAT_ERROR, 29: Alarm.AFTERHEAT_FROST_RISK, 48: Alarm.FIRE_INPUT, 49: Alarm.FIRE,
    50: Alarm.AFTERHEAT_FROST, 51: Alarm.ROOM_TEMPERATURE_LOW, 52: Alarm.EMERGENCY_STOP,
}
"""What each of a CTS400's alarm codes means (software instructions S75, pages 23-24); 0 is none."""

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
    reading(PointKey.ALARM_1, 51, codes=CTS400_ALARMS),
    reading(PointKey.ALARM_2, 52, codes=CTS400_ALARMS),
    reading(PointKey.ALARM_3, 53, codes=CTS400_ALARMS),
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

