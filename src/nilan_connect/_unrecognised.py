"""A controller behind a Nilan gateway that no model matches, connected so that it can be mapped."""
from __future__ import annotations

from modbus_event_connect.micro_nabto import MicroNabtoModel

from ._shared import (
    ANSWER_WAIT,
    LATER_ANSWER_WAIT,
    MAX_REGISTERS,
    READ_BACK_AFTER,
    WRITE_RETRY,
    WRITE_TAKEN,
    ZEROS,
)

UNRECOGNISED = MicroNabtoModel(
    "Unrecognised unit", "Nilan", (),
    poll_intervals={},
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
"""A controller the gateway names by numbers no model knows. It has no points, so nothing is read
or written but what a mapping asks for; every gateway numbers its datapoints and setpoints alike,
so a mapping reads it as any other."""
