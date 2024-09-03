"""Platform for Binary Sensor integration."""

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from genvexnabto import GenvexNabto, GenvexNabtoDatapointKey
from .entity import GenvexConnectEntityBase

from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    genvexNabto: GenvexNabto = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = []
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.ALARM_STATUS):
        new_entities.append(
            GenvexConnectBinarySensor(
                genvexNabto,
                GenvexNabtoDatapointKey.ALARM_STATUS,
                "mdi:alarm-bell",
                type=BinarySensorDeviceClass.PROBLEM,
            )
        )
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.BYPASS_ACTIVE):
        new_entities.append(
            GenvexConnectBinarySensor(
                genvexNabto,
                GenvexNabtoDatapointKey.BYPASS_ACTIVE,
                "mdi:valve",
                type=BinarySensorDeviceClass.OPENING,
            )
        )
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.DEFROST_ACTIVE):
        new_entities.append(
            GenvexConnectBinarySensor(
                genvexNabto,
                GenvexNabtoDatapointKey.DEFROST_ACTIVE,
                "mdi:snowflake-melt",
                type=BinarySensorDeviceClass.RUNNING,
            )
        )
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.FILTER_OK):
        new_entities.append(
            GenvexConnectBinarySensor(
                genvexNabto,
                GenvexNabtoDatapointKey.FILTER_OK,
                "mdi:air-filter",
                type=BinarySensorDeviceClass.PROBLEM,
                inverted=True
            )
        )
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.SACRIFICIAL_ANODE_OK):
        new_entities.append(
            GenvexConnectBinarySensor(
                genvexNabto,
                GenvexNabtoDatapointKey.SACRIFICIAL_ANODE_OK,
                "mdi:water-opacity",
                type=BinarySensorDeviceClass.PROBLEM,
                inverted=True,
            )
        )
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.WINTER_MODE_ACTIVE):
        new_entities.append(
            GenvexConnectBinarySensor(
                genvexNabto,
                GenvexNabtoDatapointKey.WINTER_MODE_ACTIVE,
                "mdi:sun-snowflake-variant",
            )
        )

    async_add_entities(new_entities)


class GenvexConnectBinarySensor(GenvexConnectEntityBase, BinarySensorEntity):
    def __init__(self, genvexNabto: GenvexNabto, valueKey: GenvexNabtoDatapointKey, icon:str, type:BinarySensorDeviceClass|None=None, inverted:bool=False):
        super().__init__(genvexNabto, valueKey.value, valueKey)
        self._valueKey = valueKey
        self._icon = icon
        self._attr_device_class = type
        self._attr_icon = icon
        self._inverted = inverted

    @property
    def is_on(self) -> bool|None:
        """Fetch new state data for the sensor."""
        if self._inverted:
            return not self.genvex_nabto.get_value(self._valueKey)
        return self.genvex_nabto.get_value(self._valueKey)
