"""Platform for sensor integration."""

from typing import Callable, List
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor.const import SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from genvexnabto import GenvexNabto, GenvexNabtoDatapointKey, GenvexNabtoSetpointKey # type: ignore
from .data import getGenvexNabto
from .entity import GenvexConnectEntityBase


async def async_setup_entry(hass: HomeAssistant, entry:ConfigEntry, async_add_entities:AddEntitiesCallback):
    """Add sensors for passed config_entry in HA."""
    genvex_nabto = getGenvexNabto(hass, entry)

    new_entities:List[SensorEntity] = []
    
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.ALARM_1_CODE):
        new_entities.append(GenvexConnectSensorMisc(genvex_nabto, GenvexNabtoDatapointKey.ALARM_1_CODE, "mdi:alarm-light"))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.ALARM_1_INFO):
        new_entities.append(GenvexConnectSensorMisc(genvex_nabto, GenvexNabtoDatapointKey.ALARM_1_INFO, "mdi:alarm-light"))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.ALARM_2_CODE):
        new_entities.append(GenvexConnectSensorMisc(genvex_nabto, GenvexNabtoDatapointKey.ALARM_2_CODE, "mdi:alarm-light"))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.ALARM_2_INFO):
        new_entities.append(GenvexConnectSensorMisc(genvex_nabto, GenvexNabtoDatapointKey.ALARM_2_INFO, "mdi:alarm-light"))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.ALARM_3_CODE):
        new_entities.append(GenvexConnectSensorMisc(genvex_nabto, GenvexNabtoDatapointKey.ALARM_3_CODE, "mdi:alarm-light"))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.ALARM_3_INFO):
        new_entities.append(GenvexConnectSensorMisc(genvex_nabto, GenvexNabtoDatapointKey.ALARM_3_INFO, "mdi:alarm-light"))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.ALARM_BITS):
        new_entities.append(GenvexConnectSensorAlarmOptima270(genvex_nabto, GenvexNabtoDatapointKey.ALARM_BITS))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.CO2_LEVEL):
        new_entities.append(GenvexConnectSensorCO2(genvex_nabto, GenvexNabtoDatapointKey.CO2_LEVEL))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.DEFROST_TIME_AGO):
        new_entities.append(GenvexConnectSensorFilterDays(genvex_nabto, GenvexNabtoDatapointKey.DEFROST_TIME_AGO, icon="mdi:snowflake-melt"))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.FAN_DUTYCYCLE_EXTRACT):
        new_entities.append(GenvexConnectSensorPercentage(genvex_nabto, GenvexNabtoDatapointKey.FAN_DUTYCYCLE_EXTRACT, "mdi:fan"))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.FAN_DUTYCYCLE_SUPPLY):
        new_entities.append(GenvexConnectSensorPercentage(genvex_nabto, GenvexNabtoDatapointKey.FAN_DUTYCYCLE_SUPPLY, "mdi:fan"))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.FAN_LEVEL_CURRENT):
        new_entities.append(GenvexConnectSensorMisc(genvex_nabto, GenvexNabtoDatapointKey.FAN_LEVEL_CURRENT, "mdi:fan"))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.FAN_LEVEL_EXTRACT):
        new_entities.append(GenvexConnectSensorMisc(genvex_nabto, GenvexNabtoDatapointKey.FAN_LEVEL_EXTRACT, "mdi:fan")) 
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.FAN_LEVEL_SUPPLY):
        new_entities.append(GenvexConnectSensorMisc(genvex_nabto, GenvexNabtoDatapointKey.FAN_LEVEL_SUPPLY, "mdi:fan"))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.FAN_RPM_EXTRACT):
        new_entities.append(GenvexConnectSensorFanRPM(genvex_nabto, GenvexNabtoDatapointKey.FAN_RPM_EXTRACT))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.FAN_RPM_SUPPLY):
        new_entities.append(GenvexConnectSensorFanRPM(genvex_nabto, GenvexNabtoDatapointKey.FAN_RPM_SUPPLY))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.FILTER_REPLACE_TIME_AGO):
        new_entities.append(GenvexConnectSensorFilterDays(genvex_nabto, GenvexNabtoDatapointKey.FILTER_REPLACE_TIME_AGO))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.FILTER_REPLACE_TIME_REMAIN):
        new_entities.append(GenvexConnectSensorFilterDays(genvex_nabto, GenvexNabtoDatapointKey.FILTER_REPLACE_TIME_REMAIN))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.HUMIDITY):
        new_entities.append(GenvexConnectSensorHumidity(genvex_nabto, GenvexNabtoDatapointKey.HUMIDITY))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.HUMIDITY_AVG):
        new_entities.append(GenvexConnectSensorHumidity(genvex_nabto, GenvexNabtoDatapointKey.HUMIDITY_AVG))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.HUMIDITY_HIGH_LEVEL):
        new_entities.append(GenvexConnectSensorMisc(genvex_nabto, GenvexNabtoDatapointKey.HUMIDITY_HIGH_LEVEL, "mdi:water-percent"))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.HUMIDITY_HIGH_LEVEL_TIME):
        new_entities.append(GenvexConnectSensorMisc(genvex_nabto, GenvexNabtoDatapointKey.HUMIDITY_HIGH_LEVEL_TIME, "mdi:water-percent"))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.STATE_CODE):
        new_entities.append(GenvexConnectSensorControlState602(genvex_nabto, GenvexNabtoDatapointKey.STATE_CODE))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.TEMP_CONDENSER):
        new_entities.append(GenvexConnectSensorTemperature(genvex_nabto, GenvexNabtoDatapointKey.TEMP_CONDENSER))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.TEMP_EVAPORATOR):
        new_entities.append(GenvexConnectSensorTemperature(genvex_nabto, GenvexNabtoDatapointKey.TEMP_EVAPORATOR))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.TEMP_EXHAUST):
        new_entities.append(GenvexConnectSensorTemperature(genvex_nabto, GenvexNabtoDatapointKey.TEMP_EXHAUST))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.TEMP_EXTRACT):
        new_entities.append(GenvexConnectSensorTemperature(genvex_nabto, GenvexNabtoDatapointKey.TEMP_EXTRACT))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.TEMP_HOTWATER_BOTTOM):
        new_entities.append(GenvexConnectSensorTemperature(genvex_nabto, GenvexNabtoDatapointKey.TEMP_HOTWATER_BOTTOM))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.TEMP_HOTWATER_TOP):
        new_entities.append(GenvexConnectSensorTemperature(genvex_nabto, GenvexNabtoDatapointKey.TEMP_HOTWATER_TOP))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.TEMP_OUTSIDE):
        new_entities.append(GenvexConnectSensorTemperature(genvex_nabto, GenvexNabtoDatapointKey.TEMP_OUTSIDE))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.TEMP_ROOM):
        new_entities.append(GenvexConnectSensorTemperature(genvex_nabto, GenvexNabtoDatapointKey.TEMP_ROOM))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.TEMP_SUPPLY):
        new_entities.append(GenvexConnectSensorTemperature(genvex_nabto, GenvexNabtoDatapointKey.TEMP_SUPPLY))
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.VOC_LEVEL):
        new_entities.append(GenvexConnectSensorVOC(genvex_nabto, GenvexNabtoDatapointKey.VOC_LEVEL))
        
        
    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.UNKNOWN_VALUE_1):
        new_entities.append(GenvexConnectSensorMisc(genvex_nabto, GenvexNabtoDatapointKey.UNKNOWN_VALUE_1))

    if genvex_nabto.provides_value(GenvexNabtoDatapointKey.ALARM_1_CODE):
        alarmHandler = GenvexConnectCTS400AlarmHandler(genvex_nabto)
        new_entities.append(GenvexConnectSensorCTS400AlarmList(genvex_nabto, alarmHandler))
        new_entities.append(GenvexConnectSensorCTS400AlarmCount(genvex_nabto, alarmHandler))
        # Trigger the alarm handler to react on the starting state
        alarmHandler.on_change(0, 0)
        
        
    if (
        genvex_nabto.provides_value(GenvexNabtoDatapointKey.TEMP_SUPPLY)
        and genvex_nabto.provides_value(GenvexNabtoDatapointKey.TEMP_EXTRACT)
        and genvex_nabto.provides_value(GenvexNabtoDatapointKey.TEMP_OUTSIDE)
    ):
        new_entities.append(GenvexConnectSensorEfficiency(genvex_nabto))
    
    async_add_entities(new_entities)


