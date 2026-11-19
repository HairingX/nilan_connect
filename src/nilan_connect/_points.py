"""The kinds of point a controller behind a Nilan gateway has.

Over micro_nabto a controller's input registers are datapoints and its holding registers
setpoints. Each builder's `replaces` names the point a candidate built by it takes the place of
at the Test level; such a point is given under `section(candidates=...)`.
"""
from __future__ import annotations

from collections.abc import Callable, Collection, Mapping, Sequence
from dataclasses import replace
from enum import IntEnum
from typing import Any

from event_connect import Certainty
from modbus_event_connect import (
    Candidate,
    DataType,
    Identity,
    Key,
    Limits,
    ModelError,
    Point,
    PollRate,
    Refresh,
    Section,
    Transform,
    Transforms,
    Unit,
    WriteKind,
)
from modbus_event_connect.micro_nabto import DatapointRegister, SetpointRegister


def section(*, when: Callable[[Identity], bool] | None = None, verified: Sequence[Point[Any]] = (),
            reported: Sequence[Point[Any]] = (), inferred: Sequence[Point[Any]] = (),
            candidates: Sequence[Point[Any]] = ()) -> Section:
    """A section of a model, each point given under how certain it is; `when` as a `Section` has it.

    A point under `candidates` is used only at the Test level, in place of the point it was built
    to replace, if any; it keeps the certainty it was built with.

    Raises:
        ModelError: a point under `verified`, `reported` or `inferred` was built as a candidate.
    """
    built_as_candidates = [point.key for point in (*verified, *reported, *inferred) if point.candidate is not None]
    if built_as_candidates:
        raise ModelError(f"built as candidates, but not given under candidates: {', '.join(built_as_candidates)}")
    return Section((*(replace(point, certainty=Certainty.VERIFIED) for point in verified),
                    *(replace(point, certainty=Certainty.REPORTED) for point in reported),
                    *(replace(point, certainty=Certainty.INFERRED) for point in inferred),
                    *(replace(point, candidate=point.candidate or Candidate()) for point in candidates)), when=when)


def _candidate(replaces: Key[Any] | None) -> Candidate | None:
    """What a point built to replace the point of `replaces` is; None for one built to replace none."""
    return None if replaces is None else Candidate(replaces=replaces)


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
               codes: Mapping[int, IntEnum] | None = None, replaces: Key[Any] | None = None) -> Point[T]:
    """A datapoint that is only read."""
    return Point(key, read=DatapointRegister(address), data_type=data_type, scale=scale, offset=offset,
                 unit=unit, transform=transform, codes=codes, poll_rate=PollRate.FAST, candidate=_candidate(replaces))


def temperature(key: Key[float], address: int, *, scale: float, offset: float = 0,
                replaces: Key[Any] | None = None) -> Point[float]:
    """A datapoint holding a signed temperature in °C."""
    return reading(key, address, data_type=DataType.INT16, scale=scale, offset=offset, unit=Unit.CELSIUS,
                   replaces=replaces)


def state(key: Key[bool], address: int, *, inverted: bool = False, replaces: Key[Any] | None = None) -> Point[bool]:
    """A datapoint that is 1 while `key` is true, or, `inverted`, while it is false."""
    return reading(key, address, data_type=DataType.BOOL, transform=Transforms.INVERT_BOOL if inverted else None,
                   replaces=replaces)


def alarm_bit(key: Key[bool], address: int, bit: int, *, inverted: bool = False,
              replaces: Key[Any] | None = None) -> Point[bool]:
    """One bit of a datapoint: set while `key` is true, or, `inverted`, while it is false."""
    return Point(key, read=DatapointRegister(address), data_type=DataType.bit(bit),
                 transform=Transforms.INVERT_BOOL if inverted else None, poll_rate=PollRate.FAST,
                 candidate=_candidate(replaces))


def setpoint_reading[T](key: Key[T], address: int, *, data_type: DataType = DataType.UINT16,
                        unit: Unit | None = None, codes: Mapping[int, IntEnum] | None = None,
                        replaces: Key[Any] | None = None) -> Point[T]:
    """A setpoint that is only read."""
    return Point(key, read=SetpointRegister(address), data_type=data_type, unit=unit, codes=codes,
                 poll_rate=PollRate.SLOW, candidate=_candidate(replaces))


def setting[T](key: Key[T], address: int, limits: Limits | None, *, write_address: int | None = None,
               data_type: DataType = DataType.UINT16, scale: float = 1, offset: float = 0,
               unit: Unit | None = None, on_write: Refresh | None = None,
               replaces: Key[Any] | None = None) -> Point[T]:
    """A setpoint holding a number, written at `address` unless `write_address` says otherwise.

    `limits` is None where no source gives the range the controller takes.
    """
    return Point(key, read=SetpointRegister(address),
                 write=SetpointRegister(address if write_address is None else write_address),
                 data_type=data_type, scale=scale, offset=offset, unit=unit, limits=limits,
                 poll_rate=PollRate.SLOW, on_write=on_write, candidate=_candidate(replaces))


def setpoint_bit(key: Key[bool], address: int, bit: int, *, replaces: Key[Any] | None = None) -> Point[bool]:
    """One bit of a setpoint that is only read: set while `key` is true."""
    return Point(key, read=SetpointRegister(address), data_type=DataType.bit(bit), poll_rate=PollRate.SLOW,
                 candidate=_candidate(replaces))


def choice[T: IntEnum](key: Key[T], address: int, *, write_address: int | None = None,
                       codes: Mapping[int, IntEnum] | None = None, replaces: Key[Any] | None = None) -> Point[T]:
    """A setpoint holding one of the states `key` names, written at `address` unless
    `write_address` says otherwise."""
    return Point(key, read=SetpointRegister(address),
                 write=SetpointRegister(address if write_address is None else write_address),
                 codes=codes, poll_rate=PollRate.SLOW, candidate=_candidate(replaces))


def switch(key: Key[bool], address: int, *, write_address: int | None = None,
           replaces: Key[Any] | None = None) -> Point[bool]:
    """A setpoint that is 1 while `key` is on, written at `address` unless `write_address` says
    otherwise."""
    return Point(key, read=SetpointRegister(address),
                 write=SetpointRegister(address if write_address is None else write_address),
                 data_type=DataType.BOOL, poll_rate=PollRate.SLOW, candidate=_candidate(replaces))


def command(key: Key[bool], address: int, *, on_write: Refresh | None = None,
            replaces: Key[Any] | None = None) -> Point[bool]:
    """A setpoint written to make the controller act; nothing to show once it has."""
    return Point(key, write=SetpointRegister(address), data_type=DataType.BOOL, write_kind=WriteKind.COMMAND,
                 on_write=on_write, candidate=_candidate(replaces))
