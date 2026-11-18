"""Genvex's Optima 314 as a model: its points, and how its gateway is talked to over micro_nabto.

Sources:
    No Modbus description of an Optima is published. The gateway's addresses, scales and
    ranges were found in material published online. The user manuals in this repository's
    docs/models/genvex-optima name the sensors and the settings' ranges.
"""
from __future__ import annotations

from modbus_event_connect import DataType, Limits, Point, PollRate, Unit
from modbus_event_connect.micro_nabto import MicroNabtoModel

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
from ._points import alarm_bit, command, reading, section, state
from ._shared import (
    ANSWER_WAIT,
    FAST_INTERVAL,
    LATER_ANSWER_WAIT,
    MAX_REGISTERS,
    READ_BACK_AFTER,
    SLOW_INTERVAL,
    WRITE_RETRY,
    ZEROS,
)

# The alarm bits, as found in material published online. The filter alarm's bit is set while the
# filter must be changed, so it is `filter_ok` inverted, as every controller has that key.
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


OPTIMA_314 = MicroNabtoModel(
    "Optima 314", "Genvex", (
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
            optima_target(1, write_address=optima_write_address(1)),
            optima_270_switch(PointKey.REHEAT_ENABLE, 3),
            optima_270_switch(PointKey.HUMIDITY_CONTROL_ENABLE, 6),
            optima_270_fan_level(),
            optima_270_switch(PointKey.BOOST_ENABLE, 30),
            command(PointKey.FILTER_REPLACE_RESET, 110),
            optima_270_setting(PointKey.BOOST_TIME, 70, Limits(1, 120, step=1), unit=Unit.MINUTES),
            # The user manual gives the filter timer in months, 0-12; this register was reported in days.
            optima_270_setting(PointKey.FILTER_REPLACE_INTERVAL, 100, None, unit=Unit.DAYS),
            optima_270_setting(PointKey.TEMP_HOTWATER, 122, Limits(0, 55, step=0.1), data_type=DataType.INT16,
                               scale=0.1, unit=Unit.CELSIUS),
        )),
    ),
    poll_intervals={
        PollRate.FAST: FAST_INTERVAL,
        PollRate.SLOW: SLOW_INTERVAL,
    },
    read_back_after=READ_BACK_AFTER,
    write_retry=WRITE_RETRY,
    scan_check=None,
    identity_points=(),
    scan_steps=(),
    max_registers=MAX_REGISTERS,
    answer_wait=ANSWER_WAIT,
    later_answer_wait=LATER_ANSWER_WAIT,
    zeros=ZEROS,
)
"""Genvex's Optima 314, as its gateway is talked to over micro_nabto."""
