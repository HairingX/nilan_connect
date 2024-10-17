from typing import List
from nilan_proxy import NilanProxy, NilanProxySetpointKey, NilanProxyUnits # type: ignore
from homeassistant.components.number import NumberDeviceClass, NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .data import get_proxy
from .entity import NilanConnectEntityBase


async def async_setup_entry(hass: HomeAssistant, entry:ConfigEntry, async_add_entities:AddEntitiesCallback):
    """Add numbers for passed config_entry in HA."""
    proxy = get_proxy(hass, entry)

    new_entities:List[NumberEntity] = []
    if proxy.provides_value(NilanProxySetpointKey.BOOST_TIME):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.BOOST_TIME, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.CO2_THRESHOLD):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.CO2_THRESHOLD, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.DEFROST_BREAK_TIME):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.DEFROST_BREAK_TIME, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.DEFROST_MAX_TIME):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.DEFROST_MAX_TIME, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.FAN_LEVEL_LOW_HUMIDITY):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.FAN_LEVEL_LOW_HUMIDITY, EntityCategory.CONFIG, default_enabled=True, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.FAN_LEVEL_HIGH_CO2):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.FAN_LEVEL_HIGH_CO2, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.FAN_LEVEL_HIGH_HUMIDITY):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.FAN_LEVEL_HIGH_HUMIDITY, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.FAN_LEVEL_HIGH_HUMIDITY_TIME):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.FAN_LEVEL_HIGH_HUMIDITY_TIME, EntityCategory.CONFIG, default_enabled=True, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.FAN_LEVEL1_SUPPLY_PRESET):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.FAN_LEVEL1_SUPPLY_PRESET, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.FAN_LEVEL2_SUPPLY_PRESET):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.FAN_LEVEL2_SUPPLY_PRESET, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.FAN_LEVEL3_SUPPLY_PRESET):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.FAN_LEVEL3_SUPPLY_PRESET, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.FAN_LEVEL4_SUPPLY_PRESET):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.FAN_LEVEL4_SUPPLY_PRESET, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.FAN_LEVEL1_EXTRACT_PRESET):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.FAN_LEVEL1_EXTRACT_PRESET, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.FAN_LEVEL2_EXTRACT_PRESET):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.FAN_LEVEL2_EXTRACT_PRESET, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.FAN_LEVEL3_EXTRACT_PRESET):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.FAN_LEVEL3_EXTRACT_PRESET, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.FAN_LEVEL4_EXTRACT_PRESET):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.FAN_LEVEL4_EXTRACT_PRESET, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.FILTER_REPLACE_INTERVAL):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.FILTER_REPLACE_INTERVAL, EntityCategory.CONFIG, default_enabled=True, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.HUMIDITY_LOW_THRESHOLD):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.HUMIDITY_LOW_THRESHOLD, EntityCategory.CONFIG, default_enabled=True, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.PREHEAT_CYCLE_TIME):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.PREHEAT_CYCLE_TIME, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.PREHEAT_PID_D):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.PREHEAT_PID_D, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.PREHEAT_PID_I):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.PREHEAT_PID_I, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.PREHEAT_PID_P):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.PREHEAT_PID_P, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.REHEAT_CYCLE_TIME):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.REHEAT_CYCLE_TIME, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.REHEAT_PID_D):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.REHEAT_PID_D, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.REHEAT_PID_I):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.REHEAT_PID_I, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.REHEAT_PID_P):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.REHEAT_PID_P, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.TEMP_DEFROST_LOW_THRESHOLD):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.TEMP_DEFROST_LOW_THRESHOLD, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.TEMP_DEFROST_HIGH_THRESHOLD):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.TEMP_DEFROST_HIGH_THRESHOLD, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.TEMP_BYPASS_OPEN_OFFSET):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.TEMP_BYPASS_OPEN_OFFSET, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.TEMP_COOLING_START_OFFSET):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.TEMP_COOLING_START_OFFSET, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.TEMP_HOTWATER):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.TEMP_HOTWATER, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.TEMP_HOTWATER_BOOST):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.TEMP_HOTWATER_BOOST, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.TEMP_REGULATION_DEAD_BAND):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.TEMP_REGULATION_DEAD_BAND, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.TEMP_REHEAT_OFFSET):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.TEMP_REHEAT_OFFSET, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.TEMP_SUMMER_SUPPLY_MIN):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.TEMP_SUMMER_SUPPLY_MIN, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.TEMP_SUMMER_SUPPLY_MAX):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.TEMP_SUMMER_SUPPLY_MAX, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.TEMP_SUPPLY_MAX):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.TEMP_SUPPLY_MAX, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.TEMP_SUPPLY_MIN):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.TEMP_SUPPLY_MIN, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.TEMP_TARGET):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.TEMP_TARGET, None))
    if proxy.provides_value(NilanProxySetpointKey.TEMP_WINTER_SUPPLY_MAX):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.TEMP_WINTER_SUPPLY_MAX, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.TEMP_WINTER_SUPPLY_MIN):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.TEMP_WINTER_SUPPLY_MIN, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.TEMP_WINTER_MODE_THRESHOLD):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.TEMP_WINTER_MODE_THRESHOLD, EntityCategory.CONFIG, default_enabled=False, default_visible=False))
    if proxy.provides_value(NilanProxySetpointKey.VOC_THRESHOLD):
        new_entities.append(NilanConnectNumber(proxy, NilanProxySetpointKey.VOC_THRESHOLD, EntityCategory.CONFIG, default_enabled=False, default_visible=False))

    async_add_entities(new_entities)


