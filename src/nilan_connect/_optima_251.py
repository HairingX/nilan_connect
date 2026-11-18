"""Genvex's Optima 251 as a model: its points, and how its gateway is talked to over micro_nabto.

Sources:
    No Modbus description of an Optima is published. The gateway's addresses, scales and
    ranges were found in material published online. The user manuals in this repository's
    docs/models/genvex-optima name the sensors and the settings' ranges.
"""
from __future__ import annotations

from modbus_event_connect import PollRate
from modbus_event_connect.micro_nabto import MicroNabtoModel

from ._optima_250 import OPTIMA_250_SECTIONS
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

OPTIMA_251 = MicroNabtoModel(
    "Optima 251", "Genvex", OPTIMA_250_SECTIONS,
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
"""Genvex's Optima 251, as its gateway is talked to over micro_nabto."""
