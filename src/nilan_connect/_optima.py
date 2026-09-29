"""Genvex's Optima controllers as models.

Sources:
    No Modbus description of an Optima is published. The gateway's addresses, scales and
    ranges were found in material published online; the Optima 270's have been read on a unit,
    the others' are untested. The user manuals in this repository's docs/models/genvex-optima name
    the sensors.
"""
from __future__ import annotations

from modbus_event_connect import DataType, Limits, Model, PollRate, Section, Unit
from modbus_event_connect.micro_nabto import MicroNabtoOptions

from ._model import (
    PointKey,
    Source,
    command,
    labelled,
    reading,
    setting,
    state,
    switch,
    temperature,
)


OPTIMA_250_SECTIONS: tuple[Section, ...] = (
    Section(labelled(Source.UNTESTED, (
        temperature(PointKey.TEMP_SUPPLY, 0, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_OUTSIDE, 2, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_EXHAUST, 3, scale=0.1, offset=-30),
        temperature(PointKey.TEMP_EXTRACT, 6, scale=0.1, offset=-30),
        reading(PointKey.HUMIDITY, 10, data_type=DataType.INT16, unit=Unit.PERCENT),
        reading(PointKey.ALARM_BITS, 101),
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
        reading(PointKey.BYPASS_POSITION, 40, data_type=DataType.INT16, unit=Unit.PERCENT),
        reading(PointKey.PREHEAT_OUTPUT, 41, data_type=DataType.INT16, scale=0.01, unit=Unit.PERCENT),
        reading(PointKey.REHEAT_OUTPUT, 42, data_type=DataType.INT16, scale=0.01, unit=Unit.PERCENT),
        reading(PointKey.ROTOR_SPEED, 50, data_type=DataType.INT16, unit=Unit.RPM),
        state(PointKey.BYPASS_ACTIVE, 53),
        reading(PointKey.ALARM_BITS, 114),
        reading(PointKey.ALARM_BITS_HIGH, 115),
        setting(PointKey.TEMP_TARGET, 1, Limits(10, 30, step=0.5), write_address=12, data_type=DataType.INT16, scale=0.1, offset=10, unit=Unit.CELSIUS),
        switch(PointKey.REHEAT_ENABLE, 3, write_address=16),
        switch(PointKey.HUMIDITY_CONTROL_ENABLE, 6, write_address=22),
        setting(PointKey.FAN_LEVEL, 7, Limits(0, 4, step=1), write_address=24),
        setting(PointKey.TEMP_BYPASS_OPEN_OFFSET, 21, Limits(1, 10, step=0.1), write_address=52, data_type=DataType.INT16, scale=0.1, unit=Unit.CELSIUS),
        setting(PointKey.BYPASS_TURNOFF, 29, Limits(0, 20, step=1), write_address=68),
        switch(PointKey.BOOST_ENABLE, 30, write_address=70),
        command(PointKey.FILTER_REPLACE_RESET, 110),
        setting(PointKey.BYPASS_FAN_LEVEL, 57, Limits(0, 100, step=1), write_address=124, unit=Unit.PERCENT),
        setting(PointKey.TEMP_BYPASS_FORCE, 58, Limits(0, 5, step=0.1), write_address=126, data_type=DataType.INT16, scale=0.1, unit=Unit.CELSIUS),
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
        reading(PointKey.FAN_DUTYCYCLE_SUPPLY, 102, data_type=DataType.INT16, unit=Unit.PERCENT),
        reading(PointKey.FAN_DUTYCYCLE_EXTRACT, 103, data_type=DataType.INT16, unit=Unit.PERCENT),
        state(PointKey.BYPASS_ACTIVE, 104),
        setting(PointKey.TEMP_TARGET, 0, Limits(10, 30, step=0.5), data_type=DataType.INT16, scale=0.1, offset=10, unit=Unit.CELSIUS),
        setting(PointKey.TEMP_COOLING_START_OFFSET, 1, Limits(30, 100, step=1)),
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
