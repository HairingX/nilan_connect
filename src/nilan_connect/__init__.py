"""Nilan ventilation units behind a Nilan gateway, over micro_nabto, built on modbus_event_connect.

Everything a user of a Nilan controller needs is here, so that nothing has to be imported from
modbus_event_connect or event_connect: the client and its values, what a point is, how certain it
is and the range it can be written with, the level of certainty a client uses and the candidates
tried at its Test level, the raw snapshots a mapping of the unit reads, the errors, and discovery.
"""
from importlib.metadata import version as _installed_version

from event_connect import (
    Area,
    AuthenticationError,
    Candidate,
    CannotConnectError,
    Certainty,
    Change,
    ClientError,
    Clock,
    DataValue,
    DeviceClient,
    Identity,
    InvalidValueError,
    Key,
    Labels,
    Level,
    Limits,
    ModelError,
    NotConnectedError,
    PointsCallback,
    PollRate,
    Quality,
    RawAddress,
    ReadOnlyError,
    RegisterChange,
    Selector,
    Snapshot,
    Status,
    StatusCallback,
    Unit,
    UnsupportedDeviceError,
    ValueCallback,
    Write,
    WriteKind,
    WriteRange,
    difference,
)
from modbus_event_connect import Client, Point
from modbus_event_connect.micro_nabto import PORT, MicroNabtoModel

from ._cts400 import CTS400
from ._cts602 import CTS602
from ._cts602_light import CTS602_LIGHT
from ._keys import PointKey
from ._optima_250 import OPTIMA_250
from ._optima_251 import OPTIMA_251
from ._optima_260 import OPTIMA_260
from ._optima_270 import OPTIMA_270
from ._optima_301 import OPTIMA_301
from ._optima_312 import OPTIMA_312
from ._optima_314 import OPTIMA_314
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
    ElectricCoil,
    ExtraSensor,
    FilterReplaceInterval,
    HeatSource,
    OperationMode,
    OperationState,
    ServiceMode,
    Weekday,
)
from ._nilan import MODELS, DiscoveredDevice, create_client, discover, model_points

__version__ = _installed_version("nilan_connect")
__all__ = [
    "AuthenticationError",
    "CannotConnectError",
    "Certainty",
    "Change",
    "ClientError",
    "Clock",
    "DataValue",
    "DeviceClient",
    "Identity",
    "InvalidValueError",
    "Key",
    "Labels",
    "Limits",
    "ModelError",
    "NotConnectedError",
    "PointsCallback",
    "PollRate",
    "Quality",
    "ReadOnlyError",
    "Selector",
    "Status",
    "StatusCallback",
    "Unit",
    "UnsupportedDeviceError",
    "ValueCallback",
    "Write",
    "WriteKind",
    "WriteRange",
    "Area",
    "RawAddress",
    "RegisterChange",
    "Snapshot",
    "difference",
    "Level",
    "Candidate",
    "Client",
    "Point",
    "MicroNabtoModel",
    "PORT",
    "DiscoveredDevice",
    "create_client",
    "discover",
    "MODELS",
    "model_points",
    "select_model",
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
    "AirExchangeMode",
    "Alarm",
    "CentralHeatMode",
    "CirculationPumpMode",
    "CompressorPriority",
    "ControlSensor",
    "CoolingSetpoint",
    "DamperTestState",
    "ElectricCoil",
    "ExtraSensor",
    "FilterReplaceInterval",
    "HeatSource",
    "OperationMode",
    "OperationState",
    "ServiceMode",
    "Weekday",
]
