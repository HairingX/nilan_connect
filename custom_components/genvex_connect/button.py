"""Platform for button integration."""

from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import EntityCategory
from genvexnabto import GenvexNabto, GenvexNabto, GenvexNabtoSetpointKey
from .entity import GenvexConnectEntityBase

from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    genvexNabto: GenvexNabto = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = []
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.FILTER_REPLACE_RESET):
        new_entities.append(GenvexConnectButton(genvexNabto, GenvexNabtoSetpointKey.FILTER_REPLACE_RESET, "mdi:air-filter"))

    if genvexNabto.provides_value(GenvexNabtoSetpointKey.ALARM_RESET):
        new_entities.append(GenvexConnectButton(genvexNabto, GenvexNabtoSetpointKey.ALARM_RESET, "mdi:alarm-light"))

    async_add_entities(new_entities)


class GenvexConnectButton(GenvexConnectEntityBase, ButtonEntity):
    def __init__(self, genvexNabto:GenvexNabto, valueKey:GenvexNabtoSetpointKey, icon:str):
        super().__init__(genvexNabto, valueKey.value, valueKey, False)
        self._valueKey = valueKey
        self._icon = icon
        self._attr_icon = icon
        self._attr_entity_category = EntityCategory.CONFIG

    async def async_press(self) -> None:
        self.genvex_nabto.set_setpoint(self._valueKey, 1)
