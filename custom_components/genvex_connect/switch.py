"""Platform for switch integration."""

from typing import Any, List
from genvexnabto import GenvexNabto, GenvexNabtoSetpointKey # type: ignore
from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .data import getGenvexNabto 
from .entity import GenvexConnectEntityBase


async def async_setup_entry(hass: HomeAssistant, entry:ConfigEntry, async_add_entities:AddEntitiesCallback):
    """Add switches for passed config_entry in HA."""
    genvex_nabto = getGenvexNabto(hass, entry)
    
    new_entities:List[SwitchEntity] = []
    
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.BOOST_ENABLE):
        new_entities.append(GenvexConnectSwitch(genvex_nabto, GenvexNabtoSetpointKey.BOOST_ENABLE, "mdi:fan-chevron-up"))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.COOLING_ENABLE):
        new_entities.append(GenvexConnectSwitch(genvex_nabto, GenvexNabtoSetpointKey.COOLING_ENABLE, "mdi:coolant-temperature"))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.ENABLE):
        new_entities.append(GenvexConnectSwitch(genvex_nabto, GenvexNabtoSetpointKey.ENABLE, "mdi:power", default_enabled=False))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.HUMIDITY_CONTROL_ENABLE):
        new_entities.append(GenvexConnectSwitch(genvex_nabto, GenvexNabtoSetpointKey.HUMIDITY_CONTROL_ENABLE, "mdi:water-circle", default_enabled=False))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.PREHEAT_ENABLE):
        new_entities.append(GenvexConnectSwitch(genvex_nabto, GenvexNabtoSetpointKey.PREHEAT_ENABLE, "mdi:heating-coil"))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.REHEAT_ENABLE):
        new_entities.append(GenvexConnectSwitch(genvex_nabto, GenvexNabtoSetpointKey.REHEAT_ENABLE, "mdi:heating-coil"))

    async_add_entities(new_entities)


class GenvexConnectSwitch(GenvexConnectEntityBase[GenvexNabtoSetpointKey], SwitchEntity): # type: ignore
    def __init__(self, genvexNabto: GenvexNabto, valueKey: GenvexNabtoSetpointKey, icon:str, default_enabled:bool|None = None, default_visible:bool|None = None):
        super().__init__(genvexNabto, valueKey.value, valueKey, default_enabled=default_enabled, default_visible=default_visible)
        self._valueKey = valueKey
        self._attr_device_class = SwitchDeviceClass.SWITCH
        self._attr_icon = icon

    async def async_turn_on(self, **kwargs:Any) -> None:
        """Turn the entity on."""
        self.genvex_nabto.set_setpoint(self._valueKey, 1)

    async def async_turn_off(self, **kwargs:Any) -> None:
        """Turn the entity on."""
        self.genvex_nabto.set_setpoint(self._valueKey, 0)

    @property
    def is_on(self) -> bool|None: # type: ignore
        """Fetch new state data for the switch."""
        return self.genvex_nabto.get_value(self._valueKey) == 1
