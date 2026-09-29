"""Genvex's Optima controllers as models.

Sources:
    No Modbus description of an Optima is published. The gateway's addresses, scales and
    ranges were found in material published online; the Optima 270's have been read on a unit,
    the others' are untested. The user manuals in this repository's docs/models/genvex-optima name
    the sensors.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from modbus_event_connect import DataType, Key, Limits, Model, Point, PollRate, Section, Unit
from modbus_event_connect.micro_nabto import MicroNabtoOptions

from ._model import (
    PointKey,
    Source,
    alarm_bit,
    command,
    labelled,
    reading,
    setting,
    state,
    switch,
    temperature,
)

# Which alarm each bit of an Optima's alarm registers raises, as found in material published online.
# A 32-bit field spans two registers, the lower bits first. The filter alarm is `filter_ok`, the
# other way round, as a CTS400 has it.
_FILTER = PointKey.FILTER_OK

ALARM_BITS_250: Mapping[int, Key[bool]] = {
    0: PointKey.ALARM_EXTERNAL_STOP, 1: _FILTER, 2: PointKey.ALARM_HIGH_PRESSURE, 3: PointKey.ALARM_FROST_FAILURE,
    4: PointKey.ALARM_PANEL_COMMUNICATION, 5: PointKey.ALARM_EXTERNAL_FILTER, 6: PointKey.ALARM_FAN_ERROR,
    7: PointKey.ALARM_SENSOR_ERROR,
}
"""The Optima 250, 251, 301 and 312."""

_SENSOR_T1_T9: tuple[Key[bool], ...] = (
    PointKey.ALARM_SENSOR_T1_ERROR, PointKey.ALARM_SENSOR_T2_ERROR, PointKey.ALARM_SENSOR_T3_ERROR,
    PointKey.ALARM_SENSOR_T4_ERROR, PointKey.ALARM_SENSOR_T5_ERROR, PointKey.ALARM_SENSOR_T6_ERROR,
    PointKey.ALARM_SENSOR_T7_ERROR, PointKey.ALARM_SENSOR_T8_ERROR, PointKey.ALARM_SENSOR_T9_ERROR,
)
_FIRE_DAMPERS: tuple[Key[bool], ...] = (
    PointKey.ALARM_FIRE_DAMPER_1_ERROR, PointKey.ALARM_FIRE_DAMPER_2_ERROR, PointKey.ALARM_FIRE_DAMPER_3_ERROR,
    PointKey.ALARM_FIRE_DAMPER_4_ERROR,
)

ALARM_BITS_270: Mapping[int, Key[bool]] = {
    0: _FILTER, 1: PointKey.ALARM_EXTERNAL_STOP, **{2 + n: key for n, key in enumerate(_SENSOR_T1_T9)},
    11: PointKey.ALARM_HUMIDITY_SENSOR_ERROR, 12: PointKey.ALARM_FIRE_TEST_ERROR,
    13: PointKey.ALARM_SUPPLY_FAN_ERROR, 14: PointKey.ALARM_EXTRACT_FAN_ERROR, 15: PointKey.ALARM_FROST_FAILURE,
    **{16 + n: key for n, key in enumerate(_FIRE_DAMPERS)}, 20: PointKey.ALARM_FIRE_BOX_1_ERROR,
    21: PointKey.ALARM_FIRE_BOX_2_ERROR, 22: PointKey.ALARM_ROTOR,
}

ALARM_BITS_314: Mapping[int, Key[bool]] = {
    1: _FILTER, 2: PointKey.ALARM_EXTERNAL_STOP, **{3 + n: key for n, key in enumerate(_SENSOR_T1_T9)},
    12: PointKey.ALARM_HUMIDITY_SENSOR_ERROR, 13: PointKey.ALARM_FIRE_TEST_ERROR,
    14: PointKey.ALARM_SUPPLY_FAN_ERROR, 15: PointKey.ALARM_EXTRACT_FAN_ERROR,
    **{17 + n: key for n, key in enumerate(_FIRE_DAMPERS)}, 21: PointKey.ALARM_FIRE_BOX_1_ERROR,
    22: PointKey.ALARM_FIRE_BOX_2_ERROR, 24: PointKey.ALARM_INTERNAL_MODBUS, 25: PointKey.ALARM_HIGH_PRESSURE,
    26: PointKey.ALARM_LOW_PRESSURE, 27: PointKey.ALARM_FLOW_TEMPERATURE_ERROR,
    28: PointKey.ALARM_RETURN_TEMPERATURE_ERROR, 29: PointKey.ALARM_SENSOR_T10_ERROR,
    30: PointKey.ALARM_SENSOR_T11_ERROR,
}


def alarm_bits(bits: Mapping[int, Key[bool]], address: int) -> tuple[Point[Any], ...]:
    """A point for each alarm of the field starting at `address`, the filter alarm inverted."""
    return tuple(alarm_bit(key, address + bit // 16, bit % 16, inverted=key == _FILTER) for bit, key in bits.items())


OPTIMA_250_SECTIONS: tuple[Section, ...] = (
    Section(labelled(Source.UNTESTED, (
        temperature(PointKey.TEMP_SUPPLY, 0, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_OUTSIDE, 2, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_EXHAUST, 3, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_EXTRACT, 6, scale=0.1, offset=-30),
        reading(PointKey.HUMIDITY, 10, data_type=DataType.INT16, unit=Unit.PERCENT),
        reading(PointKey.ALARM_BITS, 101),
        *alarm_bits(ALARM_BITS_250, 101),
        reading(PointKey.FAN_DUTYCYCLE_SUPPLY, 102, data_type=DataType.INT16, unit=Unit.PERCENT),
        reading(PointKey.FAN_DUTYCYCLE_EXTRACT, 103, data_type=DataType.INT16, unit=Unit.PERCENT),
        state(PointKey.BYPASS_ACTIVE, 104),
        reading(PointKey.FAN_RPM_SUPPLY, 108, data_type=DataType.INT16, unit=Unit.RPM),
        reading(PointKey.FAN_RPM_EXTRACT, 109, data_type=DataType.INT16, unit=Unit.RPM),
        setting(PointKey.TEMP_TARGET, 0, Limits(10, 30, step=0.5), data_type=DataType.INT16, scale=0.1, offset=10, unit=Unit.CELSIUS),
        switch(PointKey.REHEAT_ENABLE, 2),
        setting(PointKey.FILTER_REPLACE_INTERVAL, 4, Limits(0, 6, step=1), unit=Unit.MONTHS),
        switch(PointKey.HUMIDITY_CONTROL_ENABLE, 5),
        setting(PointKey.FAN_LEVEL1_SUPPLY_PRESET, 6, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL2_SUPPLY_PRESET, 7, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL3_SUPPLY_PRESET, 8, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL1_EXTRACT_PRESET, 9, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL2_EXTRACT_PRESET, 10, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL3_EXTRACT_PRESET, 11, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.TEMP_BYPASS_OPEN_OFFSET, 17, Limits(1, 10, step=0.1), data_type=DataType.INT16, scale=0.1, unit=Unit.CELSIUS),
        setting(PointKey.FAN_LEVEL, 100, Limits(0, 4, step=1)),
        command(PointKey.FILTER_REPLACE_RESET, 105),
    ))),
)

OPTIMA_250 = Model(
    "Optima 250", "Genvex", OPTIMA_250_SECTIONS,
    options=MicroNabtoOptions(),
    poll_intervals={PollRate.FAST: 10.0, PollRate.SLOW: 180.0},
    read_back_after=1.0,
)


OPTIMA_251_SECTIONS: tuple[Section, ...] = (
    Section(labelled(Source.UNTESTED, (
        temperature(PointKey.TEMP_SUPPLY, 0, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_OUTSIDE, 2, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_EXHAUST, 3, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_EXTRACT, 6, scale=0.1, offset=-30),
        reading(PointKey.HUMIDITY, 10, data_type=DataType.INT16, unit=Unit.PERCENT),
        reading(PointKey.ALARM_BITS, 101),
        *alarm_bits(ALARM_BITS_250, 101),
        reading(PointKey.FAN_DUTYCYCLE_SUPPLY, 102, data_type=DataType.INT16, unit=Unit.PERCENT),
        reading(PointKey.FAN_DUTYCYCLE_EXTRACT, 103, data_type=DataType.INT16, unit=Unit.PERCENT),
        state(PointKey.BYPASS_ACTIVE, 104),
        reading(PointKey.FAN_RPM_SUPPLY, 108, data_type=DataType.INT16, unit=Unit.RPM),
        reading(PointKey.FAN_RPM_EXTRACT, 109, data_type=DataType.INT16, unit=Unit.RPM),
        setting(PointKey.TEMP_TARGET, 0, Limits(10, 30, step=0.5), data_type=DataType.INT16, scale=0.1, offset=10, unit=Unit.CELSIUS),
        switch(PointKey.REHEAT_ENABLE, 2),
        setting(PointKey.FILTER_REPLACE_INTERVAL, 4, Limits(0, 6, step=1), unit=Unit.MONTHS),
        switch(PointKey.HUMIDITY_CONTROL_ENABLE, 5),
        setting(PointKey.FAN_LEVEL1_SUPPLY_PRESET, 6, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL2_SUPPLY_PRESET, 7, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL3_SUPPLY_PRESET, 8, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL1_EXTRACT_PRESET, 9, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL2_EXTRACT_PRESET, 10, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL3_EXTRACT_PRESET, 11, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.TEMP_BYPASS_OPEN_OFFSET, 17, Limits(1, 10, step=0.1), data_type=DataType.INT16, scale=0.1, unit=Unit.CELSIUS),
        setting(PointKey.FAN_LEVEL, 100, Limits(0, 4, step=1)),
        command(PointKey.FILTER_REPLACE_RESET, 105),
    ))),
)

OPTIMA_251 = Model(
    "Optima 251", "Genvex", OPTIMA_251_SECTIONS,
    options=MicroNabtoOptions(),
    poll_intervals={PollRate.FAST: 10.0, PollRate.SLOW: 180.0},
    read_back_after=1.0,
)


OPTIMA_260_SECTIONS: tuple[Section, ...] = (
    Section(labelled(Source.UNTESTED, (
        temperature(PointKey.TEMP_SUPPLY, 0, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_OUTSIDE, 2, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_EXHAUST, 3, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_EXTRACT, 6, scale=0.1, offset=-30),
        reading(PointKey.FAN_DUTYCYCLE_SUPPLY, 9, data_type=DataType.INT16, unit=Unit.PERCENT),
        reading(PointKey.FAN_DUTYCYCLE_EXTRACT, 10, data_type=DataType.INT16, unit=Unit.PERCENT),
        state(PointKey.BYPASS_ACTIVE, 11),
        reading(PointKey.HUMIDITY, 13, data_type=DataType.INT16, unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL, 0, Limits(0, 4, step=1)),
        setting(PointKey.TEMP_TARGET, 2, Limits(10, 30, step=0.5), data_type=DataType.INT16, scale=0.1, offset=10, unit=Unit.CELSIUS),
        setting(PointKey.FILTER_REPLACE_INTERVAL, 5, Limits(0, 12, step=1), unit=Unit.MONTHS),
        switch(PointKey.HUMIDITY_CONTROL_ENABLE, 5),
        setting(PointKey.FAN_LEVEL1_SUPPLY_PRESET, 7, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL2_SUPPLY_PRESET, 8, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL3_SUPPLY_PRESET, 9, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL1_EXTRACT_PRESET, 10, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL2_EXTRACT_PRESET, 11, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL3_EXTRACT_PRESET, 12, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.TEMP_BYPASS_OPEN_OFFSET, 18, Limits(1, 10, step=0.1), data_type=DataType.INT16, scale=0.1, unit=Unit.CELSIUS),
        command(PointKey.FILTER_REPLACE_RESET, 47),
    ))),
)

OPTIMA_260 = Model(
    "Optima 260", "Genvex", OPTIMA_260_SECTIONS,
    options=MicroNabtoOptions(),
    poll_intervals={PollRate.FAST: 10.0, PollRate.SLOW: 180.0},
    read_back_after=1.0,
)


OPTIMA_270_SECTIONS: tuple[Section, ...] = (
    Section(labelled(Source.TESTED, (
        reading(PointKey.FAN_DUTYCYCLE_SUPPLY, 18, data_type=DataType.INT16, scale=0.01, unit=Unit.PERCENT),
        reading(PointKey.FAN_DUTYCYCLE_EXTRACT, 19, data_type=DataType.INT16, scale=0.01, unit=Unit.PERCENT),
        temperature(PointKey.TEMP_SUPPLY, 20, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_OUTSIDE, 21, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_EXHAUST, 22, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_EXTRACT, 23, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_FROST_PROTECTION, 24, scale=0.1, offset=-30),
        reading(PointKey.HUMIDITY, 26, data_type=DataType.INT16, unit=Unit.PERCENT),
        reading(PointKey.FAN_RPM_SUPPLY, 35, data_type=DataType.INT16, unit=Unit.RPM),
        reading(PointKey.FAN_RPM_EXTRACT, 36, data_type=DataType.INT16, unit=Unit.RPM),
        reading(PointKey.BYPASS_POSITION, 40, data_type=DataType.INT16),
        reading(PointKey.PREHEAT_OUTPUT, 41, data_type=DataType.INT16, scale=0.01, unit=Unit.PERCENT),
        reading(PointKey.REHEAT_OUTPUT, 42, data_type=DataType.INT16, scale=0.01, unit=Unit.PERCENT),
        reading(PointKey.ROTOR_SPEED, 50, data_type=DataType.INT16, unit=Unit.RPM),
        state(PointKey.BYPASS_ACTIVE, 53),
        reading(PointKey.ALARM_BITS, 114),
        reading(PointKey.ALARM_BITS_HIGH, 115),
        *alarm_bits(ALARM_BITS_270, 114),
        setting(PointKey.TEMP_TARGET, 1, Limits(10, 30, step=0.5), write_address=12, data_type=DataType.INT16, scale=0.1, offset=10, unit=Unit.CELSIUS),
        switch(PointKey.REHEAT_ENABLE, 3, write_address=16),
        switch(PointKey.HUMIDITY_CONTROL_ENABLE, 6, write_address=22),
        setting(PointKey.FAN_LEVEL, 7, Limits(0, 4, step=1), write_address=24),
        setting(PointKey.TEMP_BYPASS_OPEN_OFFSET, 21, Limits(1, 10, step=0.1), write_address=52, data_type=DataType.INT16, scale=0.1, unit=Unit.CELSIUS),
        setting(PointKey.TEMP_BYPASS_CLOSE_OFFSET, 29, Limits(0, 20, step=1), write_address=68, unit=Unit.CELSIUS),
        switch(PointKey.BOOST_ENABLE, 30, write_address=70),
        command(PointKey.FILTER_REPLACE_RESET, 110),
        setting(PointKey.BYPASS_FAN_INCREASE, 57, Limits(0, 100, step=1), write_address=124, unit=Unit.PERCENT),
        setting(PointKey.TEMP_BYPASS_FAN_INCREASE_OFFSET, 58, Limits(0, 5, step=0.1), write_address=126, data_type=DataType.INT16, scale=0.1, unit=Unit.CELSIUS),
        setting(PointKey.BOOST_TIME, 70, Limits(1, 120, step=1), write_address=150, unit=Unit.MINUTES),
        setting(PointKey.FILTER_REPLACE_INTERVAL, 100, Limits(0, 65535, step=1), write_address=210, unit=Unit.DAYS),
    ))),
)

OPTIMA_270 = Model(
    "Optima 270", "Genvex", OPTIMA_270_SECTIONS,
    options=MicroNabtoOptions(),
    poll_intervals={PollRate.FAST: 10.0, PollRate.SLOW: 180.0},
    read_back_after=1.0,
)


OPTIMA_301_SECTIONS: tuple[Section, ...] = (
    Section(labelled(Source.UNTESTED, (
        temperature(PointKey.TEMP_SUPPLY, 0, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_OUTSIDE, 2, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_EXHAUST, 3, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_BEFORE_CONDENSER, 4, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_EVAPORATOR, 5, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_HOTWATER_TOP, 6, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_HOTWATER_BOTTOM, 7, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_ROOM, 9, scale=0.1, offset=-30),
        reading(PointKey.HUMIDITY, 10, data_type=DataType.INT16, unit=Unit.PERCENT),
        reading(PointKey.ALARM_BITS, 101),
        *alarm_bits(ALARM_BITS_250, 101),
        reading(PointKey.FAN_DUTYCYCLE_SUPPLY, 102, data_type=DataType.INT16, unit=Unit.PERCENT),
        reading(PointKey.FAN_DUTYCYCLE_EXTRACT, 103, data_type=DataType.INT16, unit=Unit.PERCENT),
        state(PointKey.BYPASS_ACTIVE, 104),
        setting(PointKey.TEMP_TARGET, 0, Limits(10, 30, step=0.5), data_type=DataType.INT16, scale=0.1, offset=10, unit=Unit.CELSIUS),
        setting(PointKey.COOLING_TEMPERATURE, 1, Limits(30, 100, step=1)),
        switch(PointKey.COOLING_ENABLE, 2),
        setting(PointKey.FAN_LEVEL1_SUPPLY_PRESET, 6, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL2_SUPPLY_PRESET, 7, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL3_SUPPLY_PRESET, 8, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL1_EXTRACT_PRESET, 9, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL2_EXTRACT_PRESET, 10, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL3_EXTRACT_PRESET, 11, Limits(0, 100, step=1), unit=Unit.PERCENT),
        switch(PointKey.PREHEAT_ENABLE, 20),
        setting(PointKey.FAN_LEVEL, 100, Limits(0, 4, step=1)),
        command(PointKey.FILTER_REPLACE_RESET, 105),
    ))),
)

OPTIMA_301 = Model(
    "Optima 301", "Genvex", OPTIMA_301_SECTIONS,
    options=MicroNabtoOptions(),
    poll_intervals={PollRate.FAST: 10.0, PollRate.SLOW: 180.0},
    read_back_after=1.0,
)


OPTIMA_312_SECTIONS: tuple[Section, ...] = (
    Section(labelled(Source.UNTESTED, (
        temperature(PointKey.TEMP_SUPPLY, 0, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_OUTSIDE, 2, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_EXHAUST, 3, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_BEFORE_CONDENSER, 4, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_EVAPORATOR, 5, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_HOTWATER_TOP, 6, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_HOTWATER_BOTTOM, 7, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_ROOM, 9, scale=0.1, offset=-30),
        reading(PointKey.HUMIDITY, 10, data_type=DataType.INT16, unit=Unit.PERCENT),
        state(PointKey.HEAT_PUMP_ACTIVE, 11),
        state(PointKey.HEAT_PUMP_HEATER_ACTIVE, 12),
        state(PointKey.REHEAT_ACTIVE, 13),
        state(PointKey.DEFROST_ACTIVE, 14),
        state(PointKey.HEAT_PUMP_WATER_HEATING, 15),
        state(PointKey.HEAT_PUMP_ROOM_HEATING, 16),
        reading(PointKey.ALARM_BITS, 101),
        *alarm_bits(ALARM_BITS_250, 101),
        reading(PointKey.FAN_DUTYCYCLE_SUPPLY, 102, data_type=DataType.INT16, unit=Unit.PERCENT),
        reading(PointKey.FAN_DUTYCYCLE_EXTRACT, 103, data_type=DataType.INT16, unit=Unit.PERCENT),
        state(PointKey.BYPASS_ACTIVE, 104),
        setting(PointKey.TEMP_TARGET, 0, Limits(10, 30, step=0.5), data_type=DataType.INT16, scale=0.1, offset=10, unit=Unit.CELSIUS),
        setting(PointKey.TEMP_HOTWATER, 1, Limits(0, 55, step=0.1), data_type=DataType.INT16, scale=0.1, unit=Unit.CELSIUS),
        switch(PointKey.HOTWATER_HEATER_ENABLE, 2),
        setting(PointKey.FAN_LEVEL1_SUPPLY_PRESET, 6, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL2_SUPPLY_PRESET, 7, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL3_SUPPLY_PRESET, 8, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL1_EXTRACT_PRESET, 9, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL2_EXTRACT_PRESET, 10, Limits(0, 100, step=1), unit=Unit.PERCENT),
        setting(PointKey.FAN_LEVEL3_EXTRACT_PRESET, 11, Limits(0, 100, step=1), unit=Unit.PERCENT),
        switch(PointKey.REHEAT_ENABLE, 21),
        setting(PointKey.FAN_LEVEL, 100, Limits(0, 4, step=1)),
        command(PointKey.FILTER_REPLACE_RESET, 105),
    ))),
)

OPTIMA_312 = Model(
    "Optima 312", "Genvex", OPTIMA_312_SECTIONS,
    options=MicroNabtoOptions(),
    poll_intervals={PollRate.FAST: 10.0, PollRate.SLOW: 180.0},
    read_back_after=1.0,
)


OPTIMA_314_SECTIONS: tuple[Section, ...] = (
    Section(labelled(Source.UNTESTED, (
        state(PointKey.BYPASS_ACTIVE, 12),
        reading(PointKey.FAN_DUTYCYCLE_SUPPLY, 18, data_type=DataType.INT16, scale=0.01, unit=Unit.PERCENT),
        reading(PointKey.FAN_DUTYCYCLE_EXTRACT, 19, data_type=DataType.INT16, scale=0.01, unit=Unit.PERCENT),
        temperature(PointKey.TEMP_SUPPLY, 20, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_OUTSIDE, 21, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_EXHAUST, 22, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_HOTWATER_TOP, 23, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_FROST_PROTECTION, 24, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_HOTWATER_BOTTOM, 24, scale=0.1, offset=-30),
        reading(PointKey.HUMIDITY, 26, data_type=DataType.INT16, unit=Unit.PERCENT),
        reading(PointKey.FAN_RPM_SUPPLY, 35, data_type=DataType.INT16, unit=Unit.RPM),
        reading(PointKey.FAN_RPM_EXTRACT, 36, data_type=DataType.INT16, unit=Unit.RPM),
        state(PointKey.HEAT_PUMP_HEATER_ACTIVE, 58),
        temperature(PointKey.TEMP_EXTRACT, 64, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_BEFORE_CONDENSER, 65, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_EVAPORATOR, 66, scale=0.1, offset=-30),
        state(PointKey.HEAT_PUMP_ACTIVE, 75),
        reading(PointKey.ALARM_BITS, 114),
        reading(PointKey.ALARM_BITS_HIGH, 115),
        *alarm_bits(ALARM_BITS_314, 114),
        setting(PointKey.TEMP_TARGET, 1, Limits(10, 30, step=0.5), write_address=12, data_type=DataType.INT16, scale=0.1, offset=10, unit=Unit.CELSIUS),
        switch(PointKey.REHEAT_ENABLE, 3, write_address=16),
        switch(PointKey.HUMIDITY_CONTROL_ENABLE, 6, write_address=22),
        setting(PointKey.FAN_LEVEL, 7, Limits(0, 4, step=1), write_address=24),
        switch(PointKey.BOOST_ENABLE, 30, write_address=70),
        command(PointKey.FILTER_REPLACE_RESET, 110),
        setting(PointKey.BOOST_TIME, 70, Limits(1, 120, step=1), write_address=150, unit=Unit.MINUTES),
        setting(PointKey.FILTER_REPLACE_INTERVAL, 100, Limits(0, 65535, step=1), write_address=210, unit=Unit.DAYS),
        setting(PointKey.TEMP_HOTWATER, 122, Limits(0, 55, step=0.1), write_address=254, data_type=DataType.INT16, scale=0.1, unit=Unit.CELSIUS),
    ))),
)

OPTIMA_314 = Model(
    "Optima 314", "Genvex", OPTIMA_314_SECTIONS,
    options=MicroNabtoOptions(),
    poll_intervals={PollRate.FAST: 10.0, PollRate.SLOW: 180.0},
    read_back_after=1.0,
)
