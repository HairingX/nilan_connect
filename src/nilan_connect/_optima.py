"""Genvex's Optima controllers as models.

Sources:
    No Modbus description of an Optima is published. The gateway's addresses, scales and
    ranges were found in material published online. The user manuals in this repository's
    docs/models/genvex-optima name the sensors and the settings' ranges.
"""
from __future__ import annotations

from typing import Any

from modbus_event_connect import DataType, Key, Limits, Point, Refresh, Unit

from ._certainty import section
from ._keys import PointKey
from ._points import (
    alarm_bit,
    command,
    fan_level_rereads,
    nilan_model,
    reading,
    setting,
    state,
    switch,
    temperature,
)


def optima_temperature(key: Key[float], address: int) -> Point[float]:
    """A datapoint holding a temperature in tenths of a °C above -30 °C."""
    return temperature(key, address, scale=0.1, offset=-30)


def optima_percent(key: Key[float], address: int, *, scale: float = 1) -> Point[float]:
    """A datapoint holding a percentage."""
    return reading(key, address, data_type=DataType.INT16, scale=scale, unit=Unit.PERCENT)


def optima_rpm(key: Key[int], address: int) -> Point[int]:
    """A datapoint holding a speed in revolutions per minute."""
    return reading(key, address, data_type=DataType.INT16, unit=Unit.RPM)


def optima_target(address: int, *, write_address: int | None = None) -> Point[float]:
    """The setpoint holding the target temperature, in tenths of a °C above 10 °C."""
    return setting(PointKey.TEMP_TARGET, address, Limits(10, 30, step=0.5), write_address=write_address,
                   data_type=DataType.INT16, scale=0.1, offset=10, unit=Unit.CELSIUS)


def optima_fan_presets(address: int) -> tuple[Point[float], ...]:
    """The fans' speeds at levels 1 to 3, supply fan first, in the six setpoints from `address`."""
    keys = (PointKey.FAN_LEVEL1_SUPPLY_PRESET, PointKey.FAN_LEVEL2_SUPPLY_PRESET, PointKey.FAN_LEVEL3_SUPPLY_PRESET,
            PointKey.FAN_LEVEL1_EXTRACT_PRESET, PointKey.FAN_LEVEL2_EXTRACT_PRESET, PointKey.FAN_LEVEL3_EXTRACT_PRESET)
    return tuple(setting(key, address + n, Limits(0, 100, step=1), unit=Unit.PERCENT) for n, key in enumerate(keys))


def written_apart_setting[T](key: Key[T], address: int, limits: Limits | None, *,
                             data_type: DataType = DataType.UINT16, scale: float = 1,
                             unit: Unit | None = None, on_write: Refresh | None = None) -> Point[T]:
    """A setpoint of an Optima 270 or 314, which takes the write to the setpoint it reports at
    `address` at 2 × `address` + 10."""
    return setting(key, address, limits, write_address=2 * address + 10, data_type=data_type, scale=scale,
                   unit=unit, on_write=on_write)


def written_apart_fan_level() -> Point[int]:
    """The fan level of an Optima 270 or 314."""
    return written_apart_setting(PointKey.FAN_LEVEL, 7, Limits(0, 4, step=1), on_write=fan_level_rereads(
        PointKey.FAN_DUTYCYCLE_SUPPLY, PointKey.FAN_DUTYCYCLE_EXTRACT, PointKey.FAN_RPM_SUPPLY,
        PointKey.FAN_RPM_EXTRACT))


def written_apart_switch(key: Key[bool], address: int) -> Point[bool]:
    """A switch of an Optima 270 or 314, written at 2 × `address` + 10."""
    return switch(key, address, write_address=2 * address + 10)


# The alarm bits, as found in material published online. The filter alarm's bit is set while the
# filter must be changed, so it is `filter_ok` inverted, as every controller has that key.

ALARMS_250: tuple[Point[bool], ...] = (
    alarm_bit(PointKey.ALARM_EXTERNAL_STOP, 101, 0),
    alarm_bit(PointKey.FILTER_OK, 101, 1, inverted=True),
    alarm_bit(PointKey.ALARM_HIGH_PRESSURE, 101, 2),
    alarm_bit(PointKey.ALARM_FROST_FAILURE, 101, 3),
    alarm_bit(PointKey.ALARM_PANEL_COMMUNICATION, 101, 4),
    alarm_bit(PointKey.ALARM_EXTERNAL_FILTER, 101, 5),
    alarm_bit(PointKey.ALARM_FAN_ERROR, 101, 6),
    alarm_bit(PointKey.ALARM_SENSOR_ERROR, 101, 7),
)
"""The Optima 250's, 251's, 301's and 312's alarms."""

