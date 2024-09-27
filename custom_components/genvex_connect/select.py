"""Platform for sensor integration."""

from typing import List
from genvexnabto import GenvexNabto, GenvexNabtoSetpointKey # type: ignore
from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .data import get_genvexnabto
from .entity import GenvexConnectEntityBase


async def async_setup_entry(hass: HomeAssistant, entry:ConfigEntry, async_add_entities:AddEntitiesCallback):
    """Add selects for passed config_entry in HA."""
    genvex_nabto = get_genvexnabto(hass, entry)

    new_entities:List[SelectEntity] = []
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL):
        new_entities.append(GenvexConnectSelect(genvex_nabto, GenvexNabtoSetpointKey.FAN_LEVEL, "mdi:fan", default_enabled=False))
        
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.COMPRESSOR_PRIORITY):
        new_entities.append(GenvexConnectSelect(genvex_nabto, GenvexNabtoSetpointKey.COMPRESSOR_PRIORITY, "mdi:priority-high"))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.TEMP_COOLING_START_OFFSET):
        new_entities.append(GenvexConnectSelect(genvex_nabto, GenvexNabtoSetpointKey.TEMP_COOLING_START_OFFSET, "mdi:snowflake-thermometer"))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.ANTILEGIONELLA_DAY):
        new_entities.append(GenvexConnectSelect(genvex_nabto, GenvexNabtoSetpointKey.ANTILEGIONELLA_DAY, "mdi:bacteria"))

    async_add_entities(new_entities)


class GenvexConnectSelect(GenvexConnectEntityBase[GenvexNabtoSetpointKey], SelectEntity): # type: ignore
    def __init__(self, genvex_nabto: GenvexNabto, valueKey: GenvexNabtoSetpointKey, icon: str, default_enabled:bool|None = None, default_visible:bool|None = None):
        super().__init__(genvex_nabto, valueKey.value, valueKey, default_enabled=default_enabled, default_visible=default_visible)
        min = genvex_nabto.get_setpoint_min_value(valueKey)
        max = genvex_nabto.get_setpoint_max_value(valueKey)
        if min is not None: self._min = int(min)
        if max is not None: self._max = int(max)
        self._attr_icon = icon
        if self._min > self._max:
            self._attr_options = []
        else:
            self._attr_options = list(map(str, range(self._min, self._max + 1)))

    @property
    def current_option(self) -> str | None: # type: ignore
        """Return the selected entity option to represent the entity state."""
        val = self._genvex_nabto.get_value(self._value_key)
        if val is None: return None
        currentFanLevel = str(int(val))
        if currentFanLevel not in self._attr_options: return None
        return currentFanLevel

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        value = int(option)
        self._genvex_nabto.set_setpoint(self._value_key, value)