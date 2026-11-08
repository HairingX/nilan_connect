"""Genvex's Optima 301 as a model, and how it is talked to over micro_nabto.

Sources:
    No Modbus description of an Optima is published. The gateway's addresses, scales and
    ranges were found in material published online. The user manuals in this repository's
    docs/models/genvex-optima name the sensors and the settings' ranges.
"""
from __future__ import annotations

from modbus_event_connect import Limits, Model
from modbus_event_connect.micro_nabto import MicroNabtoProfile

from ._keys import PointKey
from ._optima import SLAVE_79250_FAN_LEVEL, SLAVE_79250_POINTS, optima_temperature
from ._points import GATEWAY_TIMING, GATEWAY_ZEROS, section, setting, switch

OPTIMA_301 = Model("Optima 301", "Genvex", (
    section(reported=(
        *SLAVE_79250_POINTS,
        optima_temperature(PointKey.TEMP_BEFORE_CONDENSER, 4),
        optima_temperature(PointKey.TEMP_EVAPORATOR, 5),
        optima_temperature(PointKey.TEMP_HOTWATER_TOP, 6),
        optima_temperature(PointKey.TEMP_HOTWATER_BOTTOM, 7),
        optima_temperature(PointKey.TEMP_ROOM, 9),
        setting(PointKey.COOLING_TEMPERATURE, 1, Limits(30, 100, step=1)),
        switch(PointKey.COOLING_ENABLE, 2),
        switch(PointKey.PREHEAT_ENABLE, 20),
        SLAVE_79250_FAN_LEVEL,
    )),
), timing=GATEWAY_TIMING)

OPTIMA_301_MICRO_NABTO = MicroNabtoProfile(
    model=OPTIMA_301,
    max_registers=64,           # a CTS 402 answered 108, so this leaves room
    later_answer_wait=5.0,      # not measured on this controller, so longer than a CTS400's
    zeros=GATEWAY_ZEROS,
)
