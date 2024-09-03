"""Platform for sensor integration."""

from typing import Callable
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature, PERCENTAGE, CONCENTRATION_PARTS_PER_MILLION, REVOLUTIONS_PER_MINUTE
from genvexnabto import GenvexNabto, GenvexNabtoDatapointKey, GenvexNabtoSetpointKey
from .entity import GenvexConnectEntityBase

from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    genvexNabto: GenvexNabto = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = []
    
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.ALARM_1_CODE):
        new_entities.append(GenvexConnectSensorMisc(genvexNabto, GenvexNabtoDatapointKey.ALARM_1_CODE))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.ALARM_1_INFO):
        new_entities.append(GenvexConnectSensorMisc(genvexNabto, GenvexNabtoDatapointKey.ALARM_1_INFO))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.ALARM_2_CODE):
        new_entities.append(GenvexConnectSensorMisc(genvexNabto, GenvexNabtoDatapointKey.ALARM_2_CODE))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.ALARM_2_INFO):
        new_entities.append(GenvexConnectSensorMisc(genvexNabto, GenvexNabtoDatapointKey.ALARM_2_INFO))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.ALARM_3_CODE):
        new_entities.append(GenvexConnectSensorMisc(genvexNabto, GenvexNabtoDatapointKey.ALARM_3_CODE))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.ALARM_3_INFO):
        new_entities.append(GenvexConnectSensorMisc(genvexNabto, GenvexNabtoDatapointKey.ALARM_3_INFO))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.ALARM_BITS):
        new_entities.append(GenvexConnectSensorAlarmOptima270(genvexNabto, GenvexNabtoDatapointKey.ALARM_BITS))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.CO2_LEVEL):
        new_entities.append(GenvexConnectSensorCO2(genvexNabto, GenvexNabtoDatapointKey.CO2_LEVEL))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.DEFROST_TIME_AGO):
        new_entities.append(GenvexConnectSensorFilterDays(genvexNabto, GenvexNabtoDatapointKey.DEFROST_TIME_AGO, icon="mdi:snowflake-melt"))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.FAN_DUTYCYCLE_EXTRACT):
        new_entities.append(GenvexConnectSensorPercentage(genvexNabto, GenvexNabtoDatapointKey.FAN_DUTYCYCLE_EXTRACT, "mdi:fan"))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.FAN_DUTYCYCLE_SUPPLY):
        new_entities.append(GenvexConnectSensorPercentage(genvexNabto, GenvexNabtoDatapointKey.FAN_DUTYCYCLE_SUPPLY, "mdi:fan"))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.FAN_LEVEL_CURRENT):
        new_entities.append(GenvexConnectSensorMisc(genvexNabto, GenvexNabtoDatapointKey.FAN_LEVEL_CURRENT))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.FAN_LEVEL_EXTRACT):
        new_entities.append(GenvexConnectSensorMisc(genvexNabto, GenvexNabtoDatapointKey.FAN_LEVEL_EXTRACT)) 
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.FAN_LEVEL_SUPPLY):
        new_entities.append(GenvexConnectSensorMisc(genvexNabto, GenvexNabtoDatapointKey.FAN_LEVEL_SUPPLY))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.FAN_RPM_EXTRACT):
        new_entities.append(GenvexConnectSensorFanRPM(genvexNabto, GenvexNabtoDatapointKey.FAN_RPM_EXTRACT))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.FAN_RPM_SUPPLY):
        new_entities.append(GenvexConnectSensorFanRPM(genvexNabto, GenvexNabtoDatapointKey.FAN_RPM_SUPPLY))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.FILTER_REPLACE_TIME_AGO):
        new_entities.append(GenvexConnectSensorFilterDays(genvexNabto, GenvexNabtoDatapointKey.FILTER_REPLACE_TIME_AGO))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.FILTER_REPLACE_TIME_REMAIN):
        new_entities.append(GenvexConnectSensorFilterDays(genvexNabto, GenvexNabtoDatapointKey.FILTER_REPLACE_TIME_REMAIN))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.HUMIDITY):
        new_entities.append(GenvexConnectSensorHumidity(genvexNabto, GenvexNabtoDatapointKey.HUMIDITY))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.HUMIDITY_AVG):
        new_entities.append(GenvexConnectSensorHumidity(genvexNabto, GenvexNabtoDatapointKey.HUMIDITY_AVG))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.HUMIDITY_HIGH_LEVEL):
        new_entities.append(GenvexConnectSensorMisc(genvexNabto, GenvexNabtoDatapointKey.HUMIDITY_HIGH_LEVEL))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.HUMIDITY_HIGH_LEVEL_TIME):
        new_entities.append(GenvexConnectSensorMisc(genvexNabto, GenvexNabtoDatapointKey.HUMIDITY_HIGH_LEVEL_TIME))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.STATE_CODE):
        new_entities.append(GenvexConnectSensorControlState602(genvexNabto, GenvexNabtoDatapointKey.STATE_CODE))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.TEMP_CONDENSER):
        new_entities.append(GenvexConnectSensorTemperature(genvexNabto, GenvexNabtoDatapointKey.TEMP_CONDENSER))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.TEMP_EVAPORATOR):
        new_entities.append(GenvexConnectSensorTemperature(genvexNabto, GenvexNabtoDatapointKey.TEMP_EVAPORATOR))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.TEMP_EXHAUST):
        new_entities.append(GenvexConnectSensorTemperature(genvexNabto, GenvexNabtoDatapointKey.TEMP_EXHAUST))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.TEMP_EXTRACT):
        new_entities.append(GenvexConnectSensorTemperature(genvexNabto, GenvexNabtoDatapointKey.TEMP_EXTRACT))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.TEMP_HOTWATER_BOTTOM):
        new_entities.append(GenvexConnectSensorTemperature(genvexNabto, GenvexNabtoDatapointKey.TEMP_HOTWATER_BOTTOM))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.TEMP_HOTWATER_TOP):
        new_entities.append(GenvexConnectSensorTemperature(genvexNabto, GenvexNabtoDatapointKey.TEMP_HOTWATER_TOP))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.TEMP_OUTSIDE):
        new_entities.append(GenvexConnectSensorTemperature(genvexNabto, GenvexNabtoDatapointKey.TEMP_OUTSIDE))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.TEMP_ROOM):
        new_entities.append(GenvexConnectSensorTemperature(genvexNabto, GenvexNabtoDatapointKey.TEMP_ROOM))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.TEMP_SUPPLY):
        new_entities.append(GenvexConnectSensorTemperature(genvexNabto, GenvexNabtoDatapointKey.TEMP_SUPPLY))
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.VOC_LEVEL):
        new_entities.append(GenvexConnectSensorVOC(genvexNabto, GenvexNabtoDatapointKey.VOC_LEVEL))
        
        
    if genvexNabto.provides_value(GenvexNabtoDatapointKey.UNKNOWN_VALUE_1):
        new_entities.append(GenvexConnectSensorMisc(genvexNabto, GenvexNabtoDatapointKey.UNKNOWN_VALUE_1))

    if genvexNabto.provides_value(GenvexNabtoDatapointKey.ALARM_1_CODE):
        alarmHandler = GenvexConnectCTS400AlarmHandler(genvexNabto)
        new_entities.append(GenvexConnectSensorCTS400AlarmList(genvexNabto, alarmHandler))
        new_entities.append(GenvexConnectSensorCTS400AlarmCount(genvexNabto, alarmHandler))
        # Trigger the alarm handler to react on the starting state
        alarmHandler._on_change(0, 0)
        
        
    if (
        genvexNabto.provides_value(GenvexNabtoDatapointKey.TEMP_SUPPLY)
        and genvexNabto.provides_value(GenvexNabtoDatapointKey.TEMP_EXTRACT)
        and genvexNabto.provides_value(GenvexNabtoDatapointKey.TEMP_OUTSIDE)
    ):
        new_entities.append(GenvexConnectSensorEfficiency(genvexNabto))
    
    async_add_entities(new_entities)


