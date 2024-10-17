"""Platform for sensor integration."""

from typing import List
from nilan_proxy import NilanProxy, NilanProxySetpointKey # type: ignore
from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .data import get_proxy
from .entity import NilanConnectEntityBase


async def async_setup_entry(hass: HomeAssistant, entry:ConfigEntry, async_add_entities:AddEntitiesCallback):
    """Add selects for passed config_entry in HA."""
    proxy = get_proxy(hass, entry)

    new_entities:List[SelectEntity] = []
    if proxy.provides_value(NilanProxySetpointKey.FAN_LEVEL):
        new_entities.append(NilanConnectSelect(proxy, NilanProxySetpointKey.FAN_LEVEL, "mdi:fan", default_enabled=False))
        
    if proxy.provides_value(NilanProxySetpointKey.COMPRESSOR_PRIORITY):
        new_entities.append(NilanConnectSelect(proxy, NilanProxySetpointKey.COMPRESSOR_PRIORITY, "mdi:priority-high"))
    if proxy.provides_value(NilanProxySetpointKey.TEMP_COOLING_START_OFFSET):
        new_entities.append(NilanConnectSelect(proxy, NilanProxySetpointKey.TEMP_COOLING_START_OFFSET, "mdi:snowflake-thermometer"))
    if proxy.provides_value(NilanProxySetpointKey.ANTILEGIONELLA_DAY):
        new_entities.append(NilanConnectSelect(proxy, NilanProxySetpointKey.ANTILEGIONELLA_DAY, "mdi:bacteria"))

    async_add_entities(new_entities)


class NilanConnectSelect(NilanConnectEntityBase[NilanProxySetpointKey], SelectEntity): # type: ignore
    def __init__(self, proxy: NilanProxy, valueKey: NilanProxySetpointKey, icon: str, default_enabled:bool|None = None, default_visible:bool|None = None):
        super().__init__(proxy, valueKey.value, valueKey, default_enabled=default_enabled, default_visible=default_visible)
        min = proxy.get_setpoint_min_value(valueKey)
        max = proxy.get_setpoint_max_value(valueKey)
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
        val = self.proxy.get_value(self._value_key)
        if val is None: return None
        currentFanLevel = str(int(val))
        if currentFanLevel not in self._attr_options: return None
        return currentFanLevel

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        value = int(option)
        self.proxy.set_setpoint(self._value_key, value)