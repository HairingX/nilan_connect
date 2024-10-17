"""Platform for sensor integration."""

from typing import List
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor.const import SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from nilan_proxy import NilanProxy, NilanProxyDatapointKey, NilanProxySetpointKey # type: ignore
from .data import get_proxy
from .entity import NilanConnectEntityBase


async def async_setup_entry(hass: HomeAssistant, entry:ConfigEntry, async_add_entities:AddEntitiesCallback):
    """Add sensors for passed config_entry in HA."""
    proxy = get_proxy(hass, entry)

    new_entities:List[SensorEntity] = []
    
    if proxy.provides_value(NilanProxyDatapointKey.ALARM_1_CODE):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.ALARM_1_CODE, icon="mdi:alarm-light", default_enabled=False))
    if proxy.provides_value(NilanProxyDatapointKey.ALARM_1_INFO):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.ALARM_1_INFO, icon="mdi:alarm-light", default_enabled=False))
    if proxy.provides_value(NilanProxyDatapointKey.ALARM_2_CODE):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.ALARM_2_CODE, icon="mdi:alarm-light", default_enabled=False))
    if proxy.provides_value(NilanProxyDatapointKey.ALARM_2_INFO):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.ALARM_2_INFO, icon="mdi:alarm-light", default_enabled=False))
    if proxy.provides_value(NilanProxyDatapointKey.ALARM_3_CODE):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.ALARM_3_CODE, icon="mdi:alarm-light", default_enabled=False))
    if proxy.provides_value(NilanProxyDatapointKey.ALARM_3_INFO):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.ALARM_3_INFO, icon="mdi:alarm-light", default_enabled=False))
    if proxy.provides_value(NilanProxyDatapointKey.ALARM_BITS):
        new_entities.append(NilanConnectSensorAlarmOptima270(proxy, NilanProxyDatapointKey.ALARM_BITS))
    if proxy.provides_value(NilanProxyDatapointKey.CO2_LEVEL):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.CO2_LEVEL, device_class=SensorDeviceClass.CO2))
    if proxy.provides_value(NilanProxyDatapointKey.DEFROST_TIME_AGO):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.DEFROST_TIME_AGO, icon="mdi:snowflake-melt"))
    if proxy.provides_value(NilanProxyDatapointKey.FAN_DUTYCYCLE_EXTRACT):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.FAN_DUTYCYCLE_EXTRACT, icon="mdi:fan"))
    if proxy.provides_value(NilanProxyDatapointKey.FAN_DUTYCYCLE_SUPPLY):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.FAN_DUTYCYCLE_SUPPLY, icon="mdi:fan"))
    if proxy.provides_value(NilanProxyDatapointKey.FAN_LEVEL_CURRENT):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.FAN_LEVEL_CURRENT, icon="mdi:fan"))
    if proxy.provides_value(NilanProxyDatapointKey.FAN_LEVEL_EXTRACT):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.FAN_LEVEL_EXTRACT, icon="mdi:fan")) 
    if proxy.provides_value(NilanProxyDatapointKey.FAN_LEVEL_SUPPLY):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.FAN_LEVEL_SUPPLY, icon="mdi:fan"))
    if proxy.provides_value(NilanProxyDatapointKey.FAN_RPM_EXTRACT):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.FAN_RPM_EXTRACT, icon="mdi:fan", precision=0))
    if proxy.provides_value(NilanProxyDatapointKey.FAN_RPM_SUPPLY):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.FAN_RPM_SUPPLY, icon="mdi:fan", precision=0))
    if proxy.provides_value(NilanProxyDatapointKey.FILTER_REPLACE_TIME_AGO):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.FILTER_REPLACE_TIME_AGO, icon="mdi:air-filter"))
    if proxy.provides_value(NilanProxyDatapointKey.FILTER_REPLACE_TIME_REMAIN):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.FILTER_REPLACE_TIME_REMAIN, icon="mdi:air-filter"))
    if proxy.provides_value(NilanProxyDatapointKey.HUMIDITY):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.HUMIDITY, icon="mdi:water-percent", device_class=SensorDeviceClass.HUMIDITY))
    if proxy.provides_value(NilanProxyDatapointKey.HUMIDITY_AVG):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.HUMIDITY_AVG, icon="mdi:water-percent", device_class=SensorDeviceClass.HUMIDITY))
    if proxy.provides_value(NilanProxyDatapointKey.HUMIDITY_HIGH_LEVEL):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.HUMIDITY_HIGH_LEVEL, icon="mdi:water-percent"))
    if proxy.provides_value(NilanProxyDatapointKey.HUMIDITY_HIGH_LEVEL_TIME):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.HUMIDITY_HIGH_LEVEL_TIME, icon="mdi:water-percent"))
    if proxy.provides_value(NilanProxyDatapointKey.STATE_CODE):
        new_entities.append(NilanConnectSensorControlState602(proxy, NilanProxyDatapointKey.STATE_CODE))
    if proxy.provides_value(NilanProxyDatapointKey.TEMP_CONDENSER):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.TEMP_CONDENSER, device_class=SensorDeviceClass.TEMPERATURE))
    if proxy.provides_value(NilanProxyDatapointKey.TEMP_EVAPORATOR):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.TEMP_EVAPORATOR, device_class=SensorDeviceClass.TEMPERATURE))
    if proxy.provides_value(NilanProxyDatapointKey.TEMP_EXHAUST):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.TEMP_EXHAUST, device_class=SensorDeviceClass.TEMPERATURE))
    if proxy.provides_value(NilanProxyDatapointKey.TEMP_EXTRACT):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.TEMP_EXTRACT, device_class=SensorDeviceClass.TEMPERATURE))
    if proxy.provides_value(NilanProxyDatapointKey.TEMP_HOTWATER_BOTTOM):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.TEMP_HOTWATER_BOTTOM, device_class=SensorDeviceClass.TEMPERATURE))
    if proxy.provides_value(NilanProxyDatapointKey.TEMP_HOTWATER_TOP):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.TEMP_HOTWATER_TOP, device_class=SensorDeviceClass.TEMPERATURE))
    if proxy.provides_value(NilanProxyDatapointKey.TEMP_OUTSIDE):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.TEMP_OUTSIDE, device_class=SensorDeviceClass.TEMPERATURE))
    if proxy.provides_value(NilanProxyDatapointKey.TEMP_ROOM):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.TEMP_ROOM, device_class=SensorDeviceClass.TEMPERATURE))
    if proxy.provides_value(NilanProxyDatapointKey.TEMP_SUPPLY):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.TEMP_SUPPLY, device_class=SensorDeviceClass.TEMPERATURE))
    if proxy.provides_value(NilanProxyDatapointKey.VOC_LEVEL):
        new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.VOC_LEVEL, device_class=SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS_PARTS))
        
        
    # if proxy.provides_value(NilanProxyDatapointKey.UNKNOWN_VALUE_1):
    #     new_entities.append(NilanConnectSensor(proxy, NilanProxyDatapointKey.UNKNOWN_VALUE_1))

    # if proxy.provides_value(NilanProxyDatapointKey.ALARM_1_CODE):
    #     alarmHandler = NilanConnectCTS400AlarmHandler(proxy)
    #     new_entities.append(NilanConnectSensorCTS400AlarmList(proxy, alarmHandler))
    #     new_entities.append(NilanConnectSensorCTS400AlarmCount(proxy, alarmHandler))
    #     # Trigger the alarm handler to react on the starting state
    #     alarmHandler.on_change(0, 0)
        
        
    if (
        proxy.provides_value(NilanProxyDatapointKey.TEMP_SUPPLY)
        and proxy.provides_value(NilanProxyDatapointKey.TEMP_EXTRACT)
        and proxy.provides_value(NilanProxyDatapointKey.TEMP_OUTSIDE)
    ):
        new_entities.append(NilanConnectSensorEfficiency(proxy))
    
    async_add_entities(new_entities)