class GenvexConnectSensor(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto: GenvexNabto, name: str, valueKey: GenvexNabtoDatapointKey|GenvexNabtoSetpointKey|None, useDefaultUpdateHandler: bool = True):
        super().__init__(genvexNabto, name, valueKey, useDefaultUpdateHandler)
        self._attr_state_class = SensorStateClass.MEASUREMENT

    def set_unit_of_measurement(self, uom: str):
        self._attr_native_unit_of_measurement = self.parse_unit_of_measure(uom)

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = self.genvex_nabto.get_value(self._value_key)


class GenvexConnectSensorMisc(GenvexConnectSensor):
    def __init__(self, genvexNabto: GenvexNabto, valueKey:GenvexNabtoDatapointKey|GenvexNabtoSetpointKey):
        super().__init__(genvexNabto, valueKey.value, valueKey)
        # self._attr_device_class = SensorDeviceClass.
        # self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

class GenvexConnectSensorTemperature(GenvexConnectSensor):
    def __init__(self, genvexNabto: GenvexNabto, valueKey:GenvexNabtoDatapointKey|GenvexNabtoSetpointKey):
        super().__init__(genvexNabto, valueKey.value, valueKey)
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        # self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS


class GenvexConnectSensorHumidity(GenvexConnectSensor):
    def __init__(self, genvexNabto: GenvexNabto, valueKey:GenvexNabtoDatapointKey|GenvexNabtoSetpointKey):
        super().__init__(genvexNabto, valueKey.value, valueKey)
        self._attr_device_class = SensorDeviceClass.HUMIDITY
        # self._attr_native_unit_of_measurement = PERCENTAGE