ALARMS_270: tuple[Point[bool], ...] = (
    alarm_bit(PointKey.FILTER_OK, 114, 0, inverted=True),
    alarm_bit(PointKey.ALARM_EXTERNAL_STOP, 114, 1),
    alarm_bit(PointKey.ALARM_SENSOR_T1_ERROR, 114, 2),
    alarm_bit(PointKey.ALARM_SENSOR_T2_ERROR, 114, 3),
    alarm_bit(PointKey.ALARM_SENSOR_T3_ERROR, 114, 4),
    alarm_bit(PointKey.ALARM_SENSOR_T4_ERROR, 114, 5),
    alarm_bit(PointKey.ALARM_SENSOR_T5_ERROR, 114, 6),
    alarm_bit(PointKey.ALARM_SENSOR_T6_ERROR, 114, 7),
    alarm_bit(PointKey.ALARM_SENSOR_T7_ERROR, 114, 8),
    alarm_bit(PointKey.ALARM_SENSOR_T8_ERROR, 114, 9),
    alarm_bit(PointKey.ALARM_SENSOR_T9_ERROR, 114, 10),
    alarm_bit(PointKey.ALARM_HUMIDITY_SENSOR_ERROR, 114, 11),
    alarm_bit(PointKey.ALARM_FIRE_TEST_ERROR, 114, 12),
    alarm_bit(PointKey.ALARM_SUPPLY_FAN_ERROR, 114, 13),
    alarm_bit(PointKey.ALARM_EXTRACT_FAN_ERROR, 114, 14),
    alarm_bit(PointKey.ALARM_FROST_FAILURE, 114, 15),
    alarm_bit(PointKey.ALARM_FIRE_DAMPER_1_ERROR, 115, 0),
    alarm_bit(PointKey.ALARM_FIRE_DAMPER_2_ERROR, 115, 1),
    alarm_bit(PointKey.ALARM_FIRE_DAMPER_3_ERROR, 115, 2),
    alarm_bit(PointKey.ALARM_FIRE_DAMPER_4_ERROR, 115, 3),
    alarm_bit(PointKey.ALARM_FIRE_BOX_1_ERROR, 115, 4),
    alarm_bit(PointKey.ALARM_FIRE_BOX_2_ERROR, 115, 5),
    alarm_bit(PointKey.ALARM_ROTOR, 115, 6),
)

ALARMS_314: tuple[Point[bool], ...] = (
    alarm_bit(PointKey.FILTER_OK, 114, 1, inverted=True),
    alarm_bit(PointKey.ALARM_EXTERNAL_STOP, 114, 2),
    alarm_bit(PointKey.ALARM_SENSOR_T1_ERROR, 114, 3),
    alarm_bit(PointKey.ALARM_SENSOR_T2_ERROR, 114, 4),
    alarm_bit(PointKey.ALARM_SENSOR_T3_ERROR, 114, 5),
    alarm_bit(PointKey.ALARM_SENSOR_T4_ERROR, 114, 6),
    alarm_bit(PointKey.ALARM_SENSOR_T5_ERROR, 114, 7),
    alarm_bit(PointKey.ALARM_SENSOR_T6_ERROR, 114, 8),
    alarm_bit(PointKey.ALARM_SENSOR_T7_ERROR, 114, 9),
    alarm_bit(PointKey.ALARM_SENSOR_T8_ERROR, 114, 10),
    alarm_bit(PointKey.ALARM_SENSOR_T9_ERROR, 114, 11),
    alarm_bit(PointKey.ALARM_HUMIDITY_SENSOR_ERROR, 114, 12),
    alarm_bit(PointKey.ALARM_FIRE_TEST_ERROR, 114, 13),
    alarm_bit(PointKey.ALARM_SUPPLY_FAN_ERROR, 114, 14),
    alarm_bit(PointKey.ALARM_EXTRACT_FAN_ERROR, 114, 15),
    alarm_bit(PointKey.ALARM_FIRE_DAMPER_1_ERROR, 115, 1),
    alarm_bit(PointKey.ALARM_FIRE_DAMPER_2_ERROR, 115, 2),
    alarm_bit(PointKey.ALARM_FIRE_DAMPER_3_ERROR, 115, 3),
    alarm_bit(PointKey.ALARM_FIRE_DAMPER_4_ERROR, 115, 4),
    alarm_bit(PointKey.ALARM_FIRE_BOX_1_ERROR, 115, 5),
    alarm_bit(PointKey.ALARM_FIRE_BOX_2_ERROR, 115, 6),
    alarm_bit(PointKey.ALARM_INTERNAL_MODBUS, 115, 8),
    alarm_bit(PointKey.ALARM_HIGH_PRESSURE, 115, 9),
    alarm_bit(PointKey.ALARM_LOW_PRESSURE, 115, 10),
    alarm_bit(PointKey.ALARM_FLOW_TEMPERATURE_ERROR, 115, 11),
    alarm_bit(PointKey.ALARM_RETURN_TEMPERATURE_ERROR, 115, 12),
    alarm_bit(PointKey.ALARM_SENSOR_T10_ERROR, 115, 13),
    alarm_bit(PointKey.ALARM_SENSOR_T11_ERROR, 115, 14),
)


