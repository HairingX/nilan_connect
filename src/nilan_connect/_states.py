"""The states Nilan's and Genvex's controllers report, each shared by every controller that has it.

A controller numbers its states its own way; each model maps its numbers onto these. A state's
number here is stable, and where the CTS602's manual numbers a state, it is that number.

Sources:
    Nilan, "Software instructions Comfort CTS400" (S75) 1.30, pages 23-24: the CTS400's alarms.
    Nilan, "CTS 602 Modbus user manual" 3.00, pages 15-16, and "Protocol description Nilan CTS602
    with HMI350T Modbus" version 23: the CTS602's alarms and every other state below. All are in
    this repository's docs/models. The Optimas' alarms and the heat pump's states were found in
    material published online.
"""
from __future__ import annotations

from enum import IntEnum


class Alarm(IntEnum):
    """An alarm. A sensor alarm names the sensor by the controller's own T number, as its panel
    does; the same number is a different sensor on another controller."""
    NONE = 0
    CHANGE_FILTER = 1
    EXTERNAL_FILTER = 2
    EXTERNAL_STOP = 3
    EMERGENCY_STOP = 4
    DEFROST_TIMEOUT_EXCHANGER = 5
    DEFROST_TIMEOUT_COMPRESSOR = 6
    SENSOR_ERROR = 7
    CONTROL_SENSOR_ERROR = 8
    """The sensor chosen to control the temperature has failed."""
    HUMIDITY_SENSOR_ERROR = 9
    CO2_SENSOR_ERROR = 10
    AIR_TEMPERATURE_ERROR = 11
    WATER_TEMPERATURE_ERROR = 12
    CENTRAL_HEAT_TEMPERATURE_ERROR = 13
    FLOW_TEMPERATURE_ERROR = 14
    RETURN_TEMPERATURE_ERROR = 15
    AFTERHEAT_FROST_THERMOSTAT_ERROR = 16
    AFTERHEAT_FROST_RISK = 17
    AFTERHEAT_FROST = 18
    FROST_FAILURE = 19
    FIRE = 20
    FIRE_INPUT = 21
    FIRE_TEST_ERROR = 22
    FIRE_DAMPER_1_ERROR = 23
    FIRE_DAMPER_2_ERROR = 24
    FIRE_DAMPER_3_ERROR = 25
    FIRE_DAMPER_4_ERROR = 26
    FIRE_BOX_1_ERROR = 27
    FIRE_BOX_2_ERROR = 28
    ROOM_TEMPERATURE_LOW = 29
    PRESSURE = 30
    """High or low pressure; the controller does not say which."""
    HIGH_PRESSURE = 31
    LOW_PRESSURE = 32
    SUPPLY_FAN_ERROR = 33
    EXTRACT_FAN_ERROR = 34
    FAN_ERROR = 35
    MOTOR_OVERHEAT = 36
    ROTOR = 37
    PANEL_COMMUNICATION = 38
    INTERNAL_MODBUS = 39
    HARDWARE = 40
    TIMEOUT = 41
    """A warning has become critical."""
    DOOR_OPEN = 42
    BOILER_OVERHEAT = 43
    REHEAT_OVERHEAT = 44
    REHEAT_NO_AIRFLOW = 45
    WATER_BOILING = 46
    SOFTWARE = 47
    WATCHDOG = 48
    SETTINGS_CHANGED = 49
    LEGIONELLA_NOT_DONE = 50
    POWER_OUTAGE = 51
    MODEM = 52
    NETWORK = 53
    ANODE_WORN = 54
    EVAPORATOR_LOW = 55
    SLAVE_IO = 56
    OPTIONS_MODULE_MISSING = 57
    PRESET_ERROR = 58
    SOFTWARE_REJECTED = 59
    DAMPER_TEST_FAILED = 60
    SENSOR_T1_OPEN = 101
    SENSOR_T2_OPEN = 102
    SENSOR_T3_OPEN = 103
    SENSOR_T4_OPEN = 104
    SENSOR_T5_OPEN = 105
    SENSOR_T6_OPEN = 106
    SENSOR_T7_OPEN = 107
    SENSOR_T8_OPEN = 108
    SENSOR_T9_OPEN = 109
    SENSOR_T10_OPEN = 110
    SENSOR_T11_OPEN = 111
    SENSOR_T12_OPEN = 112
    SENSOR_T13_OPEN = 113
    SENSOR_T14_OPEN = 114
    SENSOR_T15_OPEN = 115
    SENSOR_T16_OPEN = 116
    SENSOR_T1_SHORT = 201
    SENSOR_T2_SHORT = 202
    SENSOR_T3_SHORT = 203
    SENSOR_T4_SHORT = 204
    SENSOR_T5_SHORT = 205
    SENSOR_T6_SHORT = 206
    SENSOR_T7_SHORT = 207
    SENSOR_T8_SHORT = 208
    SENSOR_T9_SHORT = 209
    SENSOR_T10_SHORT = 210
    SENSOR_T11_SHORT = 211
    SENSOR_T12_SHORT = 212
    SENSOR_T13_SHORT = 213
    SENSOR_T14_SHORT = 214
    SENSOR_T15_SHORT = 215
    SENSOR_T16_SHORT = 216
    SENSOR_T1_ERROR = 301
    SENSOR_T2_ERROR = 302
    SENSOR_T3_ERROR = 303
    SENSOR_T4_ERROR = 304
    SENSOR_T5_ERROR = 305
    SENSOR_T6_ERROR = 306
    SENSOR_T7_ERROR = 307
    SENSOR_T8_ERROR = 308
    SENSOR_T9_ERROR = 309
    SENSOR_T10_ERROR = 310
    SENSOR_T11_ERROR = 311


