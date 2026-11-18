"""Values several models state alike, each named once so that a model can refer to it.

Sharing a value says nothing about the units being alike: a model may state its own at any time.
"""
from __future__ import annotations

from modbus_event_connect import Fixed, Retry, Steps, Within
from modbus_event_connect.micro_nabto import RereadZeros

FAST_INTERVAL = 10.0  # guess
"""Seconds between two reads of a controller's readings."""

# Settings change only when written, so they are read far less often than readings.
SLOW_INTERVAL = 180.0  # guess
"""Seconds between two reads of a controller's settings."""

READ_BACK_AFTER = 1.0  # guess
"""Seconds after a write until the setting written is read back."""

FAN_LEVEL_REREAD_AFTER = 3.0  # measured on a CTS400: level and both speeds 1.3 to 1.8 s after (HairingX/nilan_connect#4)
"""Seconds after a fan level is written until what follows it is read again."""

MAX_REGISTERS = 64  # reported: a CTS 402 answered 108 in one read (modbus_event_connect's live tests); this leaves room
"""Most registers a gateway is asked for in one read."""

ANSWER_WAIT = 2.0  # measured on a CTS602: 21,000 reads answered within 245 ms (HairingX/modbus_event_connect#35, HairingX/nilan_connect#28)
"""Seconds an answer is waited for once the gateway has said it has the request; one it leaves
unanswered holds up the reads behind it for as long as this."""

LATER_ANSWER_WAIT = 5.0  # guess: not measured, so longer than the CTS400's
"""Seconds a read sent again, and answered with only zeros where values were, is kept open for a
later answer."""

ZEROS = RereadZeros(
    within=7.5,  # measured on a CTS602: a new session's first reads zeros, values 10 s later (HairingX/modbus_event_connect#19)
    wait=Steps(0.5, then=Fixed(1.0)),  # guess
    at_once=True,  # guess
    halves=True,  # guess
)
"""How a gateway's answer of only zeros, where values were, is read again: the zeros are taken
short of the 10 s between two reads."""

WRITE_RETRY = Retry(
    Fixed(0.5),  # measured on a CTS400: eight writes, each first try answered 0x63, the second taken (HairingX/nilan_connect#5, HairingX/modbus_event_connect#10)
    Within(15.0),  # guess
)
"""When a write the controller did not take is sent again: every half second, for up to 15 s after
it was first sent."""

WRITE_TAKEN = frozenset({0})  # guess
"""The statuses a gateway answers a write it took with."""
