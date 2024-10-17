"""Platform for Climate integration."""

import logging
from typing import Any, List
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import ClimateEntityFeature,HVACMode,HVACAction
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from nilan_proxy import NilanProxy, NilanProxyDatapointKey, NilanProxySetpointKey # type: ignore
from .data import get_proxy 
from .entity import NilanConnectEntityBase

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry:ConfigEntry, async_add_entities:AddEntitiesCallback):
    """Add climates for passed config_entry in HA."""
    proxy = get_proxy(hass, entry)

    new_entities:List[ClimateEntity] = []
    new_entities.append(
        NilanConnectClimate(
            proxy,
            "hvac",
            NilanProxySetpointKey.ENABLE,
            NilanProxySetpointKey.FAN_LEVEL,
            NilanProxySetpointKey.TEMP_TARGET,
            NilanProxyDatapointKey.TEMP_EXTRACT,
            NilanProxyDatapointKey.HUMIDITY,
            NilanProxyDatapointKey.DEFROST_ACTIVE,
            NilanProxyDatapointKey.BYPASS_ACTIVE,
            NilanProxyDatapointKey.HUMIDITY_HIGH_ACTIVE,
        )
    )

    async_add_entities(new_entities)


class NilanConnectClimate(NilanConnectEntityBase[NilanProxySetpointKey], ClimateEntity): # type: ignore

    def __init__(
        self,
        proxy: NilanProxy,
        name:str,
        enable_key:NilanProxySetpointKey,
        fan_level_key:NilanProxySetpointKey,
        temp_target_key:NilanProxySetpointKey,
        temp_extract_key:NilanProxyDatapointKey,
        humidity_key:NilanProxyDatapointKey,
        defrost_active_key:NilanProxyDatapointKey,
        bypass_active_key:NilanProxyDatapointKey,
        humidity_high_active_key:NilanProxyDatapointKey,
    ):
        super().__init__(proxy, name, fan_level_key, False)
        self._attr_icon = "mdi:hvac"
        self._enable_turn_on_off_backwards_compatibility = False
        self._enable_key = enable_key
        self._fan_level_key = fan_level_key
        self._temp_target_key = temp_target_key
        self._temp_extract_key = temp_extract_key
        self._humidity_key = humidity_key
        self._defrost_active_key = defrost_active_key
        self._bypass_active_key = bypass_active_key
        self._humidity_high_active_key = humidity_high_active_key
        self._attr_hvac_modes = [HVACMode.AUTO]
        self._hvacMode = HVACMode.AUTO
        self._attr_temperature_unit = self.parse_unit_of_measure(self._unit_of_measurement, UnitOfTemperature.CELSIUS)
        
        features:ClimateEntityFeature = ClimateEntityFeature(0)
        if proxy.provides_value(enable_key):
            # features |= ClimateEntityFeature.TURN_ON | ClimateEntityFeature.TURN_OFF
            self._attr_hvac_modes.append(HVACMode.OFF)
        if proxy.provides_value(fan_level_key):
            min = int(proxy.get_setpoint_min_value(fan_level_key) or 0)
            max = int(proxy.get_setpoint_max_value(fan_level_key) or 0)
            if min < max:
                features |= ClimateEntityFeature.FAN_MODE
                self._attr_fan_modes = list(map(str, range(min, max + 1)))
        if proxy.provides_value(temp_target_key):
            features |= ClimateEntityFeature.TARGET_TEMPERATURE
        if features > 0: self._attr_supported_features = features

    async def async_added_to_hass(self) -> None:
        self.proxy.register_update_handler(self._fan_level_key, self._on_change)
        self.proxy.register_update_handler(self._enable_key, self._on_change)
        self.proxy.register_update_handler(self._temp_target_key, self._on_change)
        self.proxy.register_update_handler(self._temp_extract_key, self._on_change)
        self.proxy.register_update_handler(self._humidity_key, self._on_change)
        self.proxy.register_update_handler(self._defrost_active_key, self._on_change)
        self.proxy.register_update_handler(self._bypass_active_key, self._on_change)
        self.proxy.register_update_handler(self._humidity_high_active_key, self._on_change)

    async def async_will_remove_from_hass(self) -> None:
        self.proxy.deregister_update_handler(self._fan_level_key, self._on_change)
        self.proxy.deregister_update_handler(self._enable_key, self._on_change)
        self.proxy.deregister_update_handler(self._temp_target_key, self._on_change)
        self.proxy.deregister_update_handler(self._temp_extract_key, self._on_change)
        self.proxy.deregister_update_handler(self._humidity_key, self._on_change)
        self.proxy.deregister_update_handler(self._defrost_active_key, self._on_change)
        self.proxy.deregister_update_handler(self._bypass_active_key, self._on_change)
        self.proxy.deregister_update_handler(self._humidity_high_active_key, self._on_change)
        

    @property
    def hvac_action(self): # type: ignore
        if self.proxy.get_value(self._fan_level_key) == 0 or self.proxy.get_value(self._enable_key) == 0:
            return HVACAction.OFF
        if self.proxy.get_value(self._defrost_active_key) == 1:
            return HVACAction.DEFROSTING
        if self.proxy.get_value(self._humidity_high_active_key) == 1:
            return HVACAction.DRYING
        if self.proxy.get_value(self._bypass_active_key) == 1:
            return HVACAction.COOLING
        return HVACAction.FAN

    @property
    def hvac_mode(self): # type: ignore
        if self.proxy.get_value(self._enable_key) == 0:
            return HVACMode.OFF
        return self._hvacMode

    def set_hvac_mode(self, _hvac_mode: HVACMode): # type: ignore
        _LOGGER.info(f"Wanted to set hvac mode to {_hvac_mode}")
        if _hvac_mode == HVACMode.OFF:
            self._turn_off()
        elif _hvac_mode == HVACMode.AUTO:
            self._turn_on()

    @property
    def fan_mode(self): # type: ignore
        if self._attr_fan_modes is not None:
            currentFanLevel = str(int(self.proxy.get_value(self._fan_level_key) or -1))
            if currentFanLevel in self._attr_fan_modes:
                return currentFanLevel
            # elif len(self._attr_fan_modes) > 0:
            #     return self._attr_fan_modes[0]
        return None

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        _LOGGER.info(f"Wanted to set fan mode to {fan_mode}")
        fanLevel = int(fan_mode)
        self.proxy.set_setpoint(self._fan_level_key, fanLevel)

    @property
    def current_temperature(self) -> float|None: # type: ignore
        if self.proxy.provides_value(self._temp_extract_key):
            return self.proxy.get_value(self._temp_extract_key)
        return None
    
    @property
    def current_humidity(self) -> float|None: # type: ignore
        if self.proxy.provides_value(self._humidity_key):
            return self.proxy.get_value(self._humidity_key)
        return None

    @property
    def target_temperature(self): # type: ignore
        return self.proxy.get_value(self._temp_target_key)

    @property
    def min_temp(self): # type: ignore
        return self.proxy.get_setpoint_min_value(self._temp_target_key)

    @property
    def max_temp(self): # type: ignore
        return self.proxy.get_setpoint_max_value(self._temp_target_key)

    def _turn_on(self):
        self.proxy.set_setpoint(self._enable_key, 1)

    def _turn_off(self):
        self.proxy.set_setpoint(self._enable_key, 0)

    # async def async_turn_on(self):
    #     """Turn the entity on."""
    #     _LOGGER.info(f"Wanted to turn on")
    #     self.set_hvac_mode(HVACMode.AUTO)

    # async def async_turn_off(self):
    #     """Turn the entity off."""
    #     _LOGGER.info(f"Wanted to turn off")
    #     self.set_hvac_mode(HVACMode.OFF)

    async def async_set_temperature(self, **kwargs:Any) -> None:
        """Set the target temperature"""
        temp = kwargs["temperature"]
        if temp is not None:
            self.proxy.set_setpoint(self._temp_target_key, float(temp))
