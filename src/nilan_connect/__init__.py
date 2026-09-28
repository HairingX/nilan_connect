"""Nilan ventilation units behind a Nilan gateway, over micro_nabto, built on modbus_event_connect.

Everything a user of a Nilan controller needs is here, so that nothing has to be imported from
modbus_event_connect: the client and its values, what a point is, the errors, and discovery.
"""
from importlib.metadata import version as _installed_version

from modbus_event_connect import (
    AuthenticationError,
    CannotConnectError,
    Client,
    ClientError,
    Clock,
    DataValue,
    Identity,
    InvalidValueError,
    Key,
    Limits,
    ModelError,
    NotConnectedError,
    Point,
    PointsCallback,
    PollRate,
    Quality,
    ReadOnlyError,
    Status,
    StatusCallback,
    Unit,
    UnsupportedDeviceError,
    ValueCallback,
    Write,
    WriteKind,
)
from modbus_event_connect.micro_nabto import DiscoveredDevice, discover

from ._model import CTS400, PointKey, select_model
from ._nilan import WRITE_RETRY_FOR, create_client

__version__ = _installed_version("nilan_connect")
__all__ = [
    "AuthenticationError",
    "CannotConnectError",
    "Client",
    "ClientError",
    "Clock",
    "DataValue",
    "Identity",
    "InvalidValueError",
    "Key",
    "Limits",
    "ModelError",
    "NotConnectedError",
    "Point",
    "PointsCallback",
    "PollRate",
    "Quality",
    "ReadOnlyError",
    "Status",
    "StatusCallback",
    "Unit",
    "UnsupportedDeviceError",
    "ValueCallback",
    "Write",
    "WriteKind",
    "DiscoveredDevice",
    "discover",
    "CTS400",
    "PointKey",
    "WRITE_RETRY_FOR",
    "create_client",
    "select_model",
]
