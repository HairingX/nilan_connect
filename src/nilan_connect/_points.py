"""The kinds of point a controller behind a Nilan gateway has, and what its models share.

Over micro_nabto a controller's input registers are datapoints and its holding registers
setpoints.
"""
from __future__ import annotations

from collections.abc import Callable, Collection, Mapping, Sequence
from dataclasses import replace
from enum import IntEnum
from typing import Any

from event_connect import Certainty
from modbus_event_connect import (
    DataType,
    Fixed,
    Identity,
    Key,
    Limits,
    Point,
    PollRate,
    Refresh,
    Section,
    Steps,
    Timing,
    Transform,
    Transforms,
    Unit,
    WriteKind,
)
from modbus_event_connect.micro_nabto import DatapointRegister, RereadZeros, SetpointRegister

GATEWAY_TIMING = Timing(
    # Settings change only when written, so they are read far less often than readings.
    poll_intervals={PollRate.FAST: 10.0, PollRate.SLOW: 180.0},
    min_poll_interval=0.0,
    read_back_after=1.0,
    # One missed read, of those that come every 10 s, keeps the last values; a gateway that stays
    # silent is shown as not answering.
    offline_after=10.0,
)
"""When a controller behind a Nilan gateway is read, and how long a write takes to show."""

GATEWAY_ZEROS = RereadZeros(within=7.5, wait=Steps(0.5, then=Fixed(1.0)), at_once=True, halves=True)
"""How a Nilan gateway's answer of only zeros, where values were, is read again: the zeros are
taken after 7.5 s, short of the 10 s between two reads, as a gateway was seen answering a new
session's first reads with zeros, and values 10 s later."""


def section(*, when: Callable[[Identity], bool] | None = None, verified: Sequence[Point[Any]] = (),
            reported: Sequence[Point[Any]] = (), inferred: Sequence[Point[Any]] = ()) -> Section:
    """A section of a model, each point given under how certain it is; `when` as a `Section` has it."""
    return Section((*(replace(point, certainty=Certainty.VERIFIED) for point in verified),
                    *(replace(point, certainty=Certainty.REPORTED) for point in reported),
                    *(replace(point, certainty=Certainty.INFERRED) for point in inferred)), when=when)


def slave_model_in(models: Collection[int]) -> Callable[[Identity], bool]:
    """Whether the handshake names one of `models` as its slave device model."""
    chosen = frozenset(models)
    return lambda identity: identity.get("slave_device_model") in chosen


def slave_model_not_in(models: Collection[int]) -> Callable[[Identity], bool]:
    """Whether the handshake names none of `models` as its slave device model."""
    excluded = frozenset(models)
    return lambda identity: identity.get("slave_device_model") not in excluded


def reading[T](key: Key[T], address: int, *, data_type: DataType = DataType.UINT16, scale: float = 1,
               offset: float = 0, unit: Unit | None = None, transform: Transform | None = None,
               codes: Mapping[int, IntEnum] | None = None) -> Point[T]:
    """A datapoint that is only read."""
    return Point(key, read=DatapointRegister(address), data_type=data_type, scale=scale, offset=offset,
                 unit=unit, transform=transform, codes=codes, poll_rate=PollRate.FAST)


def temperature(key: Key[float], address: int, *, scale: float, offset: float = 0) -> Point[float]:
    """A datapoint holding a signed temperature in °C."""
    return reading(key, address, data_type=DataType.INT16, scale=scale, offset=offset, unit=Unit.CELSIUS)


def state(key: Key[bool], address: int, *, inverted: bool = False) -> Point[bool]:
    """A datapoint that is 1 while `key` is true, or, `inverted`, while it is false."""
    return reading(key, address, data_type=DataType.BOOL, transform=Transforms.INVERT_BOOL if inverted else None)


def alarm_bit(key: Key[bool], address: int, bit: int, *, inverted: bool = False) -> Point[bool]:
    """One bit of a datapoint: set while `key` is true, or, `inverted`, while it is false."""
    return Point(key, read=DatapointRegister(address), data_type=DataType.bit(bit),
                 transform=Transforms.INVERT_BOOL if inverted else None, poll_rate=PollRate.FAST)


def setpoint_reading[T](key: Key[T], address: int, *, data_type: DataType = DataType.UINT16,
                        codes: Mapping[int, IntEnum] | None = None) -> Point[T]:
    """A setpoint that is only read."""
    return Point(key, read=SetpointRegister(address), data_type=data_type, codes=codes, poll_rate=PollRate.SLOW)


def setting[T](key: Key[T], address: int, limits: Limits | None, *, write_address: int | None = None,
               data_type: DataType = DataType.UINT16, scale: float = 1, offset: float = 0,
               unit: Unit | None = None, on_write: Refresh | None = None) -> Point[T]:
    """A setpoint holding a number, written at `address` unless `write_address` says otherwise.

    `limits` is None where no source gives the range the controller takes.
    """
    return Point(key, read=SetpointRegister(address),
                 write=SetpointRegister(address if write_address is None else write_address),
                 data_type=data_type, scale=scale, offset=offset, unit=unit, limits=limits,
                 poll_rate=PollRate.SLOW, on_write=on_write)


def choice[T: IntEnum](key: Key[T], address: int, *, write_address: int | None = None,
                       codes: Mapping[int, IntEnum] | None = None) -> Point[T]:
    """A setpoint holding one of the states `key` names, written at `address` unless
    `write_address` says otherwise."""
    return Point(key, read=SetpointRegister(address),
                 write=SetpointRegister(address if write_address is None else write_address),
                 codes=codes, poll_rate=PollRate.SLOW)


def switch(key: Key[bool], address: int, *, write_address: int | None = None) -> Point[bool]:
    """A setpoint that is 1 while `key` is on, written at `address` unless `write_address` says
    otherwise."""
    return Point(key, read=SetpointRegister(address),
                 write=SetpointRegister(address if write_address is None else write_address),
                 data_type=DataType.BOOL, poll_rate=PollRate.SLOW)


def command(key: Key[bool], address: int, *, on_write: Refresh | None = None) -> Point[bool]:
    """A setpoint written to make the controller act; nothing to show once it has."""
    return Point(key, write=SetpointRegister(address), data_type=DataType.BOOL, write_kind=WriteKind.COMMAND,
                 on_write=on_write)


def fan_level_rereads(*keys: Key[Any]) -> Refresh:
    """`keys`, which follow the chosen fan level, read again once the controller has taken it."""
    return Refresh(list(keys), after=3.0)