class NilanConnectSensor(NilanConnectEntityBase[NilanProxyDatapointKey], SensorEntity): # type: ignore
    def __init__(self, 
                 proxy: NilanProxy, 
                 valueKey: NilanProxyDatapointKey, 
                 name: str|None = None, 
                 useDefaultUpdateHandler: bool = True, 
                 icon:str|None = None, 
                 device_class:SensorDeviceClass|None = None, 
                 default_enabled:bool = True, 
                 default_visible:bool = True,
                 precision: int|None = None):
        super().__init__(proxy, name if name is not None else valueKey.value, valueKey, useDefaultUpdateHandler, default_enabled, default_visible)
        self._attr_state_class = SensorStateClass.MEASUREMENT
        if icon is not None: self._attr_icon = icon
        if device_class is not None: self._attr_device_class = device_class
        if precision is not None: self._attr_suggested_display_precision = precision
        
    def set_unit_of_measurement(self, uom: str|None):
        self._attr_native_unit_of_measurement = self.parse_unit_of_measure(uom)

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = self.proxy.get_value(self._value_key)
        if self._attr_native_value is float:
            self._attr_native_value = round(self._attr_native_value, 2)

class NilanConnectSensorEfficiency(NilanConnectEntityBase[None], SensorEntity): # type: ignore
    def __init__(self, proxy:NilanProxy):
        super().__init__(proxy, "efficiency", None, False)
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_device_class = SensorDeviceClass.POWER_FACTOR
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_suggested_display_precision = 1
        self._attr_icon = "mdi:variable"
        self._attr_should_poll = True # true since wait for HA to poll, we do not subscribe
        
    # async def async_added_to_hass(self) -> None:
    #     self.proxy.register_update_handler(NilanProxyDatapointKey.TEMP_SUPPLY, self._on_change)
    #     self.proxy.register_update_handler(NilanProxyDatapointKey.TEMP_OUTSIDE, self._on_change)
    #     self.proxy.register_update_handler(NilanProxyDatapointKey.TEMP_EXTRACT, self._on_change)
    
    # async def async_will_remove_from_hass(self) -> None:
    #     self.proxy.deregister_update_handler(NilanProxyDatapointKey.TEMP_SUPPLY, self._on_change)
    #     self.proxy.deregister_update_handler(NilanProxyDatapointKey.TEMP_OUTSIDE, self._on_change)
    #     self.proxy.deregister_update_handler(NilanProxyDatapointKey.TEMP_EXTRACT, self._on_change)

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        supply = self.proxy.get_value(NilanProxyDatapointKey.TEMP_SUPPLY)
        outside = self.proxy.get_value(NilanProxyDatapointKey.TEMP_OUTSIDE)
        extract = self.proxy.get_value(NilanProxyDatapointKey.TEMP_EXTRACT)
        
        if supply is None or outside is None or extract is None:
            return
        
        if extract - outside == 0:
            return

        self._attr_native_value = ((supply - outside) / (extract - outside)) * 100


