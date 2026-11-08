"""Genvex's Optima 251 as a model, and how it is talked to over micro_nabto.

Sources:
    No Modbus description of an Optima is published. The gateway's addresses, scales and
    ranges were found in material published online. The user manuals in this repository's
    docs/models/genvex-optima name the sensors and the settings' ranges.
"""
from __future__ import annotations

from modbus_event_connect import Model
from modbus_event_connect.micro_nabto import MicroNabtoProfile

from ._optima_250 import OPTIMA_250_SECTIONS
from ._points import GATEWAY_TIMING, GATEWAY_ZEROS

OPTIMA_251 = Model("Optima 251", "Genvex", OPTIMA_250_SECTIONS, timing=GATEWAY_TIMING)

OPTIMA_251_MICRO_NABTO = MicroNabtoProfile(
    model=OPTIMA_251,
    max_registers=64,           # a CTS 402 answered 108, so this leaves room
    later_answer_wait=5.0,      # not measured on this controller, so longer than a CTS400's
    zeros=GATEWAY_ZEROS,
)
