from typing import List
from genvexnabto import GenvexNabto, GenvexNabtoSetpointKey, GenvexNabtoUnits # type: ignore
from homeassistant.components.number import NumberDeviceClass, NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .data import getHassData
from .entity import GenvexConnectEntityBase


async def async_setup_entry(hass: HomeAssistant, entry:ConfigEntry, async_add_entities:AddEntitiesCallback):
    """Add numbers for passed config_entry in HA."""
    data = getHassData(hass, entry)
    genvex_nabto = data["genvex_nabto"]

    new_entities:List[NumberEntity] = []
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.BOOST_TIME):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.BOOST_TIME, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.CO2_THRESHOLD):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.CO2_THRESHOLD, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.DEFROST_BREAK_TIME):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.DEFROST_BREAK_TIME, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.DEFROST_MAX_TIME):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.DEFROST_MAX_TIME, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL_LOW_HUMIDITY):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.FAN_LEVEL_LOW_HUMIDITY, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL_HIGH_CO2):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.FAN_LEVEL_HIGH_CO2, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL_HIGH_HUMIDITY):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.FAN_LEVEL_HIGH_HUMIDITY, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL_HIGH_HUMIDITY_TIME):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.FAN_LEVEL_HIGH_HUMIDITY_TIME, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL1_SUPPLY_PRESET):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.FAN_LEVEL1_SUPPLY_PRESET, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL2_SUPPLY_PRESET):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.FAN_LEVEL2_SUPPLY_PRESET, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL3_SUPPLY_PRESET):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.FAN_LEVEL3_SUPPLY_PRESET, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL4_SUPPLY_PRESET):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.FAN_LEVEL4_SUPPLY_PRESET, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL1_EXTRACT_PRESET):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.FAN_LEVEL1_EXTRACT_PRESET, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL2_EXTRACT_PRESET):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.FAN_LEVEL2_EXTRACT_PRESET, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL3_EXTRACT_PRESET):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.FAN_LEVEL3_EXTRACT_PRESET, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL4_EXTRACT_PRESET):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.FAN_LEVEL4_EXTRACT_PRESET, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.FILTER_REPLACE_INTERVAL):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.FILTER_REPLACE_INTERVAL, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.HUMIDITY_LOW_THRESHOLD):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.HUMIDITY_LOW_THRESHOLD, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.PREHEAT_CYCLE_TIME):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.PREHEAT_CYCLE_TIME, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.PREHEAT_PID_D):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.PREHEAT_PID_D, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.PREHEAT_PID_I):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.PREHEAT_PID_I, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.PREHEAT_PID_P):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.PREHEAT_PID_P, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.REHEAT_CYCLE_TIME):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.REHEAT_CYCLE_TIME, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.REHEAT_PID_D):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.REHEAT_PID_D, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.REHEAT_PID_I):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.REHEAT_PID_I, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.REHEAT_PID_P):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.REHEAT_PID_P, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.TEMP_DEFROST_LOW_THRESHOLD):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.TEMP_DEFROST_LOW_THRESHOLD, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.TEMP_DEFROST_HIGH_THRESHOLD):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.TEMP_DEFROST_HIGH_THRESHOLD, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.TEMP_BYPASS_OPEN_OFFSET):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.TEMP_BYPASS_OPEN_OFFSET, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.TEMP_COOLING_START_OFFSET):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.TEMP_COOLING_START_OFFSET, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.TEMP_HOTWATER):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.TEMP_HOTWATER, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.TEMP_HOTWATER_BOOST):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.TEMP_HOTWATER_BOOST, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.TEMP_REGULATION_DEAD_BAND):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.TEMP_REGULATION_DEAD_BAND, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.TEMP_REHEAT_OFFSET):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.TEMP_REHEAT_OFFSET, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.TEMP_SUMMER_SUPPLY_MIN):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.TEMP_SUMMER_SUPPLY_MIN, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.TEMP_SUMMER_SUPPLY_MAX):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.TEMP_SUMMER_SUPPLY_MAX, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.TEMP_SUPPLY_MAX):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.TEMP_SUPPLY_MAX, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.TEMP_SUPPLY_MIN):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.TEMP_SUPPLY_MIN, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.TEMP_TARGET):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.TEMP_TARGET, None))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.TEMP_WINTER_SUPPLY_MAX):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.TEMP_WINTER_SUPPLY_MAX, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.TEMP_WINTER_SUPPLY_MIN):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.TEMP_WINTER_SUPPLY_MIN, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.TEMP_WINTER_MODE_THRESHOLD):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.TEMP_WINTER_MODE_THRESHOLD, EntityCategory.CONFIG))
    if genvex_nabto.provides_value(GenvexNabtoSetpointKey.VOC_THRESHOLD):
        new_entities.append(GenvexConnectNumber(genvex_nabto, GenvexNabtoSetpointKey.VOC_THRESHOLD, EntityCategory.CONFIG))

    async_add_entities(new_entities)


class GenvexConnectNumber(GenvexConnectEntityBase[GenvexNabtoSetpointKey], NumberEntity): # type: ignore
    def __init__(self, genvex_nabto: GenvexNabto, valueKey: GenvexNabtoSetpointKey, entityCategory: EntityCategory | None):
        super().__init__(genvex_nabto, valueKey.value, valueKey)
        self._valueKey = valueKey
        min_value = genvex_nabto.get_setpoint_min_value(valueKey)
        max_value = genvex_nabto.get_setpoint_max_value(valueKey)
        if min_value is not None: self._attr_native_min_value = float(min_value)
        if max_value is not None: self._attr_native_max_value = float(max_value)
        self._attr_native_step = genvex_nabto.get_setpoint_step(valueKey)
        self._attr_entity_category = entityCategory

    def set_unit_of_measurement(self, uom: str|None):
        self._attr_native_unit_of_measurement = self.parse_unit_of_measure(uom)
        self._attr_device_class = self.parse_device_class(uom)

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self.genvex_nabto.set_setpoint(self._valueKey, value)

    def update(self) -> None:
        """Fetch new state data for the number."""
        self._attr_native_value = self.genvex_nabto.get_value(self._valueKey)

    def parse_device_class(self, uom:str|None, default:NumberDeviceClass|None=None) -> NumberDeviceClass|None:
        match uom:
            case GenvexNabtoUnits.SECONDS:     return NumberDeviceClass.DURATION
            case GenvexNabtoUnits.MINUTES:     return NumberDeviceClass.DURATION
            case GenvexNabtoUnits.HOURS:     return NumberDeviceClass.DURATION
            case GenvexNabtoUnits.DAYS:     return NumberDeviceClass.DURATION
            case GenvexNabtoUnits.MONTHS:   return NumberDeviceClass.DURATION
            case GenvexNabtoUnits.YEARS:    return NumberDeviceClass.DURATION
            case GenvexNabtoUnits.CELSIUS:  return NumberDeviceClass.TEMPERATURE
            case GenvexNabtoUnits.PCT:      return NumberDeviceClass.POWER_FACTOR
            case GenvexNabtoUnits.PPM:      return NumberDeviceClass.CO2
            case _:
                return default
                
