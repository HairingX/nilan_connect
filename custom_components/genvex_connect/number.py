import random

from homeassistant.helpers.entity import Entity
from homeassistant.components.number import NumberDeviceClass, NumberEntity
from genvexnabto import GenvexNabto, GenvexNabto, GenvexNabtoSetpointKey
from .entity import GenvexConnectEntityBase
from homeassistant.const import EntityCategory, UnitOfTemperature, PERCENTAGE, UnitOfTime
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    genvexNabto: GenvexNabto = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = []
    # Fan speed presets
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FAN_LEVEL1_SUPPLY_PRESET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FAN_LEVEL1_SUPPLY_PRESET, NumberDeviceClass.POWER_FACTOR, PERCENTAGE, EntityCategory.CONFIG))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FAN_LEVEL2_SUPPLY_PRESET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FAN_LEVEL2_SUPPLY_PRESET, NumberDeviceClass.POWER_FACTOR, PERCENTAGE, EntityCategory.CONFIG))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FAN_LEVEL3_SUPPLY_PRESET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FAN_LEVEL3_SUPPLY_PRESET, NumberDeviceClass.POWER_FACTOR, PERCENTAGE, EntityCategory.CONFIG))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FAN_LEVEL4_SUPPLY_PRESET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FAN_LEVEL4_SUPPLY_PRESET, NumberDeviceClass.POWER_FACTOR, PERCENTAGE, EntityCategory.CONFIG))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FAN_LEVEL1_EXTRACT_PRESET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FAN_LEVEL1_EXTRACT_PRESET, NumberDeviceClass.POWER_FACTOR, PERCENTAGE, EntityCategory.CONFIG))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FAN_LEVEL2_EXTRACT_PRESET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FAN_LEVEL2_EXTRACT_PRESET, NumberDeviceClass.POWER_FACTOR, PERCENTAGE, EntityCategory.CONFIG))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FAN_LEVEL3_EXTRACT_PRESET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FAN_LEVEL3_EXTRACT_PRESET, NumberDeviceClass.POWER_FACTOR, PERCENTAGE, EntityCategory.CONFIG))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FAN_LEVEL4_EXTRACT_PRESET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FAN_LEVEL4_EXTRACT_PRESET, NumberDeviceClass.POWER_FACTOR, PERCENTAGE, EntityCategory.CONFIG))
    # Boost time
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.BOOST_TIME_MINUTES):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.BOOST_TIME_MINUTES, NumberDeviceClass.DURATION, UnitOfTime.MINUTES, EntityCategory.CONFIG))
    # Filter
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FILTER_REPLACE_INTERVAL_DAYS):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FILTER_REPLACE_INTERVAL_DAYS, NumberDeviceClass.DURATION, UnitOfTime.DAYS, EntityCategory.CONFIG))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FILTER_REPLACE_INTERVAL_MONTHS):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FILTER_REPLACE_INTERVAL_MONTHS, NumberDeviceClass.DURATION, UnitOfTime.MONTHS, EntityCategory.CONFIG))
    # Temperature    
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.TEMP_BYPASS_OPEN_OFFSET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_BYPASS_OPEN_OFFSET, NumberDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS, EntityCategory.CONFIG))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.TEMP_COOLING_START_OFFSET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_COOLING_START_OFFSET, NumberDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS, EntityCategory.CONFIG))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.TEMP_HOTWATER):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_HOTWATER, NumberDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS, EntityCategory.CONFIG))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.TEMP_HOTWATER_BOOST):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_HOTWATER_BOOST, NumberDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS, EntityCategory.CONFIG))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.TEMP_SUMMER_SUPPLY_MIN):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_SUMMER_SUPPLY_MIN, NumberDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS, EntityCategory.CONFIG))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.TEMP_SUMMER_SUPPLY_MAX):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_SUMMER_SUPPLY_MAX, NumberDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS, EntityCategory.CONFIG))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.TEMP_TARGET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_TARGET, NumberDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS, None))
   
    async_add_entities(new_entities)


class GenvexConnectNumber(GenvexConnectEntityBase, NumberEntity):
    def __init__(self, genvexNabto:GenvexNabto, valueKey:str, deviceClass:NumberDeviceClass, uom:str|None, entityCategory:EntityCategory|None):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._valueKey = valueKey
        self._attr_device_class = deviceClass
        self._attr_native_min_value = genvexNabto.getSetpointMinValue(valueKey)
        self._attr_native_max_value = genvexNabto.getSetpointMaxValue(valueKey)
        self._attr_native_step = genvexNabto.getSetpointStep(valueKey)
        self._attr_entity_category = entityCategory
        self._attr_unit_of_measurement = uom

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self.genvexNabto.setSetpoint(self._valueKey, value)

    def update(self) -> None:
        """Fetch new state data for the number."""
        self._attr_native_value = f"{self.genvexNabto.getValue(self._valueKey)}"