class GenvexConnectSensor(GenvexConnectEntityBase[GenvexNabtoDatapointKey], SensorEntity): # type: ignore
    def __init__(self, genvexNabto: GenvexNabto, name: str, valueKey: GenvexNabtoDatapointKey, useDefaultUpdateHandler: bool = True):
        super().__init__(genvexNabto, name, valueKey, useDefaultUpdateHandler)
        self._attr_state_class = SensorStateClass.MEASUREMENT

    def set_unit_of_measurement(self, uom: str|None):
        self._attr_native_unit_of_measurement = self.parse_unit_of_measure(uom)

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = self.genvex_nabto.get_value(self._value_key)
        if self._attr_native_value is float:
            self._attr_native_value = round(self._attr_native_value, 2)


class GenvexConnectSensorMisc(GenvexConnectSensor):
    def __init__(self, genvexNabto: GenvexNabto, valueKey:GenvexNabtoDatapointKey, icon:str|None = None):
        super().__init__(genvexNabto, valueKey.value, valueKey)
        if icon is not None:
            self._attr_icon = icon

class GenvexConnectSensorTemperature(GenvexConnectSensor):
    def __init__(self, genvexNabto: GenvexNabto, valueKey:GenvexNabtoDatapointKey):
        super().__init__(genvexNabto, valueKey.value, valueKey)
        self._attr_device_class = SensorDeviceClass.TEMPERATURE


