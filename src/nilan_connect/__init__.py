"""Nilan ventilation units behind a Nilan gateway, over micro_nabto, built on modbus_event_connect.

Everything a user of a Nilan controller needs is here, so that nothing has to be imported from
modbus_event_connect: the client and its values, what a point is, the errors, and discovery.
"""
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
from ._nilan import create_client

__version__ = "0.2.0rc1"
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
    "create_client",
    "select_model",
]
