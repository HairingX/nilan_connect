"""Platform for Climate integration."""

import logging
from homeassistant.helpers.entity import Entity
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    ClimateEntityFeature,
    HVACMode,
    FAN_OFF,
    FAN_LOW,
    FAN_MIDDLE,
    FAN_MEDIUM,
    FAN_HIGH,
    HVACAction,
)
from homeassistant.const import UnitOfTemperature
from genvexnabto import GenvexNabto, GenvexNabtoDatapointKey, GenvexNabtoSetpointKey
from .entity import GenvexConnectEntityBase

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    genvexNabto: GenvexNabto = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = []
    if (
        genvexNabto.providesValue(GenvexNabtoSetpointKey.FAN_SPEED)
        and genvexNabto.providesValue(GenvexNabtoSetpointKey.TEMP_SETPOINT)
        and genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_EXTRACT)
        and genvexNabto.providesValue(GenvexNabtoDatapointKey.HUMIDITY)
    ):
        if genvexNabto.providesValue(GenvexNabtoSetpointKey.VENTILATION_ENABLE):
            ventilationEnableKey = GenvexNabtoSetpointKey.VENTILATION_ENABLE

        new_entities.append(
            GenvexConnectClimate(
                genvexNabto,
                "ventilation",
                ventilationEnableKey,
                fanSetKey=GenvexNabtoSetpointKey.FAN_SPEED,
                tempSetKey=GenvexNabtoSetpointKey.TEMP_SETPOINT,
                extractAirKey=GenvexNabtoDatapointKey.TEMP_EXTRACT,
                humidityKey=GenvexNabtoDatapointKey.HUMIDITY,
            )
        )
    async_add_entities(new_entities)


class GenvexConnectClimate(GenvexConnectEntityBase, ClimateEntity):

    def __init__(self, genvexNabto, name, ventilationEnableKey, fanSetKey, tempSetKey, extractAirKey, humidityKey):
        super().__init__(genvexNabto, name, fanSetKey, False)
        self._enable_turn_on_off_backwards_compatibility = False
        self._ventilationEnableKey = ventilationEnableKey
        self._fanSetKey = fanSetKey
        self._tempSetKey = tempSetKey
        self._extractAirKey = extractAirKey
        self._humidityKey = humidityKey
        self._features = ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.FAN_MODE 
        self._hvacModes = [HVACMode.AUTO]
        self._hvacMode = HVACMode.AUTO
        if self._ventilationEnableKey is not None:
            self._features |= ClimateEntityFeature.TURN_ON | ClimateEntityFeature.TURN_OFF
            self._hvacModes.append(HVACMode.OFF)
            genvexNabto.registerUpdateHandler(ventilationEnableKey, self._on_change)
            
        genvexNabto.registerUpdateHandler(fanSetKey, self._on_change)
        genvexNabto.registerUpdateHandler(tempSetKey, self._on_change)
        genvexNabto.registerUpdateHandler(extractAirKey, self._on_change)
        genvexNabto.registerUpdateHandler(humidityKey, self._on_change)
        genvexNabto.registerUpdateHandler(humidityKey, self._on_change)

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return self._features

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:hvac"

    @property
    def hvac_modes(self):
         return self._hvacModes

    @property
    def hvac_mode(self):
        if self.genvexNabto.getValue(self._ventilationEnableKey) == 0:
            return HVACMode.OFF
        return self._hvacMode

    def set_hvac_mode(self, _hvac_mode):
        _LOGGER.info(f"Wanted to set hvac mode to {_hvac_mode}")
        if _hvac_mode == HVACMode.OFF:
            self._turn_off()
        elif _hvac_mode == HVACMode.AUTO:
            self._turn_on()

    @property
    def hvac_action(self):
        if self.genvexNabto.getValue(self._fanSetKey) == 0:
            return HVACAction.OFF
        return HVACAction.FAN

    @property
    def fan_modes(self):
        min = self.genvexNabto.getSetpointMinValue(self._fanSetKey)
        max = self.genvexNabto.getSetpointMaxValue(self._fanSetKey)
        modes = []
        if min == 0:
            modes.append(FAN_OFF)
        if min <= 1 and max >= 1:
            modes.append(FAN_LOW)
        if min <= 2 and max >= 2:
            modes.append(FAN_MIDDLE)
        if min <= 3 and max >= 3:
            modes.append(FAN_MEDIUM)
        if min <= 4 and max >= 4:
            modes.append(FAN_HIGH)
        return modes

    @property
    def fan_mode(self):
        fanValue = self.genvexNabto.getValue(self._fanSetKey)
        if fanValue == 0:
            return FAN_OFF
        elif fanValue == 1:
            return FAN_LOW
        elif fanValue == 2:
            return FAN_MIDDLE
        elif fanValue == 3:
            return FAN_MEDIUM
        elif fanValue == 4:
            return FAN_HIGH

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        _LOGGER.info(f"Wanted to set fan mode to {fan_mode}")
        speed = 2
        if fan_mode == FAN_OFF:
            speed = 0
        elif fan_mode == FAN_LOW:
            speed = 1
        elif fan_mode == FAN_MIDDLE:
            speed = 2
        elif fan_mode == FAN_MEDIUM:
            speed = 3
        elif fan_mode == FAN_HIGH:
            speed = 4
        self.genvexNabto.setSetpoint(self._fanSetKey, speed)

    @property
    def temperature_unit(self):
        return UnitOfTemperature.CELSIUS

    @property
    def current_temperature(self):
        return self.genvexNabto.getValue(self._extractAirKey)

    @property
    def target_temperature(self):
        return self.genvexNabto.getValue(self._tempSetKey)

    @property
    def min_temp(self):
        return self.genvexNabto.getSetpointMinValue(self._tempSetKey)

    @property
    def max_temp(self):
        return self.genvexNabto.getSetpointMaxValue(self._tempSetKey)

    def _turn_on(self):
        if self._ventilationEnableKey is not None:
            _LOGGER.info(f"turning on")
            self.genvexNabto.setSetpoint(self._ventilationEnableKey, 1)
        else:
            _LOGGER.info(f"turn on not supported")
            
    def _turn_off(self):
        if self._ventilationEnableKey is not None:
            _LOGGER.info(f"turning off")
            self.genvexNabto.setSetpoint(self._ventilationEnableKey, 0)
        else:
            _LOGGER.info(f"turn off not supported")
 
    async def async_turn_on(self):
        """Turn the entity on."""
        _LOGGER.info(f"Wanted to turn on")
        self.set_hvac_mode(HVACMode.AUTO)

    async def async_turn_off(self):
        """Turn the entity off."""
        _LOGGER.info(f"Wanted to turn off")
        self.set_hvac_mode(HVACMode.OFF)

    async def async_set_temperature(self, **kwargs) -> None:
        """Set the target temperature"""
        self.genvexNabto.setSetpoint(self._tempSetKey, kwargs["temperature"])