class GenvexConnectSensorHumidity(GenvexConnectSensor):
    def __init__(self, genvexNabto: GenvexNabto, valueKey:GenvexNabtoDatapointKey):
        super().__init__(genvexNabto, valueKey.value, valueKey)
        self._attr_device_class = SensorDeviceClass.HUMIDITY
        self._attr_icon = "mdi:water-percent"


class GenvexConnectSensorCO2(GenvexConnectSensor):
    def __init__(self, genvexNabto: GenvexNabto, valueKey:GenvexNabtoDatapointKey):
        super().__init__(genvexNabto, valueKey.value, valueKey)
        self._attr_device_class = SensorDeviceClass.CO2


class GenvexConnectSensorVOC(GenvexConnectSensor):
    def __init__(self, genvexNabto: GenvexNabto, valueKey:GenvexNabtoDatapointKey):
        super().__init__(genvexNabto, valueKey.value, valueKey)
        self._attr_device_class = SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS_PARTS


class GenvexConnectSensorPercentage(GenvexConnectSensor):
    def __init__(self, genvexNabto: GenvexNabto, valueKey:GenvexNabtoDatapointKey, icon: str | None = None):
        super().__init__(genvexNabto, valueKey.value, valueKey)
        self._attr_icon = icon if icon is not None else "mdi:percent"


class GenvexConnectSensorFanRPM(GenvexConnectSensor):
    def __init__(self, genvexNabto: GenvexNabto, valueKey:GenvexNabtoDatapointKey):
        super().__init__(genvexNabto, valueKey.value, valueKey)
        self._attr_suggested_display_precision = 0
        self._attr_icon = "mdi:fan"


class GenvexConnectSensorFilterDays(GenvexConnectSensor):
    def __init__(self, genvexNabto: GenvexNabto, valueKey:GenvexNabtoDatapointKey, icon: str | None = None):
        super().__init__(genvexNabto, valueKey.value, valueKey)
        self._attr_icon = icon if icon is not None else "mdi:air-filter"


class GenvexConnectSensorEfficiency(GenvexConnectEntityBase[None], SensorEntity): # type: ignore
    def __init__(self, genvexNabto:GenvexNabto):
        super().__init__(genvexNabto, "efficiency", None, False)
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_device_class = SensorDeviceClass.POWER_FACTOR
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_suggested_display_precision = 1
        self._attr_icon = "mdi:variable"
        self._attr_should_poll = True

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        supply = self.genvex_nabto.get_value(GenvexNabtoDatapointKey.TEMP_SUPPLY)
        outside = self.genvex_nabto.get_value(GenvexNabtoDatapointKey.TEMP_OUTSIDE)
        extract = self.genvex_nabto.get_value(GenvexNabtoDatapointKey.TEMP_EXTRACT)
        
        if supply is None or outside is None or extract is None:
            return
        
        if extract - outside == 0:
            return

        self._attr_native_value = ((supply - outside) / (extract - outside)) * 100


class GenvexConnectSensorControlState602(GenvexConnectSensor):
    def __init__(self, genvexNabto: GenvexNabto, valueKey:GenvexNabtoDatapointKey):
        super().__init__(genvexNabto, "cts602_state", valueKey)
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
        self._attr_native_value = f"state_{int(self.genvex_nabto.get_value(self._value_key) or 0)}"


class GenvexConnectSensorAlarmOptima270(GenvexConnectSensor):
    def __init__(self, genvexNabto: GenvexNabto, valueKey:GenvexNabtoDatapointKey):
        super().__init__(genvexNabto, "optima270_alarms", valueKey)
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
        self._attr_native_value = f"state_{int(self.genvex_nabto.get_value(self._value_key) or 0)}"


