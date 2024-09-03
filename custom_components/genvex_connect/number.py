import random

from homeassistant.helpers.entity import Entity
from homeassistant.components.number import NumberDeviceClass, NumberEntity
from genvexnabto import GenvexNabto, GenvexNabto, GenvexNabtoSetpointKey, GenvexNabtoUnits
from .entity import GenvexConnectEntityBase
from homeassistant.const import EntityCategory
from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    genvexNabto: GenvexNabto = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = []
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.BOOST_TIME):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.BOOST_TIME, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.CO2_THRESHOLD):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.CO2_THRESHOLD, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.DEFROST_BREAK_TIME):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.DEFROST_BREAK_TIME, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.DEFROST_MAX_TIME):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.DEFROST_MAX_TIME, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL_LOW_HUMIDITY):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FAN_LEVEL_LOW_HUMIDITY, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL_HIGH_CO2):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FAN_LEVEL_HIGH_CO2, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL_HIGH_HUMIDITY):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FAN_LEVEL_HIGH_HUMIDITY, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL_HIGH_HUMIDITY_TIME):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FAN_LEVEL_HIGH_HUMIDITY_TIME, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL1_SUPPLY_PRESET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FAN_LEVEL1_SUPPLY_PRESET, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL2_SUPPLY_PRESET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FAN_LEVEL2_SUPPLY_PRESET, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL3_SUPPLY_PRESET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FAN_LEVEL3_SUPPLY_PRESET, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL4_SUPPLY_PRESET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FAN_LEVEL4_SUPPLY_PRESET, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL1_EXTRACT_PRESET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FAN_LEVEL1_EXTRACT_PRESET, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL2_EXTRACT_PRESET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FAN_LEVEL2_EXTRACT_PRESET, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL3_EXTRACT_PRESET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FAN_LEVEL3_EXTRACT_PRESET, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.FAN_LEVEL4_EXTRACT_PRESET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FAN_LEVEL4_EXTRACT_PRESET, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.FILTER_REPLACE_INTERVAL):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FILTER_REPLACE_INTERVAL, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.HUMIDITY_LOW_THRESHOLD):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.HUMIDITY_LOW_THRESHOLD, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.PREHEAT_CYCLE_TIME):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.PREHEAT_CYCLE_TIME, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.PREHEAT_PID_D):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.PREHEAT_PID_D, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.PREHEAT_PID_I):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.PREHEAT_PID_I, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.PREHEAT_PID_P):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.PREHEAT_PID_P, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.REHEAT_CYCLE_TIME):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.REHEAT_CYCLE_TIME, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.REHEAT_PID_D):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.REHEAT_PID_D, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.REHEAT_PID_I):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.REHEAT_PID_I, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.REHEAT_PID_P):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.REHEAT_PID_P, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.TEMP_DEFROST_LOW_THRESHOLD):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_DEFROST_LOW_THRESHOLD, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.TEMP_DEFROST_HIGH_THRESHOLD):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_DEFROST_HIGH_THRESHOLD, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.TEMP_BYPASS_OPEN_OFFSET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_BYPASS_OPEN_OFFSET, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.TEMP_COOLING_START_OFFSET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_COOLING_START_OFFSET, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.TEMP_HOTWATER):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_HOTWATER, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.TEMP_HOTWATER_BOOST):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_HOTWATER_BOOST, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.TEMP_REGULATION_DEAD_BAND):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_REGULATION_DEAD_BAND, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.TEMP_REHEAT_OFFSET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_REHEAT_OFFSET, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.TEMP_SUMMER_SUPPLY_MIN):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_SUMMER_SUPPLY_MIN, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.TEMP_SUMMER_SUPPLY_MAX):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_SUMMER_SUPPLY_MAX, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.TEMP_SUPPLY_MAX):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_SUPPLY_MAX, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.TEMP_SUPPLY_MIN):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_SUPPLY_MIN, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.TEMP_TARGET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_TARGET, None))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.TEMP_WINTER_SUPPLY_MAX):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_WINTER_SUPPLY_MAX, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.TEMP_WINTER_SUPPLY_MIN):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_WINTER_SUPPLY_MIN, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.TEMP_WINTER_MODE_THRESHOLD):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.TEMP_WINTER_MODE_THRESHOLD, EntityCategory.CONFIG))
    if genvexNabto.provides_value(GenvexNabtoSetpointKey.VOC_THRESHOLD):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.VOC_THRESHOLD, EntityCategory.CONFIG))

    async_add_entities(new_entities)


class GenvexConnectNumber(GenvexConnectEntityBase, NumberEntity):
    def __init__(self, genvexNabto: GenvexNabto, valueKey: GenvexNabtoSetpointKey, entityCategory: EntityCategory | None):
        super().__init__(genvexNabto, valueKey.value, valueKey)
        self._valueKey = valueKey
        self._attr_native_min_value = genvexNabto.get_setpoint_min_value(valueKey)
        self._attr_native_max_value = genvexNabto.get_setpoint_max_value(valueKey)
        self._attr_native_step = genvexNabto.get_setpoint_step(valueKey)
        self._attr_entity_category = entityCategory

    def set_unit_of_measurement(self, uom: str):
        self._attr_native_unit_of_measurement = self.parse_unit_of_measure(uom)
        self._attr_device_class = self.parse_device_class(uom)

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self.genvex_nabto.set_setpoint(self._valueKey, value)

    def update(self) -> None:
        """Fetch new state data for the number."""
        self._attr_native_value = f"{self.genvex_nabto.get_value(self._valueKey)}"

    def parse_device_class(self, uom:str, default:str=None) -> str:
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
                
