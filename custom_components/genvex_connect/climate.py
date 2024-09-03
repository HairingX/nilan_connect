"""Platform for Climate integration."""

import logging
from homeassistant.helpers.entity import Entity
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    ClimateEntityFeature,
    HVACMode,
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
 
    new_entities.append(
        GenvexConnectClimate(
            genvexNabto,
            "hvac",
            GenvexNabtoSetpointKey.ENABLE,
            GenvexNabtoSetpointKey.FAN_LEVEL,
            GenvexNabtoSetpointKey.TEMP_TARGET,
            GenvexNabtoDatapointKey.TEMP_EXTRACT,
            GenvexNabtoDatapointKey.HUMIDITY,
            GenvexNabtoDatapointKey.DEFROST_ACTIVE,
            GenvexNabtoDatapointKey.BYPASS_ACTIVE,
        )
    )

    async_add_entities(new_entities)


class GenvexConnectClimate(GenvexConnectEntityBase, ClimateEntity):

    def __init__(
        self,
        genvexNabto: GenvexNabto,
        name:str,
        enableKey:GenvexNabtoSetpointKey,
        fanLevelKey:GenvexNabtoSetpointKey,
        tempTargetKey:GenvexNabtoSetpointKey,
        tempExtractKey:GenvexNabtoDatapointKey,
        humidityKey:GenvexNabtoDatapointKey,
        defrostActiveKey:GenvexNabtoDatapointKey,
        bypassActiveKey:GenvexNabtoDatapointKey,
    ):
        super().__init__(genvexNabto, name, fanLevelKey, False)
        self._attr_icon = "mdi:hvac"
        self._enable_turn_on_off_backwards_compatibility = False
        self._enableKey = enableKey
        self._fanLevelKey = fanLevelKey
        self._tempTargetKey = tempTargetKey
        self._tempExtractKey = tempExtractKey
        self._humidityKey = humidityKey
        self._defrostActiveKey = defrostActiveKey
        self._bypassActiveKey = bypassActiveKey
        self._attr_hvac_modes = [HVACMode.AUTO]
        self._hvacMode = HVACMode.AUTO
        self._attr_temperature_unit = self.parse_unit_of_measure(self._unit_of_measurement, UnitOfTemperature.CELSIUS)
        
        features = 0
        if genvexNabto.provides_value(enableKey):
            features |= ClimateEntityFeature.TURN_ON | ClimateEntityFeature.TURN_OFF
            self._attr_hvac_modes.append(HVACMode.OFF)
            genvexNabto.register_update_handler(enableKey, self._on_change)
        if genvexNabto.provides_value(fanLevelKey):
            min = int(genvexNabto.get_setpoint_min_value(fanLevelKey))
            max = int(genvexNabto.get_setpoint_max_value(fanLevelKey))
            if min < max:
                features |= ClimateEntityFeature.FAN_MODE
                genvexNabto.register_update_handler(fanLevelKey, self._on_change)
                self._attr_fan_modes = list(map(str, range(min, max + 1)))
        if genvexNabto.provides_value(tempTargetKey):
            features |= ClimateEntityFeature.TARGET_TEMPERATURE
            genvexNabto.register_update_handler(tempTargetKey, self._on_change)

        if features > 0:
            self._attr_supported_features = features

            genvexNabto.register_update_handler(tempExtractKey, self._on_change)
            genvexNabto.register_update_handler(humidityKey, self._on_change)

    @property
    def hvac_mode(self):
        if self.genvex_nabto.get_value(self._enableKey) == 0:
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
        if self.genvex_nabto.get_value(self._fanLevelKey) == 0:
            return HVACAction.OFF
        if self.genvex_nabto.get_value(self._defrostActiveKey) == 1:
            return HVACAction.DEFROSTING
        if self.genvex_nabto.get_value(self._bypassActiveKey) == 1:
            return HVACAction.COOLING
        return HVACAction.FAN

    @property
    def fan_mode(self):
        currentFanLevel = str(int(self.genvex_nabto.get_value(self._fanLevelKey)))
        if currentFanLevel in self._attr_fan_modes:
            return currentFanLevel
        elif len(self._attr_fan_modes) > 0:
            return self._attr_fan_modes[0]
        else:
            return None

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        _LOGGER.info(f"Wanted to set fan mode to {fan_mode}")
        fanLevel = int(fan_mode)
        self.genvex_nabto.set_setpoint(self._fanLevelKey, fanLevel)

    @property
    def current_temperature(self) -> float|None:
        if self.genvex_nabto.provides_value(self._tempExtractKey):
            return self.genvex_nabto.get_value(self._tempExtractKey)
        return None

    @property
    def target_temperature(self):
        return self.genvex_nabto.get_value(self._tempTargetKey)

    @property
    def min_temp(self):
        return self.genvex_nabto.get_setpoint_min_value(self._tempTargetKey)

    @property
    def max_temp(self):
        return self.genvex_nabto.get_setpoint_max_value(self._tempTargetKey)

    def _turn_on(self):
        self.genvex_nabto.set_setpoint(self._enableKey, 1)

    def _turn_off(self):
        self.genvex_nabto.set_setpoint(self._enableKey, 0)

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
        self.genvex_nabto.set_setpoint(self._tempTargetKey, kwargs["temperature"])
