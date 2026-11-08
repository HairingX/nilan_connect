"""Genvex's Optima 312 as a model, and how it is talked to over micro_nabto.

Sources:
    No Modbus description of an Optima is published. The gateway's addresses, scales and
    ranges were found in material published online. The user manuals in this repository's
    docs/models/genvex-optima name the sensors and the settings' ranges.
"""
from __future__ import annotations

from modbus_event_connect import DataType, Limits, Model, Unit
from modbus_event_connect.micro_nabto import MicroNabtoProfile

from ._keys import PointKey
from ._optima import SLAVE_79250_FAN_LEVEL, SLAVE_79250_POINTS, optima_temperature
from ._points import GATEWAY_TIMING, GATEWAY_ZEROS, section, setting, state, switch

OPTIMA_312 = Model("Optima 312", "Genvex", (
    section(reported=(
        *SLAVE_79250_POINTS,
        optima_temperature(PointKey.TEMP_BEFORE_CONDENSER, 4),
        optima_temperature(PointKey.TEMP_EVAPORATOR, 5),
        optima_temperature(PointKey.TEMP_HOTWATER_TOP, 6),
        optima_temperature(PointKey.TEMP_HOTWATER_BOTTOM, 7),
        optima_temperature(PointKey.TEMP_ROOM, 9),
        state(PointKey.HEAT_PUMP_ACTIVE, 11),
        state(PointKey.HEAT_PUMP_HEATER_ACTIVE, 12),
        state(PointKey.REHEAT_ACTIVE, 13),
        state(PointKey.DEFROST_ACTIVE, 14),
        state(PointKey.HEAT_PUMP_WATER_HEATING, 15),
        state(PointKey.HEAT_PUMP_ROOM_HEATING, 16),
        setting(PointKey.TEMP_HOTWATER, 1, Limits(0, 55, step=0.1), data_type=DataType.INT16, scale=0.1,
                unit=Unit.CELSIUS),
        switch(PointKey.HOTWATER_HEATER_ENABLE, 2),
        switch(PointKey.REHEAT_ENABLE, 21),
        SLAVE_79250_FAN_LEVEL,
    )),
), timing=GATEWAY_TIMING)

OPTIMA_312_MICRO_NABTO = MicroNabtoProfile(
    model=OPTIMA_312,
    max_registers=64,           # a CTS 402 answered 108, so this leaves room
    later_answer_wait=5.0,      # not measured on this controller, so longer than a CTS400's
    zeros=GATEWAY_ZEROS,
)