class NilanConnectSensorControlState602(NilanConnectSensor):
    def __init__(self, proxy: NilanProxy, valueKey:NilanProxyDatapointKey):
        super().__init__(proxy, valueKey, "cts602_state")
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = [
            "state_0",
            "state_1",
            "state_2",
            "state_3",
            "state_4",
            "state_5",
            "state_6",
            "state_7",
            "state_8",
            "state_9",
            "state_10",
            "state_11",
            "state_12",
            "state_13",
            "state_14",
            "state_15",
            "state_16",
            "state_17",
        ]
        self._attr_native_value = "state_0"

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = f"state_{int(self.proxy.get_value(self._value_key) or 0)}"


class NilanConnectSensorAlarmOptima270(NilanConnectSensor):
    def __init__(self, proxy: NilanProxy, valueKey:NilanProxyDatapointKey):
        super().__init__(proxy, valueKey, "optima270_alarms")
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_icon = "mdi:alarm-bell"
        self._attr_options = [
            "state_0",
            "state_2",
            "state_4",
            "state_8",
            "state_16",
            "state_32",
            "state_64",
            "state_128",
            "state_256",
            "state_512",
            "state_1024",
            "state_2048",
            "state_4096",
            "state_8192",
            "state_16384",
            "state_32768",
            "state_65536",
            "state_131072",
            "state_262144",
            "state_524288",
            "state_1048576",
            "state_2097152",
            "state_4194304",
            "state_8388608",
        ]
        self._attr_native_value = "state_0"

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = f"state_{int(self.proxy.get_value(self._value_key) or 0)}"


# class NilanConnectCTS400AlarmHandler:
#     active_alarms:List[int] = []
#     update_handlers:List[Callable[[int, int], None]] = []
    
#     def __init__(self, proxy: NilanProxy) -> None:
#         self.proxy = proxy
#         self.update_handlers = []
#         proxy.register_update_handler(NilanProxyDatapointKey.ALARM_1_CODE, self.on_change)
#         proxy.register_update_handler(NilanProxyDatapointKey.ALARM_2_CODE, self.on_change)
#         proxy.register_update_handler(NilanProxyDatapointKey.ALARM_3_CODE, self.on_change)
#         proxy.register_update_handler(NilanProxyDatapointKey.FILTER_OK, self.on_change)

