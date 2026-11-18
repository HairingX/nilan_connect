"""Genvex's Optima 250 as a model: its points, and how its gateway is talked to over micro_nabto.

Sources:
    No Modbus description of an Optima is published. The gateway's addresses, scales and
    ranges were found in material published online. The user manuals in this repository's
    docs/models/genvex-optima name the sensors and the settings' ranges.
"""
from __future__ import annotations

from modbus_event_connect import DataType, Limits, PollRate, Refresh, Unit
from modbus_event_connect.micro_nabto import MicroNabtoModel

from ._keys import PointKey
from ._optima import SLAVE_79250_POINTS, optima_rpm, optima_temperature
from ._points import section, setting, switch
from ._shared import (
    ANSWER_WAIT,
    FAN_LEVEL_REREAD_AFTER,
    FAST_INTERVAL,
    LATER_ANSWER_WAIT,
    MAX_REGISTERS,
    READ_BACK_AFTER,
    SLOW_INTERVAL,
    WRITE_RETRY,
    ZEROS,
)

OPTIMA_250_SECTIONS = (
    section(reported=(
        *SLAVE_79250_POINTS,
        optima_temperature(PointKey.TEMP_EXTRACT, 6),
        optima_rpm(PointKey.FAN_RPM_SUPPLY, 108),
        optima_rpm(PointKey.FAN_RPM_EXTRACT, 109),
        switch(PointKey.REHEAT_ENABLE, 2),
        setting(PointKey.FILTER_REPLACE_INTERVAL, 4, Limits(0, 6, step=1), unit=Unit.MONTHS),
        switch(PointKey.HUMIDITY_CONTROL_ENABLE, 5),
        setting(PointKey.TEMP_BYPASS_OPEN_OFFSET, 17, Limits(1, 10, step=0.1), data_type=DataType.INT16, scale=0.1,
                unit=Unit.CELSIUS),
        setting(PointKey.FAN_LEVEL, 100, Limits(0, 4, step=1), on_write=Refresh(
            [PointKey.FAN_DUTYCYCLE_SUPPLY, PointKey.FAN_DUTYCYCLE_EXTRACT, PointKey.FAN_RPM_SUPPLY,
             PointKey.FAN_RPM_EXTRACT], after=FAN_LEVEL_REREAD_AFTER)),
    )),
)
"""The Optima 250's, and the Optima 251's, which material published online gives the same."""

OPTIMA_250 = MicroNabtoModel(
    "Optima 250", "Genvex", OPTIMA_250_SECTIONS,
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
"""Genvex's Optima 250, as its gateway is talked to over micro_nabto."""
