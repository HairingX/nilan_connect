"""Genvex's Optima 270 as a model, and how it is talked to over micro_nabto.

Sources:
    No Modbus description of an Optima is published. The gateway's addresses, scales and
    ranges were found in material published online. The user manuals in this repository's
    docs/models/genvex-optima name the sensors and the settings' ranges.
"""
from __future__ import annotations

from modbus_event_connect import DataType, Limits, Model, Point, Unit
from modbus_event_connect.micro_nabto import MicroNabtoProfile

from ._keys import PointKey
from ._optima import (
    optima_270_fan_level,
    optima_270_setting,
    optima_270_switch,
    optima_percent,
    optima_rpm,
    optima_target,
    optima_temperature,
    optima_write_address,
)
from ._points import GATEWAY_TIMING, GATEWAY_ZEROS, alarm_bit, command, reading, section, state

# The alarm bits, as found in material published online. The filter alarm's bit is set while the
# filter must be changed, so it is `filter_ok` inverted, as every controller has that key.
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


OPTIMA_270 = Model("Optima 270", "Genvex", (
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
        optima_target(1, write_address=optima_write_address(1)),
        optima_270_switch(PointKey.REHEAT_ENABLE, 3),
        optima_270_switch(PointKey.HUMIDITY_CONTROL_ENABLE, 6),
        optima_270_fan_level(),
        optima_270_setting(PointKey.TEMP_BYPASS_OPEN_OFFSET, 21, Limits(1, 10, step=0.1), data_type=DataType.INT16,
                           scale=0.1, unit=Unit.CELSIUS),
        optima_270_setting(PointKey.TEMP_BYPASS_CLOSE_OFFSET, 29, Limits(0, 20, step=1), unit=Unit.CELSIUS),
        optima_270_switch(PointKey.BOOST_ENABLE, 30),
        command(PointKey.FILTER_REPLACE_RESET, 110),
        optima_270_setting(PointKey.BYPASS_FAN_INCREASE, 57, Limits(0, 100, step=1), unit=Unit.PERCENT),
        optima_270_setting(PointKey.TEMP_BYPASS_FAN_INCREASE_OFFSET, 58, Limits(0, 5, step=0.1),
                           data_type=DataType.INT16, scale=0.1, unit=Unit.CELSIUS),
        optima_270_setting(PointKey.BOOST_TIME, 70, Limits(1, 120, step=1), unit=Unit.MINUTES),
        # The user manual gives the filter timer in months, 0-12; this register was reported in days.
        optima_270_setting(PointKey.FILTER_REPLACE_INTERVAL, 100, None, unit=Unit.DAYS),
    )),
), timing=GATEWAY_TIMING)

OPTIMA_270_MICRO_NABTO = MicroNabtoProfile(
    model=OPTIMA_270,
    max_registers=64,           # a CTS 402 answered 108, so this leaves room
    later_answer_wait=5.0,      # not measured on this controller, so longer than a CTS400's
    zeros=GATEWAY_ZEROS,
)