class NilanConnectNumber(NilanConnectEntityBase[NilanProxySetpointKey], NumberEntity): # type: ignore
    def __init__(self, proxy: NilanProxy, valueKey: NilanProxySetpointKey, entityCategory: EntityCategory | None, default_enabled:bool = True, default_visible:bool = True):
        super().__init__(proxy, valueKey.value, valueKey, default_enabled=default_enabled, default_visible=default_visible)
        self._valueKey = valueKey
        min_value = proxy.get_setpoint_min_value(valueKey)
        max_value = proxy.get_setpoint_max_value(valueKey)
        if min_value is not None: self._attr_native_min_value = float(min_value)
        if max_value is not None: self._attr_native_max_value = float(max_value)
        self._attr_native_step = proxy.get_setpoint_step(valueKey)
        self._attr_entity_category = entityCategory

    def set_unit_of_measurement(self, uom: str|None):
        self._attr_native_unit_of_measurement = self.parse_unit_of_measure(uom)
        self._attr_device_class = self.parse_device_class(uom)

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self.proxy.set_setpoint(self._valueKey, value)

    def update(self) -> None:
        """Fetch new state data for the number."""
        self._attr_native_value = self.proxy.get_value(self._valueKey)

    def parse_device_class(self, uom:str|None, default:NumberDeviceClass|None=None) -> NumberDeviceClass|None:
        match uom:
            case NilanProxyUnits.SECONDS:     return NumberDeviceClass.DURATION
            case NilanProxyUnits.MINUTES:     return NumberDeviceClass.DURATION
            case NilanProxyUnits.HOURS:     return NumberDeviceClass.DURATION
            case NilanProxyUnits.DAYS:     return NumberDeviceClass.DURATION
            case NilanProxyUnits.MONTHS:   return NumberDeviceClass.DURATION
            case NilanProxyUnits.YEARS:    return NumberDeviceClass.DURATION
            case NilanProxyUnits.CELSIUS:  return NumberDeviceClass.TEMPERATURE
            case NilanProxyUnits.PCT:      return NumberDeviceClass.POWER_FACTOR
            case NilanProxyUnits.PPM:      return NumberDeviceClass.CO2
            case _:
                return default
                