class OperationState(IntEnum):
    """What the unit, or its heat pump, is doing. 0 to 17 are the CTS602's control states."""
    OFF = 0
    SHIFT = 1
    STOP = 2
    START = 3
    STANDBY = 4
    VENTILATION_STOP = 5
    VENTILATION = 6
    HEATING = 7
    COOLING = 8
    HOT_WATER = 9
    LEGIONELLA = 10
    COOLING_HOT_WATER = 11
    CENTRAL_HEATING = 12
    DEFROST = 13
    FROST_PROTECTION = 14
    SERVICE = 15
    ALARM = 16
    HEATING_HOT_WATER = 17
    READY = 18
    HEATING_START_UP = 19
    COOLING_START_UP = 20
    HOT_WATER_START_UP = 21
    AIR_DEFROST = 22
    HOTGAS_DEFROST = 23
    DRIP_DELAY = 24
    HEAT_PUMP_STOP = 25
    ELECTRIC_HEATING = 26
    ELECTRIC_HOT_WATER = 27
    FORCED_COLD_PUMP = 28
    HOT_WATER_HEAT_PUMP_STOP = 29
    HEATING_HEAT_PUMP_STOP = 30
    PUMP_EXERCISE = 31
    FORCED_START_UP = 32
    FORCED_RUNNING = 33
    FORCED_RUNNING_HEAT_PUMP_STOP = 34
    MANUAL = 35
    EXTERNAL_STOP = 36
    FORCED_LOW_SPEED = 37


class OperationMode(IntEnum):
    OFF = 0
    HEAT = 1
    """Heating only, no cooling."""
    COOL = 2
    """Cooling only, no heating."""
    AUTO = 3
    SERVICE = 4


class Weekday(IntEnum):
    """A day of the week, numbered as ISO 8601 numbers them; OFF for none."""
    OFF = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class HeatSource(IntEnum):
    """What heats, first named first."""
    OFF = 0
    ELECTRIC = 1
    HEAT_PUMP = 2
    AFTERHEAT = 3
    HEAT_PUMP_THEN_AFTERHEAT = 4
    AFTERHEAT_THEN_HEAT_PUMP = 5
    HEAT_PUMP_THEN_ELECTRIC = 6


class CompressorPriority(IntEnum):
    """What the compressor serves first."""
    HOT_WATER = 0
    INLET_AIR = 1


class CoolingSetpoint(IntEnum):
    """How far above the temperature setpoint cooling starts."""
    OFF = 0
    PLUS_0 = 1
    PLUS_1 = 2
    PLUS_2 = 3
    PLUS_3 = 4
    PLUS_4 = 5
    PLUS_5 = 6
    PLUS_7 = 7
    PLUS_10 = 8


class AirExchangeMode(IntEnum):
    ENERGY = 0
    COMFORT = 1
    COMFORT_WATER = 2


class ControlSensor(IntEnum):
    """The sensor the temperature is controlled by."""
    USER_PANEL = 0
    EXTERNAL = 1
    INLET = 2
    EXHAUST = 3


class CentralHeatMode(IntEnum):
    FROST_PROTECTION_ONLY = 0
    """Only moving the pump and protecting against frost."""
    ALWAYS = 1
    WHEN_ROOM_COLD = 2


class CirculationPumpMode(IntEnum):
    WHEN_HEATING = 0
    CONTINUOUS = 1


class ServiceMode(IntEnum):
    OFF = 0
    DEFROST = 1
    FLAPS = 2
    INLET = 3
    EXHAUST = 4
    COMPRESSOR = 5
    HEATING = 6
    HOT_WATER = 7
    CENTRAL_HEAT = 8


class DamperTestState(IntEnum):
    OFF = 0
    STANDBY = 1
    START = 2
    CLOSING = 3
    OPENING = 4
    OK = 5
    ERROR = 6