class GenvexConnectCTS400AlarmHandler:
    active_alarms:List[int] = []
    update_handlers:List[Callable[[int, int], None]] = []
    
    def __init__(self, genvex_nabto: GenvexNabto) -> None:
        self.genvex_nabto = genvex_nabto
        self.update_handlers = []
        genvex_nabto.register_update_handler(GenvexNabtoDatapointKey.ALARM_1_CODE, self.on_change)
        genvex_nabto.register_update_handler(GenvexNabtoDatapointKey.ALARM_2_CODE, self.on_change)
        genvex_nabto.register_update_handler(GenvexNabtoDatapointKey.ALARM_3_CODE, self.on_change)
        genvex_nabto.register_update_handler(GenvexNabtoDatapointKey.FILTER_OK, self.on_change)

    def on_change(self, _old_value:float|int, _new_value:float|int):
        # Recalculate the active alarms
        critical_errors = int(self.genvex_nabto.get_value(GenvexNabtoDatapointKey.ALARM_1_CODE) or 0)
        warning_errors = int(self.genvex_nabto.get_value(GenvexNabtoDatapointKey.ALARM_2_CODE) or 0)
        info_errors = int(self.genvex_nabto.get_value(GenvexNabtoDatapointKey.ALARM_3_CODE) or 0)
        filter_change = self.genvex_nabto.get_value(GenvexNabtoDatapointKey.FILTER_OK) == 0

        self.active_alarms = []
        for i in range(0, 16):
            if i & critical_errors:
                self.active_alarms.append(i + 48)
            critical_errors >>= 1
        for i in range(0, 16):
            if i & warning_errors:
                self.active_alarms.append(i + 16)
            warning_errors >>= 1
        for i in range(0, 16):
            if i & info_errors:
                self.active_alarms.append(i)
            info_errors >>= 1

        # filter alarm is not always active, sometimes only the filterOK is 
        if filter_change and 1 not in self.active_alarms:
            self.active_alarms.append(1)
            
        # Trigger an update of any sensors listening on this handler.
        for update_method in self.update_handlers:
            update_method(0, 0)

    def get_active_alarm_count(self):
        return len(self.active_alarms)

    def get_active_alarms(self):
        return self.active_alarms

    def add_update_handler(self, update_method: Callable[[int, int], None]):
        self.update_handlers.append(update_method)


# This sensor is more complex than the others, due to using the values of 3 datapoints.
class GenvexConnectSensorCTS400AlarmList(GenvexConnectEntityBase[None], SensorEntity): # type: ignore
    def __init__(self, genvexNabto: GenvexNabto, alarmHandler: GenvexConnectCTS400AlarmHandler):
        super().__init__(genvexNabto, "alarmlist", None, False)
        self._attr_state_class = None
        self._attr_icon = "mdi:alarm-light"
        self._alarmHandler = alarmHandler
        self._alarmHandler.add_update_handler(self._on_change)
        self._alarmTextValues = {
            1: "Filterchange",
            15: "De-icing (timeout)",
            16: "T1 disconnected",
            17: "T1 short-circuited",
            18: "T2 disconnected",
            19: "T2 short-circuited",
            20: "T3 disconnected",
            21: "T3 short-circuited",
            22: "T4 disconnected",
            23: "T4 short-circuited",
            24: "T7 disconnected",
            25: "T7 short-circuited",
            26: "Failure humidity sensor",
            27: "Failure CO2 sensor",
            28: "Failure thermostat afterheating",
            29: "Frost risk afterheating",
            48: "Firedamper",
            49: "Fire",
            50: "Frost afterheating",
            51: "Low room temperature",
            52: "Emergency stop",
        }

    def translateKey(self, key:int) -> str:
        if key in self._alarmTextValues:
            return self._alarmTextValues[key]
        return "Unknown alarm"

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        if self._alarmHandler.get_active_alarm_count() == 0:
            self._attr_native_value = "No Alarm"
            return
        # Join the string representation of the active alarms
        self._attr_native_value = ", ".join(map(lambda x: self.translateKey(x), self._alarmHandler.get_active_alarms()))


# This sensor is more complex than the others, due to using the values of 3 datapoints.
class GenvexConnectSensorCTS400AlarmCount(GenvexConnectEntityBase[None], SensorEntity): # type: ignore
    def __init__(self, genvexNabto: GenvexNabto, alarmHandler: GenvexConnectCTS400AlarmHandler):
        super().__init__(genvexNabto, "alarmcount", None, False)
        self._attr_state_class = None
        self._attr_icon = "mdi:alarm-light"
        self._alarmHandler = alarmHandler
        self._alarmHandler.add_update_handler(self._on_change)

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = self._alarmHandler.get_active_alarm_count()
