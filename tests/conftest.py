"""Shared test setup: live tests stay invisible unless configured - `live_or_skip` skips them,
and the `live` marker excludes them via `pytest -m "not live"`."""
import os

import pytest


def live_setting(name: str) -> str | None:
    """A live test's setting: environment first, then mysecrets.py (gitignored)."""
    value = os.environ.get(name)
    if value:
        return value
    try:
        import mysecrets  # type: ignore
    except Exception:
        return None
    found = getattr(mysecrets, name, None)
    return str(found) if found else None


def live_or_skip(what: str, **settings: str | None) -> list[pytest.MarkDecorator]:
    """Marks for a module of live tests: the `live` marker, plus a skip naming what is missing."""
    missing = [name for name, value in settings.items() if not value]
    return [
        pytest.mark.live,
        pytest.mark.skipif(
            bool(missing),
            reason=f"No {what} device configured. Set {', '.join(missing)} as environment "
                   f"variables or in a gitignored mysecrets file.",
        ),
    ]
