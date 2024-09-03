"""Platform for switch integration."""

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from genvexnabto import GenvexNabto, GenvexNabto, GenvexNabtoSetpointKey
from .entity import GenvexConnectEntityBase

from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    genvexNabto: GenvexNabto = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = []
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.BOOST_ENABLE):
        new_entities.append(GenvexConnectSwitch(genvexNabto, GenvexNabtoSetpointKey.BOOST_ENABLE, "mdi:fan-chevron-up"))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.COOLING_ENABLE):
        new_entities.append(GenvexConnectSwitch(genvexNabto, GenvexNabtoSetpointKey.COOLING_ENABLE, "mdi:coolant-temperature"))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.ENABLE):
        new_entities.append(GenvexConnectSwitch(genvexNabto, GenvexNabtoSetpointKey.ENABLE, "mdi:power"))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.HUMIDITY_CONTROL_ENABLE):
        new_entities.append(GenvexConnectSwitch(genvexNabto, GenvexNabtoSetpointKey.HUMIDITY_CONTROL_ENABLE, "mdi:water-circle"))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.PREHEAT_ENABLE):
        new_entities.append(GenvexConnectSwitch(genvexNabto, GenvexNabtoSetpointKey.PREHEAT_ENABLE, "mdi:heating-coil"))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.REHEAT_ENABLE):
        new_entities.append(GenvexConnectSwitch(genvexNabto, GenvexNabtoSetpointKey.REHEAT_ENABLE, "mdi:heating-coil"))

    async_add_entities(new_entities)


class GenvexConnectSwitch(GenvexConnectEntityBase, SwitchEntity):
    def __init__(self, genvexNabto: GenvexNabto, valueKey: GenvexNabtoSetpointKey, icon:str):
        super().__init__(genvexNabto, valueKey.value, valueKey)
        self._valueKey = valueKey
        self._attr_device_class = SwitchDeviceClass.SWITCH
        self._attr_icon = icon

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the entity on."""
        self.genvex_nabto.set_setpoint(self._valueKey, 1)

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the entity on."""
        self.genvex_nabto.set_setpoint(self._valueKey, 0)

    @property
    def is_on(self) -> bool|None:
        """Fetch new state data for the switch."""
        return int(self.genvex_nabto.get_value(self._valueKey)) == 1
