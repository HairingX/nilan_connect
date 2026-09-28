"""Nilan's controllers as models: every point's key, and the CTS400's registers.

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

from typing import Any

from modbus_event_connect import (
    DataType,
    Identity,
    Key,
    Limits,
    Model,
    Point,
    PollRate,
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
    """The key of each point a Nilan controller can have."""
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

    @classmethod
    def all(cls) -> tuple[Key[Any], ...]:
        """Every key, in the order declared."""
        kind: type[Key[Any]] = Key
        return _members(cls, kind)


# ============================================================================ point types


def _reading[T](key: Key[T], address: int, *, data_type: DataType = DataType.UINT16, scale: float = 1,
                unit: Unit | None = None, transform: Transform | None = None) -> Point[T]:
    """A datapoint: an input register of the controller."""
    return Point(key, read=DatapointRegister(address), data_type=data_type, scale=scale, unit=unit,
                 transform=transform, poll_rate=PollRate.FAST)


def _temperature(key: Key[float], address: int) -> Point[float]:
    return _reading(key, address, data_type=DataType.INT16, scale=0.1, unit=Unit.CELSIUS)


def _state(key: Key[bool], address: int, *, transform: Transform | None = None) -> Point[bool]:
    return _reading(key, address, data_type=DataType.BOOL, transform=transform)


def _setting[T](key: Key[T], address: int, limits: Limits, *, data_type: DataType = DataType.UINT16,
                scale: float = 1, unit: Unit | None = None) -> Point[T]:
    """A setpoint: a holding register of the controller, read and written at one address."""
    return Point(key, read=SetpointRegister(address), write=SetpointRegister(address), data_type=data_type,
                 scale=scale, unit=unit, limits=limits, poll_rate=PollRate.SLOW)


def _temperature_setting(key: Key[float], address: int, minimum: float, maximum: float) -> Point[float]:
    return _setting(key, address, Limits(minimum, maximum, step=0.5), data_type=DataType.INT16, scale=0.1,
                    unit=Unit.CELSIUS)


def _switch(key: Key[bool], address: int) -> Point[bool]:
    return Point(key, read=SetpointRegister(address), write=SetpointRegister(address), data_type=DataType.BOOL,
                 poll_rate=PollRate.SLOW)


def _command(key: Key[bool], address: int) -> Point[bool]:
    """A holding register written to make the controller act; nothing to show once it has."""
    return Point(key, write=SetpointRegister(address), data_type=DataType.BOOL, write_kind=WriteKind.COMMAND)


# ================================================================================= CTS400

CTS400_POINTS: tuple[Point[Any], ...] = (
    _state(PointKey.BYPASS_ACTIVE, 23),
    _reading(PointKey.FAN_DUTYCYCLE_EXTRACT, 24, scale=0.1, unit=Unit.PERCENT),
    _reading(PointKey.FAN_DUTYCYCLE_SUPPLY, 25, scale=0.1, unit=Unit.PERCENT),
    _temperature(PointKey.TEMP_OUTSIDE, 27),                                        # T1
    _temperature(PointKey.TEMP_SUPPLY, 28),                                         # T2
    _temperature(PointKey.TEMP_EXTRACT, 29),                                        # T3
    _temperature(PointKey.TEMP_EXHAUST, 30),                                        # T4
    _reading(PointKey.HUMIDITY, 31, scale=0.1, unit=Unit.PERCENT),
    _reading(PointKey.HUMIDITY_AVG, 46, scale=0.1, unit=Unit.PERCENT),
    _reading(PointKey.CO2_LEVEL, 47, unit=Unit.PPM),
    _reading(PointKey.VOC_LEVEL, 48, unit=Unit.PPM),
    _state(PointKey.FILTER_OK, 49, transform=Transforms.INVERT_BOOL),               # 1 = filter change must be made
    _state(PointKey.ALARM_STATUS, 50),
    _reading(PointKey.ALARM_1_CODE, 51),
    _reading(PointKey.ALARM_2_CODE, 52),
    _reading(PointKey.ALARM_3_CODE, 53),
    _reading(PointKey.ALARM_1_INFO, 56),
    _reading(PointKey.ALARM_2_INFO, 57),
    _reading(PointKey.ALARM_3_INFO, 58),
    _reading(PointKey.FAN_LEVEL_CURRENT, 63),
    _state(PointKey.HUMIDITY_HIGH_ACTIVE, 64, transform=Transforms.INVERT_BOOL),    # 1 = the 24 hour average is OK
    _reading(PointKey.HUMIDITY_HIGH_LEVEL, 66, scale=0.1),
    _reading(PointKey.HUMIDITY_HIGH_LEVEL_TIME, 70, unit=Unit.MINUTES, transform=Transforms.SECONDS_AS_MINUTES),
    _state(PointKey.WINTER_MODE_ACTIVE, 72),                                        # 0 = summer, 1 = winter
    _reading(PointKey.FILTER_REPLACE_TIME_AGO, 77, unit=Unit.DAYS, transform=Transforms.HOURS_AS_DAYS),
    _state(PointKey.DEFROST_ACTIVE, 91),
    _reading(PointKey.FILTER_REPLACE_TIME_REMAIN, 110, unit=Unit.DAYS),

    _command(PointKey.ALARM_RESET, 30),
    _setting(PointKey.HUMIDITY_LOW_THRESHOLD, 31, Limits(15, 45, step=0.5), scale=0.1, unit=Unit.PERCENT),
    _setting(PointKey.FAN_LEVEL_LOW_HUMIDITY, 32, Limits(0, 3, step=1)),
    _setting(PointKey.FAN_LEVEL_HIGH_HUMIDITY, 33, Limits(2, 4, step=1)),
    _setting(PointKey.FAN_LEVEL_HIGH_HUMIDITY_TIME, 34, Limits(0, 180, step=1), unit=Unit.MINUTES),
    _setting(PointKey.CO2_THRESHOLD, 35, Limits(500, 2000, step=1), unit=Unit.PPM),
    _setting(PointKey.VOC_THRESHOLD, 36, Limits(500, 2000, step=1), unit=Unit.PPM),
    _temperature_setting(PointKey.TEMP_TARGET, 37, 10, 30),
    _temperature_setting(PointKey.TEMP_REGULATION_DEAD_BAND, 38, 0, 4),
    _temperature_setting(PointKey.TEMP_DEFROST_LOW_THRESHOLD, 39, 1, 5),
    _temperature_setting(PointKey.TEMP_DEFROST_HIGH_THRESHOLD, 40, 5, 10),
    _setting(PointKey.DEFROST_MAX_TIME, 41, Limits(5, 60, step=1), unit=Unit.MINUTES),
    _setting(PointKey.DEFROST_BREAK_TIME, 43, Limits(15, 760, step=1), unit=Unit.MINUTES),
    _temperature_setting(PointKey.TEMP_WINTER_MODE_THRESHOLD, 45, 5, 20),
    _setting(PointKey.FILTER_REPLACE_INTERVAL, 50, Limits(0, 360, step=1), unit=Unit.DAYS),
    _command(PointKey.FILTER_REPLACE_RESET, 51),
    _temperature_setting(PointKey.TEMP_SUPPLY_MIN, 57, 10, 20),
    _temperature_setting(PointKey.TEMP_SUPPLY_MAX, 58, 10, 50),
    _setting(PointKey.FAN_LEVEL1_SUPPLY_PRESET, 59, Limits(20, 100, step=1), scale=0.1, unit=Unit.PERCENT),
    _setting(PointKey.FAN_LEVEL2_SUPPLY_PRESET, 60, Limits(20, 100, step=1), scale=0.1, unit=Unit.PERCENT),
    _setting(PointKey.FAN_LEVEL3_SUPPLY_PRESET, 61, Limits(20, 100, step=1), scale=0.1, unit=Unit.PERCENT),
    _setting(PointKey.FAN_LEVEL4_SUPPLY_PRESET, 62, Limits(20, 100, step=1), scale=0.1, unit=Unit.PERCENT),
    _setting(PointKey.FAN_LEVEL1_EXTRACT_PRESET, 63, Limits(20, 100, step=1), scale=0.1, unit=Unit.PERCENT),
    _setting(PointKey.FAN_LEVEL2_EXTRACT_PRESET, 64, Limits(20, 100, step=1), scale=0.1, unit=Unit.PERCENT),
    _setting(PointKey.FAN_LEVEL3_EXTRACT_PRESET, 65, Limits(20, 100, step=1), scale=0.1, unit=Unit.PERCENT),
    _setting(PointKey.FAN_LEVEL4_EXTRACT_PRESET, 66, Limits(20, 100, step=1), scale=0.1, unit=Unit.PERCENT),
    _setting(PointKey.FAN_LEVEL, 69, Limits(1, 4, step=1)),
    _switch(PointKey.ENABLE, 70),                                                   # 1 = operation
    _setting(PointKey.FAN_LEVEL_HIGH_CO2, 80, Limits(2, 4, step=1)),
)

CTS400 = Model(
    "CTS 400", "Nilan", [Section(CTS400_POINTS)],
    options=MicroNabtoOptions(),
    # Readings every 10 s; settings, which change only when written, every 180 s.
    poll_intervals={PollRate.FAST: 10.0, PollRate.SLOW: 180.0},
    read_back_after=1.0,
)


# =============================================================================== selection


def select_model(identity: Identity) -> Model | None:
    """The model for the controller the handshake names; None for one not supported yet.

    A CTS400 reported device model 1140, slave device 72270 and slave device model 1 on
    2026-09-27.
    """
    if identity.get("device_model") == 1140 and identity.get("slave_device_number") == 72270 \
            and identity.get("slave_device_model") == 1:
        return CTS400
    return None
