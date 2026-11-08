"""Genvex's Optima 250 as a model, and how it is talked to over micro_nabto.

Sources:
    No Modbus description of an Optima is published. The gateway's addresses, scales and
    ranges were found in material published online. The user manuals in this repository's
    docs/models/genvex-optima name the sensors and the settings' ranges.
"""
from __future__ import annotations

from modbus_event_connect import DataType, Limits, Model, Unit
from modbus_event_connect.micro_nabto import MicroNabtoProfile

from ._keys import PointKey
from ._optima import SLAVE_79250_POINTS, optima_rpm, optima_temperature
from ._points import GATEWAY_TIMING, GATEWAY_ZEROS, fan_level_rereads, section, setting, switch

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
        setting(PointKey.FAN_LEVEL, 100, Limits(0, 4, step=1), on_write=fan_level_rereads(
            PointKey.FAN_DUTYCYCLE_SUPPLY, PointKey.FAN_DUTYCYCLE_EXTRACT, PointKey.FAN_RPM_SUPPLY,
            PointKey.FAN_RPM_EXTRACT)),
    )),
)
"""The Optima 250's, and the Optima 251's, which material published online gives the same."""

OPTIMA_250 = Model("Optima 250", "Genvex", OPTIMA_250_SECTIONS, timing=GATEWAY_TIMING)

OPTIMA_250_MICRO_NABTO = MicroNabtoProfile(
    model=OPTIMA_250,
    max_registers=64,           # a CTS 402 answered 108, so this leaves room
    later_answer_wait=5.0,      # not measured on this controller, so longer than a CTS400's
    zeros=GATEWAY_ZEROS,
)
