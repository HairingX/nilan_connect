"""Genvex's Optima 301 as a model: its points, and how its gateway is talked to over micro_nabto.

Sources:
    The gateway's addresses, scales and ranges were found in material published online. Genvex's
    Modbus register workbook, posted at
    https://community.openenergymonitor.org/t/reverse-engineer-heatpump-genvex-combi-185/15992/46,
    has an 'Optima 301' sheet, whose register numbers are the gateway's datapoint and setpoint
    numbers wherever the two have been compared.
"""
from __future__ import annotations

from modbus_event_connect import Limits, PollRate, Unit
from modbus_event_connect.micro_nabto import MicroNabtoModel

from ._keys import PointKey
from ._optima import SLAVE_79250_FAN_LEVEL, SLAVE_79250_POINTS, optima_temperature
from ._points import section, setting, switch
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

OPTIMA_301 = MicroNabtoModel(
    "Optima 301", "Genvex", (
        section(reported=(
            *SLAVE_79250_POINTS,
            optima_temperature(PointKey.TEMP_BEFORE_CONDENSER, 4),
            optima_temperature(PointKey.TEMP_EVAPORATOR, 5),
            optima_temperature(PointKey.TEMP_HOTWATER_TOP, 6),
            optima_temperature(PointKey.TEMP_HOTWATER_BOTTOM, 7),
            optima_temperature(PointKey.TEMP_ROOM, 9),
            # reported: the workbook's 4x0001 "02) Cooling (°C)", 30-100 at a resolution of 0.1, shown 3-10
            setting(PointKey.COOLING_TEMPERATURE, 1, Limits(3, 10, step=0.1), scale=0.1, unit=Unit.CELSIUS),
            switch(PointKey.COOLING_ENABLE, 2),
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
"""Genvex's Optima 301, as its gateway is talked to over micro_nabto."""
