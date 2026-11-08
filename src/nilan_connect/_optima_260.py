"""Genvex's Optima 260 as a model, and how it is talked to over micro_nabto.

Sources:
    No Modbus description of an Optima is published. The gateway's addresses, scales and
    ranges were found in material published online. The user manuals in this repository's
    docs/models/genvex-optima name the sensors and the settings' ranges.
"""
from __future__ import annotations

from modbus_event_connect import DataType, Limits, Model, Unit
from modbus_event_connect.micro_nabto import MicroNabtoProfile

from ._keys import PointKey
from ._optima import optima_fan_presets, optima_percent, optima_target, optima_temperature
from ._points import (
    GATEWAY_TIMING,
    GATEWAY_ZEROS,
    command,
    fan_level_rereads,
    reading,
    section,
    setting,
    state,
)

OPTIMA_260 = Model("Optima 260", "Genvex", (
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
), timing=GATEWAY_TIMING)

OPTIMA_260_MICRO_NABTO = MicroNabtoProfile(
    model=OPTIMA_260,
    max_registers=64,           # a CTS 402 answered 108, so this leaves room
    later_answer_wait=5.0,      # not measured on this controller, so longer than a CTS400's
    zeros=GATEWAY_ZEROS,
)
