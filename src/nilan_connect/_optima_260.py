"""Genvex's Optima 260 as a model: its points, and how its gateway is talked to over micro_nabto.

Sources:
    The gateway's addresses, scales and ranges were found in material published online. Genvex's
    Modbus register workbook, posted at
    https://community.openenergymonitor.org/t/reverse-engineer-heatpump-genvex-combi-185/15992/46,
    has an 'Optima 260' sheet that names the gateway's datapoint and setpoint of each register.
"""
from __future__ import annotations

from modbus_event_connect import DataType, Limits, PollRate, Refresh, Unit
from modbus_event_connect.micro_nabto import MicroNabtoModel

from ._keys import PointKey
from ._optima import optima_fan_presets, optima_percent, optima_target, optima_temperature
from ._points import (
    command,
    reading,
    section,
    setting,
    state,
)
from ._shared import (
    ANSWER_WAIT,
    FAN_LEVEL_REREAD_AFTER,
    FAST_INTERVAL,
    LATER_ANSWER_WAIT,
    MAX_REGISTERS,
    READ_BACK_AFTER,
    SLOW_INTERVAL,
    WRITE_RETRY,
    WRITE_TAKEN,
    ZEROS,
)

OPTIMA_260 = MicroNabtoModel(
    "Optima 260", "Genvex", (
        section(reported=(
            optima_temperature(PointKey.TEMP_SUPPLY, 0),
            optima_temperature(PointKey.TEMP_OUTSIDE, 2),
            optima_temperature(PointKey.TEMP_EXHAUST, 3),
            optima_temperature(PointKey.TEMP_EXTRACT, 6),
            optima_percent(PointKey.FAN_DUTYCYCLE_SUPPLY, 9),
            optima_percent(PointKey.FAN_DUTYCYCLE_EXTRACT, 10),
            state(PointKey.BYPASS_ACTIVE, 11),
            # reported: the workbook's 3x0011 "Bypass ventil", 0-100, which it gives as datapoint 11
            reading(PointKey.BYPASS_POSITION, 11, unit=Unit.PERCENT),
            reading(PointKey.HUMIDITY, 13, data_type=DataType.INT16, unit=Unit.PERCENT),
            setting(PointKey.FAN_LEVEL, 0, Limits(0, 4, step=1), on_write=Refresh(
                [PointKey.FAN_DUTYCYCLE_SUPPLY, PointKey.FAN_DUTYCYCLE_EXTRACT], after=FAN_LEVEL_REREAD_AFTER)),
            optima_target(2),
            *optima_fan_presets(7),
            setting(PointKey.TEMP_BYPASS_OPEN_OFFSET, 18, Limits(1, 10, step=0.1), data_type=DataType.INT16, scale=0.1,
                    unit=Unit.CELSIUS),
            command(PointKey.FILTER_REPLACE_RESET, 47),
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
"""Genvex's Optima 260, as its gateway is talked to over micro_nabto."""
