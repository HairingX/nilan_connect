"""Platform for Binary Sensor integration."""

import random

from homeassistant.helpers.entity import Entity
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from genvexnabto import GenvexNabto, GenvexNabto, GenvexNabtoDatapointKey
from .entity import GenvexConnectEntityBase

from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    genvexNabto: GenvexNabto = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = []
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.BYPASS_ACTIVE):
        new_entities.append(
            GenvexConnectBinarySensor(
                genvexNabto,
                GenvexNabtoDatapointKey.BYPASS_ACTIVE,
                "mdi:valve",
                type=BinarySensorDeviceClass.OPENING,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.DEFROST_ACTIVE):
        new_entities.append(
            GenvexConnectBinarySensor(
                genvexNabto,
                GenvexNabtoDatapointKey.DEFROST_ACTIVE,
                "mdi:snowflake-melt",
                type=BinarySensorDeviceClass.RUNNING,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.WINTER_MODE_ACTIVE):
        new_entities.append(
            GenvexConnectBinarySensor(
                genvexNabto,
                GenvexNabtoDatapointKey.WINTER_MODE_ACTIVE,
                "mdi:sun-snowflake-variant",
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.SACRIFICIAL_ANODE_OK):
        new_entities.append(
            GenvexConnectBinarySensor(
                genvexNabto,
                GenvexNabtoDatapointKey.SACRIFICIAL_ANODE_OK,
                "mdi:water-opacity",
                type=BinarySensorDeviceClass.PROBLEM,
                inverted=True,
            )
        )

    async_add_entities(new_entities)


class GenvexConnectBinarySensor(GenvexConnectEntityBase, BinarySensorEntity):
    def __init__(self, genvexNabto: GenvexNabto, valueKey, icon, type=None, inverted=False):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._valueKey = valueKey
        self._icon = icon
        self._attr_device_class = type
        self._attr_icon = icon
        self._inverted = inverted

    @property
    def is_on(self) -> None:
        """Fetch new state data for the sensor."""
        if self._inverted:
            return not self.genvexNabto.getValue(self._valueKey)
        return self.genvexNabto.getValue(self._valueKey)
