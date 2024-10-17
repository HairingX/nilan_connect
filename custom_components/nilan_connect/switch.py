"""Platform for switch integration."""

from typing import Any, List
from nilan_proxy import NilanProxy, NilanProxySetpointKey # type: ignore
from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .data import get_proxy 
from .entity import NilanConnectEntityBase


async def async_setup_entry(hass: HomeAssistant, entry:ConfigEntry, async_add_entities:AddEntitiesCallback):
    """Add switches for passed config_entry in HA."""
    proxy = get_proxy(hass, entry)
    
    new_entities:List[SwitchEntity] = []
    
    if proxy.provides_value(NilanProxySetpointKey.BOOST_ENABLE):
        new_entities.append(NilanConnectSwitch(proxy, NilanProxySetpointKey.BOOST_ENABLE, "mdi:fan-chevron-up"))
    if proxy.provides_value(NilanProxySetpointKey.COOLING_ENABLE):
        new_entities.append(NilanConnectSwitch(proxy, NilanProxySetpointKey.COOLING_ENABLE, "mdi:coolant-temperature"))
    if proxy.provides_value(NilanProxySetpointKey.ENABLE):
        new_entities.append(NilanConnectSwitch(proxy, NilanProxySetpointKey.ENABLE, "mdi:power", default_enabled=False))
    if proxy.provides_value(NilanProxySetpointKey.HUMIDITY_CONTROL_ENABLE):
        new_entities.append(NilanConnectSwitch(proxy, NilanProxySetpointKey.HUMIDITY_CONTROL_ENABLE, "mdi:water-circle", default_enabled=False))
    if proxy.provides_value(NilanProxySetpointKey.PREHEAT_ENABLE):
        new_entities.append(NilanConnectSwitch(proxy, NilanProxySetpointKey.PREHEAT_ENABLE, "mdi:heating-coil"))
    if proxy.provides_value(NilanProxySetpointKey.REHEAT_ENABLE):
        new_entities.append(NilanConnectSwitch(proxy, NilanProxySetpointKey.REHEAT_ENABLE, "mdi:heating-coil"))

    async_add_entities(new_entities)


class NilanConnectSwitch(NilanConnectEntityBase[NilanProxySetpointKey], SwitchEntity): # type: ignore
    def __init__(self, proxy: NilanProxy, valueKey: NilanProxySetpointKey, icon:str, default_enabled:bool|None = None, default_visible:bool|None = None):
        super().__init__(proxy, valueKey.value, valueKey, default_enabled=default_enabled, default_visible=default_visible)
        self._valueKey = valueKey
        self._attr_device_class = SwitchDeviceClass.SWITCH
        self._attr_icon = icon

    async def async_turn_on(self, **kwargs:Any) -> None:
        """Turn the entity on."""
        self.proxy.set_setpoint(self._valueKey, 1)

    async def async_turn_off(self, **kwargs:Any) -> None:
        """Turn the entity on."""
        self.proxy.set_setpoint(self._valueKey, 0)

    @property
    def is_on(self) -> bool|None: # type: ignore
        """Fetch new state data for the switch."""
        return self.proxy.get_value(self._valueKey) == 1
