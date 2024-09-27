"""Platform for button integration."""

from typing import List
from genvexnabto import GenvexNabto, GenvexNabtoSetpointKey # type: ignore
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .data import get_genvexnabto 
from .entity import GenvexConnectEntityBase


async def async_setup_entry(hass: HomeAssistant, entry:ConfigEntry, async_add_entities:AddEntitiesCallback):
    """Add buttons for passed config_entry in HA."""
    genvex_nabto = get_genvexnabto(hass, entry)
    
    new_entities:List[ButtonEntity] = []
    
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.FILTER_REPLACE_RESET):
        new_entities.append(GenvexConnectButton(genvex_nabto, GenvexNabtoSetpointKey.FILTER_REPLACE_RESET, "mdi:air-filter", EntityCategory.CONFIG))

    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.ALARM_RESET):
        new_entities.append(GenvexConnectButton(genvex_nabto, GenvexNabtoSetpointKey.ALARM_RESET, "mdi:alarm-light", EntityCategory.CONFIG))

    async_add_entities(new_entities)


class GenvexConnectButton(GenvexConnectEntityBase[GenvexNabtoSetpointKey], ButtonEntity): # type: ignore
    def __init__(self, genvex_nabto:GenvexNabto, valueKey:GenvexNabtoSetpointKey, icon:str, category: EntityCategory, default_enabled:bool|None = None, default_visible:bool|None = None):
        super().__init__(genvex_nabto, valueKey.value, valueKey, False, default_enabled=default_enabled, default_visible=default_visible)
        self._attr_icon = icon
        self._attr_entity_category = category

    async def async_press(self) -> None:
        self._genvex_nabto.set_setpoint(self._value_key, 1)