class GenvexConnectSensorCO2(GenvexConnectSensor):
    def __init__(self, genvexNabto: GenvexNabto, valueKey:GenvexNabtoDatapointKey|GenvexNabtoSetpointKey):
        super().__init__(genvexNabto, valueKey.value, valueKey)
        self._attr_device_class = SensorDeviceClass.CO2
        # self._attr_native_unit_of_measurement = CONCENTRATION_PARTS_PER_MILLION


class GenvexConnectSensorVOC(GenvexConnectSensor):
    def __init__(self, genvexNabto: GenvexNabto, valueKey:GenvexNabtoDatapointKey|GenvexNabtoSetpointKey):
        super().__init__(genvexNabto, valueKey.value, valueKey)
        self._attr_device_class = SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS_PARTS
        # self._attr_native_unit_of_measurement = CONCENTRATION_PARTS_PER_MILLION


class GenvexConnectSensorPercentage(GenvexConnectSensor):
    def __init__(self, genvexNabto: GenvexNabto, valueKey:GenvexNabtoDatapointKey|GenvexNabtoSetpointKey, icon: str | None = None):
        super().__init__(genvexNabto, valueKey.value, valueKey)
        self._attr_icon = icon if icon is not None else "mdi:percent"
        # self._attr_native_unit_of_measurement = PERCENTAGE


class GenvexConnectSensorFanRPM(GenvexConnectSensor):
    def __init__(self, genvexNabto: GenvexNabto, valueKey:GenvexNabtoDatapointKey|GenvexNabtoSetpointKey):
        super().__init__(genvexNabto, valueKey.value, valueKey)
        self._attr_suggested_display_precision = 0
        self._attr_icon = "mdi:fan"
        # self._attr_native_unit_of_measurement = REVOLUTIONS_PER_MINUTE


class GenvexConnectSensorFilterDays(GenvexConnectSensor):
    def __init__(self, genvexNabto: GenvexNabto, valueKey:GenvexNabtoDatapointKey|GenvexNabtoSetpointKey, icon: str | None = None):
        super().__init__(genvexNabto, valueKey.value, valueKey)
        self._attr_icon = icon if icon is not None else "mdi:air-filter"
        # self._attr_native_unit_of_measurement = "d"


