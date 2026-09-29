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
    Labels,
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

from ._certainty import Certainty, certainty
from ._cts400 import CTS400
from ._cts602 import CTS602, CTS602_LIGHT
from ._keys import PointKey
from ._optima import OPTIMA_250, OPTIMA_251, OPTIMA_260, OPTIMA_270, OPTIMA_301, OPTIMA_312, OPTIMA_314
from ._select import select_model
from ._states import (
    AirExchangeMode,
    Alarm,
    CentralHeatMode,
    CirculationPumpMode,
    CompressorPriority,
    ControlSensor,
    CoolingSetpoint,
    DamperTestState,
    HeatSource,
    OperationMode,
    OperationState,
    ServiceMode,
    Weekday,
)
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
    "Labels",
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
    "CTS602",
    "CTS602_LIGHT",
    "OPTIMA_250",
    "OPTIMA_251",
    "OPTIMA_260",
    "OPTIMA_270",
    "OPTIMA_301",
    "OPTIMA_312",
    "OPTIMA_314",
    "PointKey",
    "Certainty",
    "certainty",
    "WRITE_RETRY_FOR",
    "create_client",
    "select_model",
    "AirExchangeMode",
    "Alarm",
    "CentralHeatMode",
    "CirculationPumpMode",
    "CompressorPriority",
    "ControlSensor",
    "CoolingSetpoint",
    "DamperTestState",
    "HeatSource",
    "OperationMode",
    "OperationState",
    "ServiceMode",
    "Weekday",
]
