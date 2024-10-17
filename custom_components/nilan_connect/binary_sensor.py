"""Platform for Binary Sensor integration."""

from typing import List
from nilan_proxy import NilanProxy, NilanProxyDatapointKey # type: ignore
from homeassistant.components.binary_sensor import BinarySensorDeviceClass,BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .data import get_proxy 
from .entity import NilanConnectEntityBase

async def async_setup_entry(hass: HomeAssistant, entry:ConfigEntry, async_add_entities:AddEntitiesCallback):
    """Add sensors for passed config_entry in HA."""
    proxy = get_proxy(hass, entry)
    
    new_entities:List[BinarySensorEntity] = []
    if proxy.provides_value(NilanProxyDatapointKey.ALARM_STATUS):
        new_entities.append(
            NilanConnectBinarySensor(
                proxy,
                NilanProxyDatapointKey.ALARM_STATUS,
                "mdi:alarm-bell",
                type=BinarySensorDeviceClass.PROBLEM,
            )
        )
    if proxy.provides_value(NilanProxyDatapointKey.BYPASS_ACTIVE):
        new_entities.append(
            NilanConnectBinarySensor(
                proxy,
                NilanProxyDatapointKey.BYPASS_ACTIVE,
                "mdi:valve",
                type=BinarySensorDeviceClass.OPENING,
            )
        )
    if proxy.provides_value(NilanProxyDatapointKey.DEFROST_ACTIVE):
        new_entities.append(
            NilanConnectBinarySensor(
                proxy,
                NilanProxyDatapointKey.DEFROST_ACTIVE,
                "mdi:snowflake-melt",
                type=BinarySensorDeviceClass.RUNNING,
            )
        )
    if proxy.provides_value(NilanProxyDatapointKey.FILTER_OK):
        new_entities.append(
            NilanConnectBinarySensor(
                proxy,
                NilanProxyDatapointKey.FILTER_OK,
                "mdi:air-filter",
                type=BinarySensorDeviceClass.PROBLEM,
                inverted=True
            )
        )
    if proxy.provides_value(NilanProxyDatapointKey.HUMIDITY_HIGH_ACTIVE):
        new_entities.append(
            NilanConnectBinarySensor(
                proxy,
                NilanProxyDatapointKey.HUMIDITY_HIGH_ACTIVE,
                "mdi:water-percent",
                type=BinarySensorDeviceClass.MOISTURE,
            )
        )
    if proxy.provides_value(NilanProxyDatapointKey.SACRIFICIAL_ANODE_OK):
        new_entities.append(
            NilanConnectBinarySensor(
                proxy,
                NilanProxyDatapointKey.SACRIFICIAL_ANODE_OK,
                "mdi:water-opacity",
                type=BinarySensorDeviceClass.PROBLEM,
                inverted=True,
            )
        )
    if proxy.provides_value(NilanProxyDatapointKey.WINTER_MODE_ACTIVE):
        new_entities.append(
            NilanConnectBinarySensor(
                proxy,
                NilanProxyDatapointKey.WINTER_MODE_ACTIVE,
                "mdi:sun-snowflake-variant",
            )
        )

    async_add_entities(new_entities)


class NilanConnectBinarySensor(NilanConnectEntityBase[NilanProxyDatapointKey], BinarySensorEntity): # type: ignore
    def __init__(self, proxy: NilanProxy, valueKey: NilanProxyDatapointKey, icon:str, type:BinarySensorDeviceClass|None=None, inverted:bool=False, default_enabled:bool|None = None, default_visible:bool|None = None):
        super().__init__(proxy, valueKey.value, valueKey, default_enabled=default_enabled, default_visible=default_visible)
        self._valueKey = valueKey
        self._icon = icon
        self._attr_device_class = type
        self._attr_icon = icon
        self._inverted = inverted

    @property
    def is_on(self) -> bool|None: # type: ignore
        """Fetch new state data for the sensor."""
        if self._inverted:
            return not self.proxy.get_value(self._valueKey) == 1
        return self.proxy.get_value(self._valueKey) == 1
