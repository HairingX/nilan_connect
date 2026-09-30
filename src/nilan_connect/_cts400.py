"""Nilan's CTS400 as a model.

Sources:
    Nilan, "Protocol description Nilan CTS400 Modbus version 1.0", doc. version 1.10,
    22-08-2024: the addresses, decimals, data types and limits of every CTS400 register.
    Nilan, "Software instructions Comfort CTS400" (S75), version 1.30, 20-01-2025: the sensors,
    T1 outdoor, T2 supply, T3 extract and T4 discharge air, and the alarm codes.
    Both are in this repository's docs/models/nilan-cts400.

Over micro_nabto a CTS400 is read at the manual's own addresses.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from modbus_event_connect import DataType, Key, Limits, Point, Quality, Refresh, Scan, Transforms, Unit

from ._certainty import section
from ._keys import PointKey
from ._points import choice, command, fan_level_rereads, nilan_model, reading, setting, state, switch, temperature
from ._states import Alarm, ExtraSensor

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

FAN_LEVEL_REREADS = fan_level_rereads(
    PointKey.FAN_LEVEL_CURRENT, PointKey.FAN_DUTYCYCLE_EXTRACT, PointKey.FAN_DUTYCYCLE_SUPPLY)


def _temperature_setting(key: Key[float], address: int, minimum: float, maximum: float) -> Point[float]:
    return setting(key, address, Limits(minimum, maximum, step=0.5), data_type=DataType.INT16, scale=0.1,
                   unit=Unit.CELSIUS)


def _fan_speed(key: Key[float], address: int) -> Point[float]:
    return setting(key, address, Limits(20, 100, step=1), scale=0.1, unit=Unit.PERCENT)


CTS400_POINTS: tuple[Point[Any], ...] = (
    state(PointKey.DIGITAL_INPUT_1, 20),
    state(PointKey.DIGITAL_INPUT_2, 21),
    state(PointKey.DIGITAL_INPUT_3, 22),
    state(PointKey.BYPASS_ACTIVE, 23),
    reading(PointKey.FAN_DUTYCYCLE_EXTRACT, 24, scale=0.1, unit=Unit.PERCENT),
    reading(PointKey.FAN_DUTYCYCLE_SUPPLY, 25, scale=0.1, unit=Unit.PERCENT),
    reading(PointKey.REHEAT_OUTPUT, 26, scale=0.1, unit=Unit.PERCENT),
    temperature(PointKey.TEMP_OUTSIDE, 27, scale=0.1),                             # T1
    temperature(PointKey.TEMP_SUPPLY, 28, scale=0.1),                              # T2
    temperature(PointKey.TEMP_EXTRACT, 29, scale=0.1),                             # T3
    temperature(PointKey.TEMP_EXHAUST, 30, scale=0.1),                             # T4
    reading(PointKey.HUMIDITY, 31, scale=0.1, unit=Unit.PERCENT),
    reading(PointKey.HUMIDITY_AVG, 46, scale=0.1, unit=Unit.PERCENT),
    reading(PointKey.CO2_LEVEL, 47, unit=Unit.PPM),
    reading(PointKey.VOC_LEVEL, 48, unit=Unit.PPM),
    state(PointKey.FILTER_OK, 49, inverted=True),                                  # 1 = filter change must be made
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
    state(PointKey.HUMIDITY_HIGH_ACTIVE, 64, inverted=True),                       # 1 = the 24 hour average is OK
    reading(PointKey.HUMIDITY_HIGH_LEVEL, 66, scale=0.1),
    reading(PointKey.HUMIDITY_HIGH_LEVEL_TIME, 70, unit=Unit.MINUTES, transform=Transforms.SECONDS_AS_MINUTES),
    state(PointKey.WINTER_MODE_ACTIVE, 72),                                        # 0 = summer, 1 = winter
    state(PointKey.REHEAT_ACTIVE, 74),
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
    _temperature_setting(PointKey.TEMP_TARGET, 37, 10, 30),
    _temperature_setting(PointKey.TEMP_REGULATION_DEAD_BAND, 38, 0, 4),
    _temperature_setting(PointKey.TEMP_DEFROST_LOW_THRESHOLD, 39, 1, 5),
    _temperature_setting(PointKey.TEMP_DEFROST_HIGH_THRESHOLD, 40, 5, 10),
    setting(PointKey.DEFROST_MAX_TIME, 41, Limits(5, 60, step=1), unit=Unit.MINUTES),
    setting(PointKey.DEFROST_BREAK_TIME, 43, Limits(15, 760, step=1), unit=Unit.MINUTES),
    _temperature_setting(PointKey.TEMP_WINTER_MODE_THRESHOLD, 45, 5, 20),
    setting(PointKey.FILTER_REPLACE_INTERVAL, 50, Limits(0, 360, step=1), unit=Unit.DAYS,
            on_write=FILTER_INTERVAL_REREADS),
    switch(PointKey.FILTER_ALARM_ON_PANEL, 47),
    choice(PointKey.EXTRA_SENSOR, 48),
    command(PointKey.FILTER_REPLACE_RESET, 51, on_write=FILTER_RESET_REREADS),
    _temperature_setting(PointKey.TEMP_SUPPLY_MIN, 57, 10, 20),
    _temperature_setting(PointKey.TEMP_SUPPLY_MAX, 58, 10, 50),
    _fan_speed(PointKey.FAN_LEVEL1_SUPPLY_PRESET, 59),
    _fan_speed(PointKey.FAN_LEVEL2_SUPPLY_PRESET, 60),
    _fan_speed(PointKey.FAN_LEVEL3_SUPPLY_PRESET, 61),
    _fan_speed(PointKey.FAN_LEVEL4_SUPPLY_PRESET, 62),
    _fan_speed(PointKey.FAN_LEVEL1_EXTRACT_PRESET, 63),
    _fan_speed(PointKey.FAN_LEVEL2_EXTRACT_PRESET, 64),
    _fan_speed(PointKey.FAN_LEVEL3_EXTRACT_PRESET, 65),
    _fan_speed(PointKey.FAN_LEVEL4_EXTRACT_PRESET, 66),
    setting(PointKey.FAN_LEVEL, 69, Limits(1, 4, step=1), on_write=FAN_LEVEL_REREADS),
    switch(PointKey.ENABLE, 70),                                                   # 1 = operation
    switch(PointKey.PANEL_LOCK_FAN_LEVEL, 72),
    switch(PointKey.PANEL_LOCK_ON_OFF, 73),
    switch(PointKey.DEFROST_SUPPLY_FAN, 78),                                       # 0 = stopped, 1 = operation
    setting(PointKey.FAN_LEVEL_HIGH_CO2, 80, Limits(2, 4, step=1)),
)

CO2_POINTS: tuple[Key[Any], ...] = (PointKey.CO2_LEVEL, PointKey.CO2_THRESHOLD, PointKey.FAN_LEVEL_HIGH_CO2)
"""What a CTS400 has only with a CO2 sensor fitted: its manual shows CO2 regulation "only if a
CO2sensor has been installed"."""

VOC_POINTS: tuple[Key[Any], ...] = (PointKey.VOC_LEVEL, PointKey.VOC_THRESHOLD)
"""What a CTS400 has only with a VOC sensor fitted."""


async def extra_sensor_fitted(scan: Scan) -> None:
    """Mark the CO2 or VOC points missing unless HR 48 says that sensor is fitted."""
    current = (await scan.read([PointKey.EXTRA_SENSOR])).get(PointKey.EXTRA_SENSOR)
    fitted = current.value if current is not None and current.quality is Quality.GOOD else None
    if fitted is not ExtraSensor.CO2:
        scan.set_available(list(CO2_POINTS), False, reason="no CO2 sensor fitted")
    if fitted is not ExtraSensor.VOC:
        scan.set_available(list(VOC_POINTS), False, reason="no VOC sensor fitted")


CTS400 = nilan_model("CTS 400", "Nilan", [section(verified=CTS400_POINTS)], scan_steps=[extra_sensor_fitted])
