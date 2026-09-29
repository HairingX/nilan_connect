"""The key of every point a Nilan or Genvex controller can have.

A consumer's stored entities are built on the key strings, so they never change. Where two
controllers have a value that means the same, they share its key; which key a controller has is
its model's business.
"""
from __future__ import annotations

from datetime import date, datetime
from typing import Any

from modbus_event_connect import Key

from ._states import (
    AirExchangeMode,
    Alarm,
    CentralHeatMode,
    CirculationPumpMode,
    CompressorPriority,
    ControlSensor,
    CoolingSetpoint,
    DamperTestState,
    ExtraSensor,
    FilterReplaceInterval,
    HeatSource,
    OperationMode,
    OperationState,
    ServiceMode,
    Weekday,
)


class PointKey:
    """The key of each point a Nilan or Genvex controller can have."""

    # --------------------------------------------------------------------- running
    ENABLE = Key("enable", bool)
    """Whether the unit is asked to run."""
    RUNNING = Key("running", bool)
    """Whether the unit runs."""
    OPERATION_MODE = Key("operation_mode", OperationMode)
    """The operation mode chosen. SERVICE is entered through `service_mode`, not chosen here."""
    OPERATION_MODE_CURRENT = Key("operation_mode_current", OperationMode)
    """The operation mode the unit runs in."""
    STATE_CODE = Key("state_code", int)
    """The control state as the controller numbers it; `operation_state` is what it means."""
    OPERATION_STATE = Key("operation_state", OperationState)
    """What the unit is doing."""
    TIME_IN_STATE = Key("time_in_state", int)
    """Seconds the unit has been in its control state."""
    WINTER_MODE_ACTIVE = Key("winter_mode_active", bool)
    """Whether the unit runs in winter mode."""
    DEFROST_ACTIVE = Key("defrost_active", bool)
    """Whether the heat exchanger is being defrosted."""
    SERVICE_MODE = Key("service_mode", ServiceMode)
    SERVICE_CAPACITY = Key("service_capacity", float)
    """The capacity, in percent, the unit runs at in a service mode."""

    # ---------------------------------------------------------------- temperatures
    TEMP_OUTSIDE = Key("temp_outside", float)
    """Outdoor air, in °C."""
    TEMP_INTAKE = Key("temp_intake", float)
    """Fresh air as it enters the unit, in °C."""
    TEMP_PREHEAT_INTAKE = Key("temp_preheat_intake", float)
    """Air entering the preheater or earth tube, in °C."""
    TEMP_SUPPLY = Key("temp_supply", float)
    """Air supplied to the rooms, in °C."""
    TEMP_SUPPLY_AFTER_HEATER = Key("temp_supply_after_heater", float)
    """Supply air after the heating surface, in °C."""
    TEMP_EXTRACT = Key("temp_extract", float)
    """Air taken from the rooms into the unit, in °C."""
    TEMP_EXHAUST = Key("temp_exhaust", float)
    """Air leaving the unit to the outside, in °C."""
    TEMP_ROOM = Key("temp_room", float)
    """The room, in °C."""
    TEMP_ROOM_PANEL = Key("temp_room_panel", float)
    """The room at the user panel, in °C."""
    TEMP_HEATER = Key("temp_heater", float)
    """The heating surface, in °C."""
    TEMP_FROST_PROTECTION = Key("temp_frost_protection", float)
    """The frost protection sensor, in °C."""
    TEMP_CONTROLLER = Key("temp_controller", float)
    """The controller board, in °C."""
    TEMP_AUX = Key("temp_aux", float)
    """The auxiliary sensor, in °C."""

    # ------------------------------------------------------------- temperature settings
    TEMP_TARGET = Key("temp_target", float)
    """The room temperature aimed for, in °C."""
    TEMP_REGULATION_DEAD_BAND = Key("temp_regulation_dead_band", float)
    """The regulation's dead band, in °C."""
    TEMP_SUPPLY_MIN = Key("temp_supply_min", float)
    TEMP_SUPPLY_MAX = Key("temp_supply_max", float)
    TEMP_SUMMER_SUPPLY_MIN = Key("temp_summer_supply_min", float)
    TEMP_SUMMER_SUPPLY_MAX = Key("temp_summer_supply_max", float)
    TEMP_WINTER_SUPPLY_MIN = Key("temp_winter_supply_min", float)
    TEMP_WINTER_SUPPLY_MAX = Key("temp_winter_supply_max", float)
    TEMP_WINTER_MODE_THRESHOLD = Key("temp_winter_mode_threshold", float)
    """Winter below this outdoor temperature, in °C; summer above it."""
    TEMP_NIGHT_COOLING_DAY_LIMIT = Key("temp_night_cooling_day_limit", float)
    """The outdoor day temperature, in °C, above which the unit cools at night."""
    TEMP_NIGHT_COOLING_TARGET = Key("temp_night_cooling_target", float)
    """The room temperature, in °C, night cooling aims for."""
    TEMP_COOLING_START_OFFSET = Key("temp_cooling_start_offset", CoolingSetpoint)
    """How far above the target temperature cooling starts."""
    COOLING_TEMPERATURE = Key("cooling_temperature", int)
    """An Optima 301's cooling setting; no public description gives its meaning."""
    CONTROL_SENSOR = Key("control_sensor", ControlSensor)
    """The sensor the temperature is controlled by."""

    # ------------------------------------------------------------------ control panel
    PANEL_LOCK_FAN_LEVEL = Key("panel_lock_fan_level", bool)
    """Whether the control panel's fan level button is locked."""
    PANEL_LOCK_ON_OFF = Key("panel_lock_on_off", bool)
    """Whether the control panel's on/off button is locked, so the unit cannot be turned off there."""
    DIGITAL_INPUT_1 = Key("digital_input_1", bool)
    """Whether digital input D1 is active."""
    DIGITAL_INPUT_2 = Key("digital_input_2", bool)
    DIGITAL_INPUT_3 = Key("digital_input_3", bool)

    # ------------------------------------------------------------------ air quality
    HUMIDITY = Key("humidity", float)
    """Relative humidity, in percent."""
    HUMIDITY_AVG = Key("humidity_average", float)
    """The average relative humidity, in percent."""
    HUMIDITY_HIGH_ACTIVE = Key("humidity_high_active", bool)
    """Whether the high humidity function runs."""
    HUMIDITY_HIGH_LEVEL = Key("humidity_high_level", float)
    """The high humidity level, in percent."""
    HUMIDITY_HIGH_LEVEL_TIME = Key("humidity_high_level_time", float)
    """How long, in minutes, the high humidity function has run."""
    HUMIDITY_LOW_THRESHOLD = Key("humidity_low_threshold", float)
    """The low humidity level, in percent."""
    HUMIDITY_CONTROL_ENABLE = Key("humidity_control_enable", bool)
    EXTRA_SENSOR = Key("extra_sensor", ExtraSensor)
    """The extra air quality sensor fitted."""
    CO2_LEVEL = Key("co2_level", int)
    """CO2, in ppm."""
    CO2_THRESHOLD = Key("co2_threshold", int)
    """The high CO2 level, in ppm."""
    VOC_LEVEL = Key("voc_level", int)
    """Volatile organic compounds, in ppm."""
    VOC_THRESHOLD = Key("voc_threshold", int)
    """The high VOC level, in ppm."""

    # ------------------------------------------------------------------------- fans
    FAN_LEVEL = Key("fan_level", int)
    """The fan level chosen; a CTS602's manual gives 0 as off."""
    FAN_LEVEL_CURRENT = Key("fan_level_current", int)
    """The fan level the unit runs at."""
    FAN_LEVEL_SUPPLY = Key("fan_level_supply", int)
    """The level the supply fan runs at."""
    FAN_LEVEL_EXTRACT = Key("fan_level_extract", int)
    """The level the extract fan runs at."""
    FAN_DUTYCYCLE_SUPPLY = Key("fan_dutycycle_supply", float)
    """The supply fan's speed, in percent."""
    FAN_DUTYCYCLE_EXTRACT = Key("fan_dutycycle_extract", float)
    """The extract fan's speed, in percent."""
    FAN_RPM_SUPPLY = Key("fan_rpm_supply", int)
    """The supply fan's speed, in revolutions per minute."""
    FAN_RPM_EXTRACT = Key("fan_rpm_extract", int)
    """The extract fan's speed, in revolutions per minute."""
    FAN_LEVEL1_SUPPLY_PRESET = Key("fan_level1_supply_preset", float)
    """The supply fan's speed, in percent, at level 1; likewise for the other levels and fans."""
    FAN_LEVEL2_SUPPLY_PRESET = Key("fan_level2_supply_preset", float)
    FAN_LEVEL3_SUPPLY_PRESET = Key("fan_level3_supply_preset", float)
    FAN_LEVEL4_SUPPLY_PRESET = Key("fan_level4_supply_preset", float)
    FAN_LEVEL1_EXTRACT_PRESET = Key("fan_level1_extract_preset", float)
    FAN_LEVEL2_EXTRACT_PRESET = Key("fan_level2_extract_preset", float)
    FAN_LEVEL3_EXTRACT_PRESET = Key("fan_level3_extract_preset", float)
    FAN_LEVEL4_EXTRACT_PRESET = Key("fan_level4_extract_preset", float)
    FAN_LEVEL_LOW_HUMIDITY = Key("fan_level_low_humidity", int)
    """The fan level while the humidity is low."""
    FAN_LEVEL_HIGH_HUMIDITY = Key("fan_level_high_humidity", int)
    """The fan level while the humidity is high."""
    FAN_LEVEL_HIGH_HUMIDITY_TIME = Key("fan_level_high_humidity_time", int)
    """The longest time, in minutes, the fans run at their high humidity level."""
    FAN_LEVEL_HIGH_CO2 = Key("fan_level_high_co2", int)
    """The fan level while the CO2 is high."""
    FAN_LEVEL_COOLING = Key("fan_level_cooling", int)
    """The fan level while the unit cools."""
    AIR_EXCHANGE_MODE = Key("air_exchange_mode", AirExchangeMode)
    BOOST_ENABLE = Key("boost_enable", bool)
    BOOST_TIME = Key("boost_time", int)
    """How long, in minutes, a boost lasts."""
    ROTOR_SPEED = Key("rotor_speed", int)
    """The rotary heat exchanger's speed, in revolutions per minute."""

    # ----------------------------------------------------------------------- bypass
    BYPASS_ACTIVE = Key("bypass_active", bool)
    """Whether the bypass damper is open."""
    BYPASS_POSITION = Key("bypass_position", int)
    """The bypass damper's control signal; no public description gives its unit."""
    TEMP_BYPASS_OPEN_OFFSET = Key("temp_bypass_open_offset", float)
    """The bypass's opening offset, in °C."""
    TEMP_BYPASS_CLOSE_OFFSET = Key("temp_bypass_close_offset", float)
    """How far below the target temperature, in °C, the outdoor air may be before the bypass stays
    closed; 0 for no limit."""
    BYPASS_FAN_INCREASE = Key("bypass_fan_increase", int)
    """How much faster, in percent, the fans run while the bypass cools the rooms."""
    TEMP_BYPASS_FAN_INCREASE_OFFSET = Key("temp_bypass_fan_increase_offset", float)
    """How far above the target temperature, in °C, the fans run faster while the bypass cools."""

    # ---------------------------------------------------------------------- defrost
    TEMP_DEFROST_LOW_THRESHOLD = Key("temp_defrost_low_threshold", float)
    """Defrosting starts below this discharge air temperature, in °C."""
    TEMP_DEFROST_HIGH_THRESHOLD = Key("temp_defrost_high_threshold", float)
    """Defrosting stops above this discharge air temperature, in °C."""
    DEFROST_MAX_TIME = Key("defrost_max_time", int)
    """The longest defrosting, in minutes."""
    DEFROST_BREAK_TIME = Key("defrost_break_time", int)
    """The time between two defrostings, in minutes."""
    DEFROST_SUPPLY_FAN = Key("defrost_supply_fan", bool)
    """Whether the supply fan runs while the heat exchanger is defrosted."""

    # ----------------------------------------------------------------------- filter
    FILTER_OK = Key("filter_ok", bool)
    """False while the filter must be changed."""
    FILTER_REPLACE_INTERVAL = Key("filter_replace_interval", int)
    """How long between filter changes, in the unit the point states: days on some controllers,
    months on others."""
    FILTER_REPLACE_TIME_AGO = Key("filter_replace_time_ago", float)
    """Days since the filter was changed."""
    FILTER_REPLACE_TIME_REMAIN = Key("filter_replace_time_remain", float)
    """Days until the filter must be changed."""
    FILTER_REPLACE_INTERVAL_CHOICE = Key("filter_replace_interval_choice", FilterReplaceInterval)
    """How long between filter changes, where a controller chooses from fixed periods."""
    FILTER_ALARM_ON_PANEL = Key("filter_alarm_on_panel", bool)
    """Whether the filter alarm is shown on the control panel."""
    FILTER_REPLACE_RESET = Key("filter_replace_reset", bool)
    """Written to tell the unit its filter has been changed."""

    # ----------------------------------------------------------------------- alarms
    ALARM_STATUS = Key("alarm_status", bool)
    """Whether an alarm is active."""
    ALARM_RESET = Key("alarm_reset", bool)
    """Written to clear the active alarms."""
    ALARM_1_CODE = Key("alarm_1_code", int)
    """The first alarm as the controller numbers it; `alarm_1` is what it means."""
    ALARM_2_CODE = Key("alarm_2_code", int)
    ALARM_3_CODE = Key("alarm_3_code", int)
    ALARM_1 = Key("alarm_1", Alarm)
    """The first alarm."""
    ALARM_2 = Key("alarm_2", Alarm)
    ALARM_3 = Key("alarm_3", Alarm)
    ALARM_1_INFO = Key("alarm_1_info", int)
    """The first alarm's info, as the controller gives it."""
    ALARM_2_INFO = Key("alarm_2_info", int)
    ALARM_3_INFO = Key("alarm_3_info", int)
    ALARM_1_TIME = Key("alarm_1_time", datetime)
    """When the first alarm was raised, by the controller's clock, without a time zone."""
    ALARM_2_TIME = Key("alarm_2_time", datetime)
    ALARM_3_TIME = Key("alarm_3_time", datetime)
    ALARM_BITS = Key("alarm_bits", int)
    """An alarm register as the controller sends it: one bit per alarm."""
    ALARM_BITS_HIGH = Key("alarm_bits_high", int)
    """The second alarm register, where a controller has one."""
    # One key per alarm, for a controller that reports its alarms as bits.
    ALARM_EXTERNAL_STOP = Key("alarm_external_stop", bool)
    ALARM_EXTERNAL_FILTER = Key("alarm_external_filter", bool)
    ALARM_HIGH_PRESSURE = Key("alarm_high_pressure", bool)
    ALARM_LOW_PRESSURE = Key("alarm_low_pressure", bool)
    ALARM_FROST_FAILURE = Key("alarm_frost_failure", bool)
    ALARM_PANEL_COMMUNICATION = Key("alarm_panel_communication", bool)
    ALARM_INTERNAL_MODBUS = Key("alarm_internal_modbus", bool)
    ALARM_FAN_ERROR = Key("alarm_fan_error", bool)
    ALARM_SUPPLY_FAN_ERROR = Key("alarm_supply_fan_error", bool)
    ALARM_EXTRACT_FAN_ERROR = Key("alarm_extract_fan_error", bool)
    ALARM_ROTOR = Key("alarm_rotor", bool)
    ALARM_SENSOR_ERROR = Key("alarm_sensor_error", bool)
    ALARM_HUMIDITY_SENSOR_ERROR = Key("alarm_humidity_sensor_error", bool)
    ALARM_FLOW_TEMPERATURE_ERROR = Key("alarm_flow_temperature_error", bool)
    ALARM_RETURN_TEMPERATURE_ERROR = Key("alarm_return_temperature_error", bool)
    ALARM_SENSOR_T1_ERROR = Key("alarm_sensor_t1_error", bool)
    """Sensor T1 has failed; T is the controller's own numbering."""
    ALARM_SENSOR_T2_ERROR = Key("alarm_sensor_t2_error", bool)
    ALARM_SENSOR_T3_ERROR = Key("alarm_sensor_t3_error", bool)
    ALARM_SENSOR_T4_ERROR = Key("alarm_sensor_t4_error", bool)
    ALARM_SENSOR_T5_ERROR = Key("alarm_sensor_t5_error", bool)
    ALARM_SENSOR_T6_ERROR = Key("alarm_sensor_t6_error", bool)
    ALARM_SENSOR_T7_ERROR = Key("alarm_sensor_t7_error", bool)
    ALARM_SENSOR_T8_ERROR = Key("alarm_sensor_t8_error", bool)
    ALARM_SENSOR_T9_ERROR = Key("alarm_sensor_t9_error", bool)
    ALARM_SENSOR_T10_ERROR = Key("alarm_sensor_t10_error", bool)
    ALARM_SENSOR_T11_ERROR = Key("alarm_sensor_t11_error", bool)
    ALARM_FIRE_TEST_ERROR = Key("alarm_fire_test_error", bool)
    ALARM_FIRE_DAMPER_1_ERROR = Key("alarm_fire_damper_1_error", bool)
    ALARM_FIRE_DAMPER_2_ERROR = Key("alarm_fire_damper_2_error", bool)
    ALARM_FIRE_DAMPER_3_ERROR = Key("alarm_fire_damper_3_error", bool)
    ALARM_FIRE_DAMPER_4_ERROR = Key("alarm_fire_damper_4_error", bool)
    ALARM_FIRE_BOX_1_ERROR = Key("alarm_fire_box_1_error", bool)
    ALARM_FIRE_BOX_2_ERROR = Key("alarm_fire_box_2_error", bool)

    # ------------------------------------------------------------ heating and cooling
    HEAT_SOURCE = Key("heat_source", HeatSource)
    """What heats the supply air."""
    REHEAT_ENABLE = Key("reheat_enable", bool)
    REHEAT_ACTIVE = Key("reheat_active", bool)
    REHEAT_OUTPUT = Key("reheat_output", float)
    """The reheater's output, in percent."""
    PREHEAT_ENABLE = Key("preheat_enable", bool)
    PREHEAT_OUTPUT = Key("preheat_output", float)
    """The preheater's output, in percent."""
    COOLING_ENABLE = Key("cooling_enable", bool)
    COMPRESSOR_PRIORITY = Key("compressor_priority", CompressorPriority)
    """What the compressor serves first."""

    # -------------------------------------------------------------------- hot water
    TEMP_HOTWATER_TOP = Key("temp_hotwater_top", float)
    """The top of the hot water tank, in °C."""
    TEMP_HOTWATER_BOTTOM = Key("temp_hotwater_bottom", float)
    """The bottom of the hot water tank, in °C."""
    TEMP_HOTWATER = Key("temp_hotwater", float)
    """The hot water temperature aimed for, in °C."""
    TEMP_HOTWATER_BOOST = Key("temp_hotwater_boost", float)
    """The hot water temperature, in °C, heated to electrically."""
    TEMP_HOTWATER_SCALD_PROTECTION = Key("temp_hotwater_scald_protection", float)
    """The scald protection temperature, in °C."""
    TEMP_HOTWATER_BYPASS_OFFSET = Key("temp_hotwater_bypass_offset", float)
    """The bypass offset for hot water, in °C; 0 for off."""
    HOTWATER_HEATER_ENABLE = Key("hotwater_heater_enable", bool)
    HOTWATER_SUPPLEMENT = Key("hotwater_supplement", HeatSource)
    """What supplements the heat pump for hot water."""
    ANTILEGIONELLA_DAY = Key("antilegionella_day", Weekday)
    """The day hot water is heated against legionella."""
    SACRIFICIAL_ANODE_OK = Key("sacrificial_anode_ok", bool)
    """False while the hot water tank's anode must be replaced."""

    # ---------------------------------------------------------------- central heating
    CENTRAL_HEAT_MODE = Key("central_heat_mode", CentralHeatMode)
    CENTRAL_HEAT_SOURCE = Key("central_heat_source", HeatSource)
    CENTRAL_HEAT_PUMP_MODE = Key("central_heat_pump_mode", CirculationPumpMode)
    CENTRAL_HEAT_CURVE = Key("central_heat_curve", int)
    """The outdoor temperature compensation curve, 1-10."""
    CENTRAL_HEAT_REGULATION_TIME = Key("central_heat_regulation_time", int)
    """The regulation's time, in seconds."""
    TEMP_CENTRAL_HEAT_SUPPLY = Key("temp_central_heat_supply", float)
    """Water supplied to the central heating, in °C."""
    TEMP_CENTRAL_HEAT_RETURN = Key("temp_central_heat_return", float)
    """Water returning from the central heating, in °C."""
    TEMP_CENTRAL_HEAT_SUPPLY_MIN = Key("temp_central_heat_supply_min", float)
    TEMP_CENTRAL_HEAT_SUPPLY_MAX = Key("temp_central_heat_supply_max", float)
    TEMP_CENTRAL_HEAT_OFFSET = Key("temp_central_heat_offset", float)
    """The central heating's offset from the room temperature target, in °C."""
    TEMP_CENTRAL_HEAT_COMPENSATION = Key("temp_central_heat_compensation", float)
    """The outdoor temperature compensation, in °C."""

    # -------------------------------------------------------------------- heat pump
    HEAT_PUMP_ACTIVE = Key("heat_pump_active", bool)
    HEAT_PUMP_HEATER_ACTIVE = Key("heat_pump_heater_active", bool)
    """Whether the heat pump's electric heater runs."""
    HEAT_PUMP_ROOM_HEATING = Key("heat_pump_room_heating", bool)
    HEAT_PUMP_WATER_HEATING = Key("heat_pump_water_heating", bool)
    HEAT_PUMP_STATE = Key("heat_pump_state", OperationState)
    """What the heat pump is doing."""
    HEAT_PUMP_CAPACITY = Key("heat_pump_capacity", float)
    """The heat pump's capacity, in percent."""
    TEMP_CONDENSER = Key("temp_condenser", float)
    """The condenser, in °C."""
    TEMP_EVAPORATOR = Key("temp_evaporator", float)
    """The evaporator, in °C."""
    TEMP_BEFORE_CONDENSER = Key("temp_before_condenser", float)
    TEMP_AFTER_CONDENSER = Key("temp_after_condenser", float)
    TEMP_PRESSURE_PIPE = Key("temp_pressure_pipe", float)
    """The compressor's pressure pipe, in °C."""
    TEMP_BUFFER_TANK = Key("temp_buffer_tank", float)
    TEMP_HEAT_PUMP_OUTDOOR = Key("temp_heat_pump_outdoor", float)
    SUCTION_PRESSURE = Key("suction_pressure", float)
    """The compressor's suction pressure, in bar."""
    DISCHARGE_PRESSURE = Key("discharge_pressure", float)
    """The compressor's discharge pressure, in bar."""

    # ------------------------------------------------------------------- air damper
    DAMPER_TEST_DAY = Key("damper_test_day", Weekday)
    """The day the air damper tests itself."""
    DAMPER_TEST_STATE = Key("damper_test_state", DamperTestState)
    DAMPER_TEST_LAST_DATE = Key("damper_test_last_date", date)
    """The day the air damper last tested itself, by the controller's clock."""

    @classmethod
    def all(cls) -> tuple[Key[Any], ...]:
        """Every key, in the order declared."""
        keys: list[Key[Any]] = [value for value in vars(cls).values() if isinstance(value, Key)]
        return tuple(keys)
