"""Genvex's Optima 301 as a model: its points, and how its gateway is talked to over micro_nabto.

Sources:
    The gateway's addresses, scales and ranges were found in material published online. Genvex's
    Modbus register workbook, posted at
    https://community.openenergymonitor.org/t/reverse-engineer-heatpump-genvex-combi-185/15992/46,
    has an 'Optima 301' sheet; the gateway's datapoint and setpoint numbers are taken to be its
    register numbers.
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
            # reported: the workbook's 3x0004 T5; its defrost programs name "Before cooling surface"
            # and "Cooling surface", which T6 is
            optima_temperature(PointKey.TEMP_BEFORE_EVAPORATOR, 4),
            optima_temperature(PointKey.TEMP_EVAPORATOR, 5),
            optima_temperature(PointKey.TEMP_HOTWATER_TOP, 6),
            optima_temperature(PointKey.TEMP_HOTWATER_BOTTOM, 7),
            optima_temperature(PointKey.TEMP_ROOM_PANEL, 9),  # reported: the workbook's 3x0009 "T2 Panel"
            # reported: the workbook's 4x0001 "02) Cooling (°C)", 30-100 at a resolution of 0.1, shown 3-10
            setting(PointKey.COOLING_TEMPERATURE, 1, Limits(3, 10, step=0.1), scale=0.1, unit=Unit.CELSIUS),
            switch(PointKey.COOLING_ENABLE, 2),
            SLAVE_79250_FAN_LEVEL,
        )),
        section(candidates=(
            # Not read on a 301 yet. Genvex's register workbook, sheet 'Optima 301'
            # (https://community.openenergymonitor.org/t/reverse-engineer-heatpump-genvex-combi-185/15992/46):
            # A85, 4x0016 "20) Preheat (on/off)", 0-1
            switch(PointKey.PREHEAT_ENABLE, 16),
            # A89, 4x0020 "24) Min air volume (%)", 0-100; the Optima 312's user manual, item 24
            # "Minimum extract air": "The heat pump will not start with extract air flow below this setting."
            setting(PointKey.MIN_AIR_VOLUME, 20, Limits(0, 100, step=1), unit=Unit.PERCENT),
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
