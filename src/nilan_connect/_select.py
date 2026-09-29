"""Choosing a controller's model from what its gateway's handshake says."""
from __future__ import annotations

from modbus_event_connect import Identity, Model

from ._cts400 import CTS400
from ._cts602 import CTS602, CTS602_LIGHT
from ._optima import OPTIMA_250, OPTIMA_251, OPTIMA_260, OPTIMA_270, OPTIMA_301, OPTIMA_312, OPTIMA_314

_BY_SLAVE_MODEL_79250 = {1: OPTIMA_250, 5: OPTIMA_301, 8: OPTIMA_251, 9: OPTIMA_312}


def select_model(identity: Identity) -> Model | None:
    """The model for the controller the handshake names; None for one not supported.

    A CTS400 reported device model 1140, slave device 72270 and slave device model 1 on
    2026-09-27; the other controllers' numbers were found in material published online.
    """
    device_model = identity.get("device_model")
    slave_device = identity.get("slave_device_number")
    slave_model = identity.get("slave_device_model")
    if device_model == 2010 and identity.get("device_number") == 79265:
        return OPTIMA_270
    if device_model == 2020 and identity.get("device_number") == 79280:
        return OPTIMA_314
    if device_model == 1040:
        if slave_device == 70810 and slave_model == 26:
            return OPTIMA_260
        if slave_device == 79250 and isinstance(slave_model, int):
            return _BY_SLAVE_MODEL_79250.get(slave_model)
    if device_model in (1140, 1141):
        if slave_device == 72270 and slave_model == 1:
            return CTS400
        if slave_device == 2763306:
            return CTS602_LIGHT if slave_model == 2 else CTS602
    return None