_SLAVE_79250_POINTS: tuple[Point[Any], ...] = (
    optima_temperature(PointKey.TEMP_SUPPLY, 0),
    optima_temperature(PointKey.TEMP_OUTSIDE, 2),
    optima_temperature(PointKey.TEMP_EXHAUST, 3),
    reading(PointKey.HUMIDITY, 10, data_type=DataType.INT16, unit=Unit.PERCENT),
    reading(PointKey.ALARM_BITS, 101),
    *ALARMS_250,
    optima_percent(PointKey.FAN_DUTYCYCLE_SUPPLY, 102),
    optima_percent(PointKey.FAN_DUTYCYCLE_EXTRACT, 103),
    state(PointKey.BYPASS_ACTIVE, 104),
    optima_target(0),
    *optima_fan_presets(6),
    command(PointKey.FILTER_REPLACE_RESET, 105),
)
"""What the Optima 250, 251, 301 and 312 - slave device 79250 - share."""


OPTIMA_250_SECTIONS = (
    section(reported=(
        *_SLAVE_79250_POINTS,
        optima_temperature(PointKey.TEMP_EXTRACT, 6),
        optima_rpm(PointKey.FAN_RPM_SUPPLY, 108),
        optima_rpm(PointKey.FAN_RPM_EXTRACT, 109),
        switch(PointKey.REHEAT_ENABLE, 2),
        setting(PointKey.FILTER_REPLACE_INTERVAL, 4, Limits(0, 6, step=1), unit=Unit.MONTHS),
        switch(PointKey.HUMIDITY_CONTROL_ENABLE, 5),
        setting(PointKey.TEMP_BYPASS_OPEN_OFFSET, 17, Limits(1, 10, step=0.1), data_type=DataType.INT16, scale=0.1,
                unit=Unit.CELSIUS),
        setting(PointKey.FAN_LEVEL, 100, Limits(0, 4, step=1), on_write=fan_level_rereads(
            PointKey.FAN_DUTYCYCLE_SUPPLY, PointKey.FAN_DUTYCYCLE_EXTRACT, PointKey.FAN_RPM_SUPPLY,
            PointKey.FAN_RPM_EXTRACT)),
    )),
)
"""The Optima 250's, and the Optima 251's, which material published online gives the same."""

OPTIMA_250 = nilan_model("Optima 250", "Genvex", OPTIMA_250_SECTIONS)
OPTIMA_251 = nilan_model("Optima 251", "Genvex", OPTIMA_250_SECTIONS)


_SLAVE_79250_FAN_LEVEL = setting(PointKey.FAN_LEVEL, 100, Limits(0, 4, step=1), on_write=fan_level_rereads(
    PointKey.FAN_DUTYCYCLE_SUPPLY, PointKey.FAN_DUTYCYCLE_EXTRACT))

OPTIMA_301 = nilan_model("Optima 301", "Genvex", (
    section(reported=(
        *_SLAVE_79250_POINTS,
        optima_temperature(PointKey.TEMP_BEFORE_CONDENSER, 4),
        optima_temperature(PointKey.TEMP_EVAPORATOR, 5),
        optima_temperature(PointKey.TEMP_HOTWATER_TOP, 6),
        optima_temperature(PointKey.TEMP_HOTWATER_BOTTOM, 7),
        optima_temperature(PointKey.TEMP_ROOM, 9),
        setting(PointKey.COOLING_TEMPERATURE, 1, Limits(30, 100, step=1)),
        switch(PointKey.COOLING_ENABLE, 2),
        switch(PointKey.PREHEAT_ENABLE, 20),
        _SLAVE_79250_FAN_LEVEL,
    )),
))