#     def on_change(self, _old_value:float|int, _new_value:float|int):
#         # Recalculate the active alarms
#         critical_errors = int(self.proxy.get_value(NilanProxyDatapointKey.ALARM_1_CODE) or 0)
#         warning_errors = int(self.proxy.get_value(NilanProxyDatapointKey.ALARM_2_CODE) or 0)
#         info_errors = int(self.proxy.get_value(NilanProxyDatapointKey.ALARM_3_CODE) or 0)
#         filter_change = self.proxy.get_value(NilanProxyDatapointKey.FILTER_OK) == 0

#         self.active_alarms = []
#         for i in range(0, 16):
#             if i & critical_errors:
#                 self.active_alarms.append(i + 48)
#             critical_errors >>= 1
#         for i in range(0, 16):
#             if i & warning_errors:
#                 self.active_alarms.append(i + 16)
#             warning_errors >>= 1
#         for i in range(0, 16):
#             if i & info_errors:
#                 self.active_alarms.append(i)
#             info_errors >>= 1

#         # filter alarm is not always active, sometimes only the filterOK is 
#         if filter_change and 1 not in self.active_alarms:
#             self.active_alarms.append(1)
            
#         # Trigger an update of any sensors listening on this handler.
#         for update_method in self.update_handlers:
#             update_method(0, 0)

#     def get_active_alarm_count(self):
#         return len(self.active_alarms)

#     def get_active_alarms(self):
#         return self.active_alarms

#     def add_update_handler(self, update_method: Callable[[int, int], None]):
#         self.update_handlers.append(update_method)


# # This sensor is more complex than the others, due to using the values of 3 datapoints.
# class NilanConnectSensorCTS400AlarmList(NilanConnectEntityBase[None], SensorEntity): # type: ignore
#     def __init__(self, proxy: NilanProxy, alarmHandler: NilanConnectCTS400AlarmHandler):
#         super().__init__(proxy, "alarmlist", None, False)
#         self._attr_state_class = None
#         self._attr_icon = "mdi:alarm-light"
#         self._alarmHandler = alarmHandler
#         self._alarmHandler.add_update_handler(self._on_change)
#         self._alarmTextValues = {
#             1: "Filterchange",
#             15: "De-icing (timeout)",
#             16: "T1 disconnected",
#             17: "T1 short-circuited",
#             18: "T2 disconnected",
#             19: "T2 short-circuited",
#             20: "T3 disconnected",
#             21: "T3 short-circuited",
#             22: "T4 disconnected",
#             23: "T4 short-circuited",
#             24: "T7 disconnected",
#             25: "T7 short-circuited",
#             26: "Failure humidity sensor",
#             27: "Failure CO2 sensor",
#             28: "Failure thermostat afterheating",
#             29: "Frost risk afterheating",
#             48: "Firedamper",
#             49: "Fire",
#             50: "Frost afterheating",
#             51: "Low room temperature",
#             52: "Emergency stop",
#         }

#     def translateKey(self, key:int) -> str:
#         if key in self._alarmTextValues:
#             return self._alarmTextValues[key]
#         return "Unknown alarm"

#     def update(self) -> None:
#         """Fetch new state data for the sensor."""
#         if self._alarmHandler.get_active_alarm_count() == 0:
#             self._attr_native_value = "No Alarm"
#             return
#         # Join the string representation of the active alarms
#         self._attr_native_value = ", ".join(map(lambda x: self.translateKey(x), self._alarmHandler.get_active_alarms()))


# # This sensor is more complex than the others, due to using the values of 3 datapoints.
# class NilanConnectSensorCTS400AlarmCount(NilanConnectEntityBase[None], SensorEntity): # type: ignore
#     def __init__(self, proxy: NilanProxy, alarmHandler: NilanConnectCTS400AlarmHandler):
#         super().__init__(proxy, "alarmcount", None, False)
#         self._attr_state_class = None
#         self._attr_icon = "mdi:alarm-light"
#         self._alarmHandler = alarmHandler
#         self._alarmHandler.add_update_handler(self._on_change)

#     def update(self) -> None:
#         """Fetch new state data for the sensor."""
#         self._attr_native_value = self._alarmHandler.get_active_alarm_count()
