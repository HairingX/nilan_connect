"""Platform for button integration."""

from typing import List
from nilan_proxy import NilanProxy, NilanProxySetpointKey # type: ignore
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .data import get_proxy 
from .entity import NilanConnectEntityBase


async def async_setup_entry(hass: HomeAssistant, entry:ConfigEntry, async_add_entities:AddEntitiesCallback):
    """Add buttons for passed config_entry in HA."""
    proxy = get_proxy(hass, entry)
    
    new_entities:List[ButtonEntity] = []
    
    if proxy.provides_value(NilanProxySetpointKey.FILTER_REPLACE_RESET):
        new_entities.append(NilanConnectButton(proxy, NilanProxySetpointKey.FILTER_REPLACE_RESET, "mdi:air-filter", EntityCategory.CONFIG))

    if proxy.provides_value(NilanProxySetpointKey.ALARM_RESET):
        new_entities.append(NilanConnectButton(proxy, NilanProxySetpointKey.ALARM_RESET, "mdi:alarm-light", EntityCategory.CONFIG))

    async_add_entities(new_entities)


class NilanConnectButton(NilanConnectEntityBase[NilanProxySetpointKey], ButtonEntity): # type: ignore
    def __init__(self, proxy:NilanProxy, valueKey:NilanProxySetpointKey, icon:str, category: EntityCategory, default_enabled:bool|None = None, default_visible:bool|None = None):
        super().__init__(proxy, valueKey.value, valueKey, False, default_enabled=default_enabled, default_visible=default_visible)
        self._attr_icon = icon
        self._attr_entity_category = category

    async def async_press(self) -> None:
        self.proxy.set_setpoint(self._value_key, 1)