class GenvexConnectSensorEfficiency(GenvexConnectSensor):
    def __init__(self, genvexNabto:GenvexNabto):
        super().__init__(genvexNabto, "efficiency", None, False)
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_suggested_display_precision = 1
        self._attr_icon = "mdi:variable"

    @property
    def should_poll(self) -> bool:
        """HA should poll this entity"""
        return True

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
    def __init__(self, genvexNabto: GenvexNabto, valueKey:GenvexNabtoDatapointKey|GenvexNabtoSetpointKey):
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
        self._attr_native_value = f"state_{int(self.genvex_nabto.get_value(self._value_key))}"


class GenvexConnectSensorAlarmOptima270(GenvexConnectSensor):
    def __init__(self, genvexNabto: GenvexNabto, valueKey:GenvexNabtoDatapointKey|GenvexNabtoSetpointKey):
        super().__init__(genvexNabto, "optima270_alarms", valueKey)
        self._attr_device_class = SensorDeviceClass.ENUM
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

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:alarm-bell"

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = f"state_{int(self.genvex_nabto.get_value(self._value_key))}"


class GenvexConnectCTS400AlarmHandler:
    def __init__(self, genvexNabto: GenvexNabto) -> None:
        self.genvexNabto = genvexNabto
        self.activeAlarms = []
        self.updateHandlers = []
        genvexNabto.register_update_handler(GenvexNabtoDatapointKey.ALARM_1_CODE, self._on_change)
        genvexNabto.register_update_handler(GenvexNabtoDatapointKey.ALARM_2_CODE, self._on_change)
        genvexNabto.register_update_handler(GenvexNabtoDatapointKey.ALARM_3_CODE, self._on_change)

    def _on_change(self, _old_value, _new_value):
        # Recalculate the active alarms
        criticalErrors = int(self.genvexNabto.get_value(GenvexNabtoDatapointKey.ALARM_1_CODE))
        warningErrors = int(self.genvexNabto.get_value(GenvexNabtoDatapointKey.ALARM_2_CODE))
        infoErrors = int(self.genvexNabto.get_value(GenvexNabtoDatapointKey.ALARM_3_CODE))

        self.activeAlarms = []
        for i in range(0, 16):
            if i & criticalErrors:
                self.activeAlarms.append(i + 48)
            criticalErrors >>= 1
        for i in range(0, 16):
            if i & warningErrors:
                self.activeAlarms.append(i + 16)
            warningErrors >>= 1
        for i in range(0, 16):
            if i & infoErrors:
                self.activeAlarms.append(i)
            infoErrors >>= 1

        # Trigger an update of any sensors listening on this handler.
        for updateMethod in self.updateHandlers:
            updateMethod(0, 0)

    def getActiveAlarmCount(self):
        return len(self.activeAlarms)

    def getActiveAlarms(self):
        return self.activeAlarms

    def addUpdateHandler(self, updateMethod: Callable[[int, int], None]):
        self.updateHandlers.append(updateMethod)


# This sensor is more complex than the others, due to using the values of 3 datapoints.
class GenvexConnectSensorCTS400AlarmList(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto: GenvexNabto, alarmHandler: GenvexConnectCTS400AlarmHandler):
        super().__init__(genvexNabto, "alarmlist", None, False)
        self._attr_state_class = None
        self._alarmHandler = alarmHandler
        self._alarmHandler.addUpdateHandler(self._on_change)
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

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:alarm-light"

    def translateKey(self, key) -> str:
        if key in self._alarmTextValues:
            return self._alarmTextValues[key]
        return "Unknown alarm"

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        if self._alarmHandler.getActiveAlarmCount() == 0:
            self._attr_native_value = "No Alarm"
            return
        # Join the string representation of the active alarms
        self._attr_native_value = ", ".join(map(lambda x: self.translateKey(x), self._alarmHandler.getActiveAlarms()))


# This sensor is more complex than the others, due to using the values of 3 datapoints.
class GenvexConnectSensorCTS400AlarmCount(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto: GenvexNabto, alarmHandler: GenvexConnectCTS400AlarmHandler):
        super().__init__(genvexNabto, "alarmcount", None, False)
        self._attr_state_class = None
        self._alarmHandler = alarmHandler
        self._alarmHandler.addUpdateHandler(self._on_change)

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:alarm-light"

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = self._alarmHandler.getActiveAlarmCount()
