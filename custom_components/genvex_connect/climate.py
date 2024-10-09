"""Platform for Climate integration."""

import logging
from typing import Any, List
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import ClimateEntityFeature,HVACMode,HVACAction
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from genvexnabto import GenvexNabto, GenvexNabtoDatapointKey, GenvexNabtoSetpointKey # type: ignore
from .data import get_genvexnabto 
from .entity import GenvexConnectEntityBase

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry:ConfigEntry, async_add_entities:AddEntitiesCallback):
    """Add climates for passed config_entry in HA."""
    genvex_nabto = get_genvexnabto(hass, entry)

    new_entities:List[ClimateEntity] = []
    new_entities.append(
        GenvexConnectClimate(
            genvex_nabto,
            "hvac",
            GenvexNabtoSetpointKey.ENABLE,
            GenvexNabtoSetpointKey.FAN_LEVEL,
            GenvexNabtoSetpointKey.TEMP_TARGET,
            GenvexNabtoDatapointKey.TEMP_EXTRACT,
            GenvexNabtoDatapointKey.HUMIDITY,
            GenvexNabtoDatapointKey.DEFROST_ACTIVE,
            GenvexNabtoDatapointKey.BYPASS_ACTIVE,
            GenvexNabtoDatapointKey.HUMIDITY_HIGH_ACTIVE,
        )
    )

    async_add_entities(new_entities)


class GenvexConnectClimate(GenvexConnectEntityBase[GenvexNabtoSetpointKey], ClimateEntity): # type: ignore

    def __init__(
        self,
        genvex_nabto: GenvexNabto,
        name:str,
        enable_key:GenvexNabtoSetpointKey,
        fan_level_key:GenvexNabtoSetpointKey,
        temp_target_key:GenvexNabtoSetpointKey,
        temp_extract_key:GenvexNabtoDatapointKey,
        humidity_key:GenvexNabtoDatapointKey,
        defrost_active_key:GenvexNabtoDatapointKey,
        bypass_active_key:GenvexNabtoDatapointKey,
        humidity_high_active_key:GenvexNabtoDatapointKey,
    ):
        super().__init__(genvex_nabto, name, fan_level_key, False)
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
        if genvex_nabto.provides_value(enable_key):
            # features |= ClimateEntityFeature.TURN_ON | ClimateEntityFeature.TURN_OFF
            self._attr_hvac_modes.append(HVACMode.OFF)
        if genvex_nabto.provides_value(fan_level_key):
            min = int(genvex_nabto.get_setpoint_min_value(fan_level_key) or 0)
            max = int(genvex_nabto.get_setpoint_max_value(fan_level_key) or 0)
            if min < max:
                features |= ClimateEntityFeature.FAN_MODE
                self._attr_fan_modes = list(map(str, range(min, max + 1)))
        if genvex_nabto.provides_value(temp_target_key):
            features |= ClimateEntityFeature.TARGET_TEMPERATURE
        if features > 0: self._attr_supported_features = features

    async def async_added_to_hass(self) -> None:
        self._genvex_nabto.register_update_handler(self._fan_level_key, self._on_change)
        self._genvex_nabto.register_update_handler(self._enable_key, self._on_change)
        self._genvex_nabto.register_update_handler(self._temp_target_key, self._on_change)
        self._genvex_nabto.register_update_handler(self._temp_extract_key, self._on_change)
        self._genvex_nabto.register_update_handler(self._humidity_key, self._on_change)
        self._genvex_nabto.register_update_handler(self._defrost_active_key, self._on_change)
        self._genvex_nabto.register_update_handler(self._bypass_active_key, self._on_change)
        self._genvex_nabto.register_update_handler(self._humidity_high_active_key, self._on_change)

    async def async_will_remove_from_hass(self) -> None:
        self._genvex_nabto.deregister_update_handler(self._fan_level_key, self._on_change)
        self._genvex_nabto.deregister_update_handler(self._enable_key, self._on_change)
        self._genvex_nabto.deregister_update_handler(self._temp_target_key, self._on_change)
        self._genvex_nabto.deregister_update_handler(self._temp_extract_key, self._on_change)
        self._genvex_nabto.deregister_update_handler(self._humidity_key, self._on_change)
        self._genvex_nabto.deregister_update_handler(self._defrost_active_key, self._on_change)
        self._genvex_nabto.deregister_update_handler(self._bypass_active_key, self._on_change)
        self._genvex_nabto.deregister_update_handler(self._humidity_high_active_key, self._on_change)
        

    @property
    def hvac_action(self): # type: ignore
        if self._genvex_nabto.get_value(self._fan_level_key) == 0 or self._genvex_nabto.get_value(self._enable_key) == 0:
            return HVACAction.OFF
        if self._genvex_nabto.get_value(self._defrost_active_key) == 1:
            return HVACAction.DEFROSTING
        if self._genvex_nabto.get_value(self._humidity_high_active_key) == 1:
            return HVACAction.DRYING
        if self._genvex_nabto.get_value(self._bypass_active_key) == 1:
            return HVACAction.COOLING
        return HVACAction.FAN

    @property
    def hvac_mode(self): # type: ignore
        if self._genvex_nabto.get_value(self._enable_key) == 0:
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
            currentFanLevel = str(int(self._genvex_nabto.get_value(self._fan_level_key) or -1))
            if currentFanLevel in self._attr_fan_modes:
                return currentFanLevel
            # elif len(self._attr_fan_modes) > 0:
            #     return self._attr_fan_modes[0]
        return None

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        _LOGGER.info(f"Wanted to set fan mode to {fan_mode}")
        fanLevel = int(fan_mode)
        self._genvex_nabto.set_setpoint(self._fan_level_key, fanLevel)

    @property
    def current_temperature(self) -> float|None: # type: ignore
        if self._genvex_nabto.provides_value(self._temp_extract_key):
            return self._genvex_nabto.get_value(self._temp_extract_key)
        return None
    
    @property
    def current_humidity(self) -> float|None: # type: ignore
        if self._genvex_nabto.provides_value(self._humidity_key):
            return self._genvex_nabto.get_value(self._humidity_key)
        return None

    @property
    def target_temperature(self): # type: ignore
        return self._genvex_nabto.get_value(self._temp_target_key)

    @property
    def min_temp(self): # type: ignore
        return self._genvex_nabto.get_setpoint_min_value(self._temp_target_key)

    @property
    def max_temp(self): # type: ignore
        return self._genvex_nabto.get_setpoint_max_value(self._temp_target_key)

    def _turn_on(self):
        self._genvex_nabto.set_setpoint(self._enable_key, 1)

    def _turn_off(self):
        self._genvex_nabto.set_setpoint(self._enable_key, 0)

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
            self._genvex_nabto.set_setpoint(self._temp_target_key, float(temp))
