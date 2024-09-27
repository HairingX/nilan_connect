"""Platform for Binary Sensor integration."""

from typing import List
from genvexnabto import GenvexNabto, GenvexNabtoDatapointKey # type: ignore
from homeassistant.components.binary_sensor import BinarySensorDeviceClass,BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .data import get_hass_data 
from .entity import GenvexConnectEntityBase

async def async_setup_entry(hass: HomeAssistant, entry:ConfigEntry, async_add_entities:AddEntitiesCallback):
    """Add sensors for passed config_entry in HA."""
    data = get_hass_data(hass, entry)
    genvex_nabto = data["genvexnabto"]
    
    new_entities:List[BinarySensorEntity] = []
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.ALARM_STATUS):
        new_entities.append(
            GenvexConnectBinarySensor(
                genvex_nabto,
                GenvexNabtoDatapointKey.ALARM_STATUS,
                "mdi:alarm-bell",
                type=BinarySensorDeviceClass.PROBLEM,
            )
        )
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.BYPASS_ACTIVE):
        new_entities.append(
            GenvexConnectBinarySensor(
                genvex_nabto,
                GenvexNabtoDatapointKey.BYPASS_ACTIVE,
                "mdi:valve",
                type=BinarySensorDeviceClass.OPENING,
            )
        )
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.DEFROST_ACTIVE):
        new_entities.append(
            GenvexConnectBinarySensor(
                genvex_nabto,
                GenvexNabtoDatapointKey.DEFROST_ACTIVE,
                "mdi:snowflake-melt",
                type=BinarySensorDeviceClass.RUNNING,
            )
        )
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.FILTER_OK):
        new_entities.append(
            GenvexConnectBinarySensor(
                genvex_nabto,
                GenvexNabtoDatapointKey.FILTER_OK,
                "mdi:air-filter",
                type=BinarySensorDeviceClass.PROBLEM,
                inverted=True
            )
        )
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.HUMIDITY_HIGH_ACTIVE):
        new_entities.append(
            GenvexConnectBinarySensor(
                genvex_nabto,
                GenvexNabtoDatapointKey.HUMIDITY_HIGH_ACTIVE,
                "mdi:water-percent",
                type=BinarySensorDeviceClass.MOISTURE,
            )
        )
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.SACRIFICIAL_ANODE_OK):
        new_entities.append(
            GenvexConnectBinarySensor(
                genvex_nabto,
                GenvexNabtoDatapointKey.SACRIFICIAL_ANODE_OK,
                "mdi:water-opacity",
                type=BinarySensorDeviceClass.PROBLEM,
                inverted=True,
            )
        )
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.WINTER_MODE_ACTIVE):
        new_entities.append(
            GenvexConnectBinarySensor(
                genvex_nabto,
                GenvexNabtoDatapointKey.WINTER_MODE_ACTIVE,
                "mdi:sun-snowflake-variant",
            )
        )

    async_add_entities(new_entities)


class GenvexConnectBinarySensor(GenvexConnectEntityBase[GenvexNabtoDatapointKey], BinarySensorEntity): # type: ignore
    def __init__(self, genvexNabto: GenvexNabto, valueKey: GenvexNabtoDatapointKey, icon:str, type:BinarySensorDeviceClass|None=None, inverted:bool=False, default_enabled:bool|None = None, default_visible:bool|None = None):
        super().__init__(genvexNabto, valueKey.value, valueKey, default_enabled=default_enabled, default_visible=default_visible)
        self._valueKey = valueKey
        self._icon = icon
        self._attr_device_class = type
        self._attr_icon = icon
        self._inverted = inverted

    @property
    def is_on(self) -> bool|None: # type: ignore
        """Fetch new state data for the sensor."""
        if self._inverted:
            return not self._genvex_nabto.get_value(self._valueKey) == 1
        return self._genvex_nabto.get_value(self._valueKey) == 1
