"""How certain it is that a point is what its model says: stated for every point, beside the point."""
from __future__ import annotations

from collections.abc import Callable, Sequence
from enum import StrEnum
from typing import Any

from modbus_event_connect import Identity, Point, Section


class Certainty(StrEnum):
    """How certain it is that a point's address, scale and meaning are right."""

    VERIFIED = "verified"
    """Read on a unit of the model."""
    REPORTED = "reported"
    """Found in material published online; not read on a unit of the model."""
    INFERRED = "inferred"
    """Placed from the model's Modbus manual by the order of its register group; not read on a unit
    of the model, and not found elsewhere."""


_CERTAINTIES: dict[Point[Any], Certainty] = {}


def section(*, when: Callable[[Identity], bool] | None = None, verified: Sequence[Point[Any]] = (),
            reported: Sequence[Point[Any]] = (), inferred: Sequence[Point[Any]] = ()) -> Section:
    """A section of a model, each point given under how certain it is; `when` as a `Section` has it.

    Raises:
        ValueError: a point is given under two certainties.
    """
    for level, points in ((Certainty.VERIFIED, verified), (Certainty.REPORTED, reported),
                          (Certainty.INFERRED, inferred)):
        for point in points:
            known = _CERTAINTIES.setdefault(point, level)
            if known is not level:
                raise ValueError(f"{point.key!r} is both {known} and {level}")
    return Section((*verified, *reported, *inferred), when=when)


def certainty(point: Point[Any]) -> Certainty:
    """How certain it is that `point`, as a client of one of this package's models has it, is right.

    Raises:
        KeyError: `point` is not one of this package's models' points.
    """
    return _CERTAINTIES[point]