OPTIMA_312 = nilan_model("Optima 312", "Genvex", (
    section(reported=(
        *_SLAVE_79250_POINTS,
        optima_temperature(PointKey.TEMP_BEFORE_CONDENSER, 4),
        optima_temperature(PointKey.TEMP_EVAPORATOR, 5),
        optima_temperature(PointKey.TEMP_HOTWATER_TOP, 6),
        optima_temperature(PointKey.TEMP_HOTWATER_BOTTOM, 7),
        optima_temperature(PointKey.TEMP_ROOM, 9),
        state(PointKey.HEAT_PUMP_ACTIVE, 11),
        state(PointKey.HEAT_PUMP_HEATER_ACTIVE, 12),
        state(PointKey.REHEAT_ACTIVE, 13),
        state(PointKey.DEFROST_ACTIVE, 14),
        state(PointKey.HEAT_PUMP_WATER_HEATING, 15),
        state(PointKey.HEAT_PUMP_ROOM_HEATING, 16),
        setting(PointKey.TEMP_HOTWATER, 1, Limits(0, 55, step=0.1), data_type=DataType.INT16, scale=0.1,
                unit=Unit.CELSIUS),
        switch(PointKey.HOTWATER_HEATER_ENABLE, 2),
        switch(PointKey.REHEAT_ENABLE, 21),
        _SLAVE_79250_FAN_LEVEL,
    )),
))


OPTIMA_260 = nilan_model("Optima 260", "Genvex", (
    section(reported=(
        optima_temperature(PointKey.TEMP_SUPPLY, 0),
        optima_temperature(PointKey.TEMP_OUTSIDE, 2),
        optima_temperature(PointKey.TEMP_EXHAUST, 3),
        optima_temperature(PointKey.TEMP_EXTRACT, 6),
        optima_percent(PointKey.FAN_DUTYCYCLE_SUPPLY, 9),
        optima_percent(PointKey.FAN_DUTYCYCLE_EXTRACT, 10),
        state(PointKey.BYPASS_ACTIVE, 11),
        reading(PointKey.HUMIDITY, 13, data_type=DataType.INT16, unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL, 0, Limits(0, 4, step=1), on_write=fan_level_rereads(
            PointKey.FAN_DUTYCYCLE_SUPPLY, PointKey.FAN_DUTYCYCLE_EXTRACT)),
        optima_target(2),
        *optima_fan_presets(7),
        setting(PointKey.TEMP_BYPASS_OPEN_OFFSET, 18, Limits(1, 10, step=0.1), data_type=DataType.INT16, scale=0.1,
                unit=Unit.CELSIUS),
        command(PointKey.FILTER_REPLACE_RESET, 47),
    )),
))


