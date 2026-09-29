"""Write controllers.md, every point of every controller, from the models: `python docs/controllers.py`."""
from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from modbus_event_connect import Model, Point, Section
from modbus_event_connect.micro_nabto import SetpointRegister

import nilan_connect as nilan
import nilan_connect._cts602 as cts602

OUTPUT = Path(__file__).with_name("controllers.md")

MODELS: tuple[Model, ...] = (nilan.CTS400, nilan.CTS602, nilan.CTS602_LIGHT, nilan.OPTIMA_250, nilan.OPTIMA_251,
                             nilan.OPTIMA_260, nilan.OPTIMA_270, nilan.OPTIMA_301, nilan.OPTIMA_312, nilan.OPTIMA_314)



def _named_variants() -> list[int]:
    named: set[int] = set()
    for name, value in vars(cts602).items():
        if name.startswith(("WITH_", "WITHOUT_")) and isinstance(value, frozenset):
            named |= cast(frozenset[int], value)
    return sorted(named)


CTS602_VARIANTS = _named_variants()
"""Every CTS602 device variant a section names."""

UNNAMED_VARIANT = 0
"""A variant no section names, standing for all of them."""


def _register(point: Point[Any], *, written: bool) -> str:
    access = point.write if written else point.read
    if access is None:
        return ""
    space = "setpoint" if isinstance(access, SetpointRegister) else "datapoint"
    bit = point.data_type.bit_index
    return f"{space} {access.address}" + ("" if bit is None else f" bit {bit}")


def _variants(section: Section) -> str:
    if section.when is None:
        return "all"
    included = [n for n in CTS602_VARIANTS if section.when({"slave_device_model": n})]
    if section.when({"slave_device_model": UNNAMED_VARIANT}):
        excluded = [n for n in CTS602_VARIANTS if n not in included]
        return "all but " + ", ".join(map(str, excluded))
    return ", ".join(map(str, included))


def _model(model: Model) -> list[str]:
    variants = model is nilan.CTS602
    lines = [f"## {model.manufacturer} {model.name}", ""]
    header = ["Key", "Read", "Written", "Unit", "Certainty"] + (["Variants"] if variants else [])
    lines += ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    rows: list[tuple[str, ...]] = []
    for section in model.sections:
        assert isinstance(section, Section)
        for point in section.points:
            row = (f"`{point.key}`", _register(point, written=False), _register(point, written=True),
                   "" if point.unit is None else point.unit.value, nilan.certainty(point).value)
            rows.append(row + ((_variants(section),) if variants else ()))
    lines += ["| " + " | ".join(row) + " |" for row in sorted(rows, key=lambda row: (row[0].strip("`"), row[1]))]
    return lines + [""]


def render() -> str:
    """controllers.md as the models stand."""
    lines = [
        "# Controllers",
        "",
        "Every point of every controller, generated from the models by `python docs/controllers.py`.",
        "A CTS602's variant is the slave device model its gateway's handshake names; what each",
        "certainty means is in the README.",
        "",
    ]
    for model in MODELS:
        lines += _model(model)
    return "\n".join(lines)


if __name__ == "__main__":
    OUTPUT.write_text(render(), encoding="utf-8", newline="\n")
