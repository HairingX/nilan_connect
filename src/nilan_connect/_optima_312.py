"""Genvex's Optima 312 as a model: its points, and how its gateway is talked to over micro_nabto.

Sources:
    The gateway's addresses, scales and ranges were found in material published online. Genvex's
    Modbus register workbook, posted at
    https://community.openenergymonitor.org/t/reverse-engineer-heatpump-genvex-combi-185/15992/46,
    has an 'Optima 311-312' sheet; the gateway's datapoint and setpoint numbers are taken to be
    its register numbers. The user manual in this repository's docs/models/genvex-optima names
    the sensors and the settings' ranges.
"""
from __future__ import annotations

from modbus_event_connect import DataType, Limits, PollRate, Unit
from modbus_event_connect.micro_nabto import MicroNabtoModel

from ._keys import PointKey
from ._optima import SLAVE_79250_FAN_LEVEL, SLAVE_79250_POINTS, optima_temperature
from ._points import section, setpoint_bit, setpoint_reading, setting, state, switch
from ._shared import (
    ANSWER_WAIT,
    FAST_INTERVAL,
    LATER_ANSWER_WAIT,
    MAX_REGISTERS,
    READ_BACK_AFTER,
    SLOW_INTERVAL,
    WRITE_RETRY,
    WRITE_TAKEN,
    ZEROS,
)

OPTIMA_312 = MicroNabtoModel(
    "Optima 312", "Genvex", (
        section(reported=(
            *SLAVE_79250_POINTS,
            # reported: T5, which the user manual calls "Before cooling coil"; T6 is the cooling coil
            optima_temperature(PointKey.TEMP_BEFORE_EVAPORATOR, 4),
            optima_temperature(PointKey.TEMP_EVAPORATOR, 5),
            optima_temperature(PointKey.TEMP_HOTWATER_TOP, 6),
            optima_temperature(PointKey.TEMP_HOTWATER_BOTTOM, 7),
            optima_temperature(PointKey.TEMP_ROOM_PANEL, 9),  # reported: the workbook's 3x0009 "T2 Panel"
            state(PointKey.HEAT_PUMP_ACTIVE, 11),
            state(PointKey.HEAT_PUMP_HEATER_ACTIVE, 12),
            state(PointKey.REHEAT_ACTIVE, 13),
            state(PointKey.DEFROST_ACTIVE, 14),
            state(PointKey.HEAT_PUMP_WATER_HEATING, 15),
            state(PointKey.HEAT_PUMP_ROOM_HEATING, 16),
            setting(PointKey.TEMP_HOTWATER, 1, Limits(0, 55, step=0.1), data_type=DataType.INT16, scale=0.1,
                    unit=Unit.CELSIUS),
            switch(PointKey.HOTWATER_HEATER_ENABLE, 2),
            # reported: the user manual's item 25, "Electric heating coil": 0 none installed, 1 an
            # electric reheater, 2 an electric preheater, 0-2; the workbook's 4x0021, 0-2. An
            # installation fact, so only read.
            setpoint_reading(PointKey.ELECTRIC_COIL, 21),
            # As the setting holds 0, 1 or 2, bit 0 is set for a reheater alone and bit 1 for a preheater.
            setpoint_bit(PointKey.REHEAT_COIL_FITTED, 21, 0),
            setpoint_bit(PointKey.PREHEAT_COIL_FITTED, 21, 1),
            SLAVE_79250_FAN_LEVEL,
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
    write_taken=WRITE_TAKEN,
)
"""Genvex's Optima 312, as its gateway is talked to over micro_nabto."""