OPTIMA_270 = nilan_model("Optima 270", "Genvex", (
    section(verified=(
        optima_percent(PointKey.FAN_DUTYCYCLE_SUPPLY, 18, scale=0.01),
        optima_percent(PointKey.FAN_DUTYCYCLE_EXTRACT, 19, scale=0.01),
        optima_temperature(PointKey.TEMP_SUPPLY, 20),
        optima_temperature(PointKey.TEMP_OUTSIDE, 21),
        optima_temperature(PointKey.TEMP_EXHAUST, 22),
        optima_temperature(PointKey.TEMP_EXTRACT, 23),
        optima_temperature(PointKey.TEMP_FROST_PROTECTION, 24),
        reading(PointKey.HUMIDITY, 26, data_type=DataType.INT16, unit=Unit.PERCENT),
        optima_rpm(PointKey.FAN_RPM_SUPPLY, 35),
        optima_rpm(PointKey.FAN_RPM_EXTRACT, 36),
        reading(PointKey.BYPASS_POSITION, 40, data_type=DataType.INT16),
        optima_percent(PointKey.PREHEAT_OUTPUT, 41, scale=0.01),
        optima_percent(PointKey.REHEAT_OUTPUT, 42, scale=0.01),
        optima_rpm(PointKey.ROTOR_SPEED, 50),
        state(PointKey.BYPASS_ACTIVE, 53),
        reading(PointKey.ALARM_BITS, 114),
        reading(PointKey.ALARM_BITS_HIGH, 115),
        *ALARMS_270,
        optima_target(1, write_address=12),
        written_apart_switch(PointKey.REHEAT_ENABLE, 3),
        written_apart_switch(PointKey.HUMIDITY_CONTROL_ENABLE, 6),
        written_apart_fan_level(),
        written_apart_setting(PointKey.TEMP_BYPASS_OPEN_OFFSET, 21, Limits(1, 10, step=0.1), data_type=DataType.INT16,
                              scale=0.1, unit=Unit.CELSIUS),
        written_apart_setting(PointKey.TEMP_BYPASS_CLOSE_OFFSET, 29, Limits(0, 20, step=1), unit=Unit.CELSIUS),
        written_apart_switch(PointKey.BOOST_ENABLE, 30),
        command(PointKey.FILTER_REPLACE_RESET, 110),
        written_apart_setting(PointKey.BYPASS_FAN_INCREASE, 57, Limits(0, 100, step=1), unit=Unit.PERCENT),
        written_apart_setting(PointKey.TEMP_BYPASS_FAN_INCREASE_OFFSET, 58, Limits(0, 5, step=0.1),
                              data_type=DataType.INT16, scale=0.1, unit=Unit.CELSIUS),
        written_apart_setting(PointKey.BOOST_TIME, 70, Limits(1, 120, step=1), unit=Unit.MINUTES),
        # The user manual gives the filter timer in months, 0-12; this register was reported in days.
        written_apart_setting(PointKey.FILTER_REPLACE_INTERVAL, 100, None, unit=Unit.DAYS),
    )),
))

OPTIMA_314 = nilan_model("Optima 314", "Genvex", (
    section(reported=(
        state(PointKey.BYPASS_ACTIVE, 12),
        optima_percent(PointKey.FAN_DUTYCYCLE_SUPPLY, 18, scale=0.01),
        optima_percent(PointKey.FAN_DUTYCYCLE_EXTRACT, 19, scale=0.01),
        optima_temperature(PointKey.TEMP_SUPPLY, 20),
        optima_temperature(PointKey.TEMP_OUTSIDE, 21),
        optima_temperature(PointKey.TEMP_EXHAUST, 22),
        optima_temperature(PointKey.TEMP_HOTWATER_TOP, 23),
        # Datapoint 24 is sensor T8, which the user manual calls the tank bottom.
        optima_temperature(PointKey.TEMP_HOTWATER_BOTTOM, 24),
        reading(PointKey.HUMIDITY, 26, data_type=DataType.INT16, unit=Unit.PERCENT),
        optima_rpm(PointKey.FAN_RPM_SUPPLY, 35),
        optima_rpm(PointKey.FAN_RPM_EXTRACT, 36),
        state(PointKey.HEAT_PUMP_HEATER_ACTIVE, 58),
        optima_temperature(PointKey.TEMP_EXTRACT, 64),
        optima_temperature(PointKey.TEMP_BEFORE_CONDENSER, 65),
        optima_temperature(PointKey.TEMP_EVAPORATOR, 66),
        state(PointKey.HEAT_PUMP_ACTIVE, 75),
        reading(PointKey.ALARM_BITS, 114),
        reading(PointKey.ALARM_BITS_HIGH, 115),
        *ALARMS_314,
        optima_target(1, write_address=12),
        written_apart_switch(PointKey.REHEAT_ENABLE, 3),
        written_apart_switch(PointKey.HUMIDITY_CONTROL_ENABLE, 6),
        written_apart_fan_level(),
        written_apart_switch(PointKey.BOOST_ENABLE, 30),
        command(PointKey.FILTER_REPLACE_RESET, 110),
        written_apart_setting(PointKey.BOOST_TIME, 70, Limits(1, 120, step=1), unit=Unit.MINUTES),
        # The user manual gives the filter timer in months, 0-12; this register was reported in days.
        written_apart_setting(PointKey.FILTER_REPLACE_INTERVAL, 100, None, unit=Unit.DAYS),
        written_apart_setting(PointKey.TEMP_HOTWATER, 122, Limits(0, 55, step=0.1), data_type=DataType.INT16,
                              scale=0.1, unit=Unit.CELSIUS),
    )),
))
