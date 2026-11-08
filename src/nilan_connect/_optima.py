"""What Genvex's Optima controllers share: how their points are built, and the points several have.

Sources:
    No Modbus description of an Optima is published. The gateway's addresses, scales and
    ranges were found in material published online. The user manuals in this repository's
    docs/models/genvex-optima name the sensors and the settings' ranges.
"""
from __future__ import annotations

from typing import Any

from modbus_event_connect import DataType, Key, Limits, Point, Refresh, Unit

from ._keys import PointKey
from ._points import alarm_bit, command, fan_level_rereads, reading, setting, state, switch, temperature


def optima_temperature(key: Key[float], address: int) -> Point[float]:
    """A datapoint holding a temperature in tenths of a °C above -30 °C."""
    return temperature(key, address, scale=0.1, offset=-30)


def optima_percent(key: Key[float], address: int, *, scale: float = 1) -> Point[float]:
    """A datapoint holding a percentage."""
    return reading(key, address, data_type=DataType.INT16, scale=scale, unit=Unit.PERCENT)


def optima_rpm(key: Key[int], address: int) -> Point[int]:
    """A datapoint holding a speed in revolutions per minute."""
    return reading(key, address, data_type=DataType.INT16, unit=Unit.RPM)


def optima_target(address: int, *, write_address: int | None = None) -> Point[float]:
    """The setpoint holding the target temperature, in tenths of a °C above 10 °C."""
    return setting(PointKey.TEMP_TARGET, address, Limits(10, 30, step=0.5), write_address=write_address,
                   data_type=DataType.INT16, scale=0.1, offset=10, unit=Unit.CELSIUS)


def optima_fan_presets(address: int) -> tuple[Point[float], ...]:
    """The fans' speeds at levels 1 to 3, supply fan first, in the six setpoints from `address`."""
    keys = (PointKey.FAN_LEVEL1_SUPPLY_PRESET, PointKey.FAN_LEVEL2_SUPPLY_PRESET, PointKey.FAN_LEVEL3_SUPPLY_PRESET,
            PointKey.FAN_LEVEL1_EXTRACT_PRESET, PointKey.FAN_LEVEL2_EXTRACT_PRESET, PointKey.FAN_LEVEL3_EXTRACT_PRESET)
    return tuple(setting(key, address + n, Limits(0, 100, step=1), unit=Unit.PERCENT) for n, key in enumerate(keys))


def optima_write_address(address: int) -> int:
    """Where an Optima 270 or 314 takes the write to the setpoint it reports at `address`."""
    return 2 * address + 10


def optima_270_setting[T](key: Key[T], address: int, limits: Limits | None, *,
                          data_type: DataType = DataType.UINT16, scale: float = 1,
                          unit: Unit | None = None, on_write: Refresh | None = None) -> Point[T]:
    """A setpoint of an Optima 270 or 314, written at `optima_write_address`."""
    return setting(key, address, limits, write_address=optima_write_address(address), data_type=data_type,
                   scale=scale, unit=unit, on_write=on_write)


def optima_270_fan_level() -> Point[int]:
    """The fan level of an Optima 270 or 314."""
    return optima_270_setting(PointKey.FAN_LEVEL, 7, Limits(0, 4, step=1), on_write=fan_level_rereads(
        PointKey.FAN_DUTYCYCLE_SUPPLY, PointKey.FAN_DUTYCYCLE_EXTRACT, PointKey.FAN_RPM_SUPPLY,
        PointKey.FAN_RPM_EXTRACT))


def optima_270_switch(key: Key[bool], address: int) -> Point[bool]:
    """A switch of an Optima 270 or 314, written at `optima_write_address`."""
    return switch(key, address, write_address=optima_write_address(address))

# The alarm bits, as found in material published online. The filter alarm's bit is set while the
# filter must be changed, so it is `filter_ok` inverted, as every controller has that key.

ALARMS_250: tuple[Point[bool], ...] = (
    alarm_bit(PointKey.ALARM_EXTERNAL_STOP, 101, 0),
    alarm_bit(PointKey.FILTER_OK, 101, 1, inverted=True),
    alarm_bit(PointKey.ALARM_HIGH_PRESSURE, 101, 2),
    alarm_bit(PointKey.ALARM_FROST_FAILURE, 101, 3),
    alarm_bit(PointKey.ALARM_PANEL_COMMUNICATION, 101, 4),
    alarm_bit(PointKey.ALARM_EXTERNAL_FILTER, 101, 5),
    alarm_bit(PointKey.ALARM_FAN_ERROR, 101, 6),
    alarm_bit(PointKey.ALARM_SENSOR_ERROR, 101, 7),
)
"""The Optima 250's, 251's, 301's and 312's alarms."""


SLAVE_79250_POINTS: tuple[Point[Any], ...] = (
    optima_temperature(PointKey.TEMP_SUPPLY, 0),
    optima_temperature(PointKey.TEMP_OUTSIDE, 2),
    optima_temperature(PointKey.TEMP_EXHAUST, 3),
    reading(PointKey.HUMIDITY, 10, data_type=DataType.INT16, unit=Unit.PERCENT),
    reading(PointKey.ALARM_BITS, 101),
    *ALARMS_250,
    optima_percent(PointKey.FAN_DUTYCYCLE_SUPPLY, 102),
    optima_percent(PointKey.FAN_DUTYCYCLE_EXTRACT, 103),
    state(PointKey.BYPASS_ACTIVE, 104),
    optima_target(0),
    *optima_fan_presets(6),
    command(PointKey.FILTER_REPLACE_RESET, 105),
)
"""What the Optima 250, 251, 301 and 312 - slave device 79250 - share."""


SLAVE_79250_FAN_LEVEL = setting(PointKey.FAN_LEVEL, 100, Limits(0, 4, step=1), on_write=fan_level_rereads(
    PointKey.FAN_DUTYCYCLE_SUPPLY, PointKey.FAN_DUTYCYCLE_EXTRACT))
"""The fan level of the Optima 301 and 312."""
