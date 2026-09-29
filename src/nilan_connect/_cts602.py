"""Nilan's CTS602 and CTS602 Light as models.

Sources:
    Nilan, "CTS 602 Modbus user manual" 3.00 (software 2.35), "Protocol description Nilan
    CTS602Light Modbus" version 20 and "Protocol description Nilan CTS602 with HMI350T Modbus"
    version 23, in this repository's docs/models: the registers, their scales and their groups.
    The gateway's addresses and the device variants were found in material published online.

The gateway does not use the manuals' addresses. Within one of a manual's register groups -
blocks of 100, such as the temperatures from input register 200 - it keeps the manual's order and
spacing, so an inferred point is placed from a known address in its group; its comment names the
manual's register.
"""
from __future__ import annotations

from collections.abc import Mapping

from modbus_event_connect import DataType, Key, Limits, Point, Unit

from ._certainty import section
from ._keys import PointKey
from ._points import (
    alarm_bit,
    choice,
    fan_level_rereads,
    nilan_model,
    reading,
    setpoint_reading,
    setting,
    slave_model_in,
    slave_model_not_in,
    state,
    switch,
    temperature,
)
from ._states import Alarm, HeatSource, OperationState

# The device variants - the handshake's slave device model - that have each part, as found in
# material published online.
WITH_EXTRACT_AT_T3 = frozenset({2, 13, 27, 31})
"""The variants whose extract air is sensor T3; the others' is T10."""
WITH_HOT_WATER_SENSORS = frozenset({9, 10, 11, 12, 18, 19, 20, 21, 23, 30, 32, 34, 38, 43, 44, 144, 244})
WITH_HOT_WATER_SETTINGS = frozenset({9, 10, 11, 12, 13, 18, 19, 20, 21, 23, 30, 31, 32, 34, 38, 43, 44, 144, 244})
WITH_SACRIFICIAL_ANODE = frozenset({9, 10, 11, 12, 18, 19, 20, 21, 23, 30, 34, 38, 43, 44, 144, 244})
WITH_ANTILEGIONELLA = frozenset({3, 4, 9, 10, 11, 12, 18, 19, 20, 21, 23, 30, 32, 34, 38, 43, 44, 45, 144, 244})
WITH_CENTRAL_HEATING = frozenset({20, 21, 23, 38, 43, 45, 244})
WITH_HEAT_PUMP_READINGS = frozenset({44, 144, 244})
WITH_COOLING_OFFSET = frozenset({4, 9, 10, 12, 19, 21, 26, 30, 32, 33, 35, 36, 38, 39, 40, 41, 43, 44, 45, 144,
                                 244})
WITH_SUMMER_SUPPLY_LIMITS = frozenset({2, 4, 9, 10, 12, 13, 19, 21, 26, 30, 31, 32, 33, 34, 35, 36, 38, 39, 40, 41,
                                       43, 44, 45, 144, 244})
WITH_COMPRESSOR_PRIORITY = frozenset({2, 9, 10, 12, 13, 30, 31, 32, 38, 43, 44, 144, 244})
WITH_REHEATING = frozenset({2, 3, 4, 9, 10, 11, 12, 13, 18, 19, 20, 21, 23, 26, 27, 30, 31, 33, 34, 35, 36, 38, 39,
                            40, 41, 43, 44, 45, 144, 244})
WITHOUT_OPERATION_MODE = frozenset({23})

CTS602_ALARMS: Mapping[int, Alarm] = {
    0: Alarm.NONE, 1: Alarm.HARDWARE, 2: Alarm.TIMEOUT, 3: Alarm.FIRE, 4: Alarm.PRESSURE, 5: Alarm.DOOR_OPEN,
    6: Alarm.DEFROST_TIMEOUT_COMPRESSOR, 7: Alarm.AFTERHEAT_FROST, 8: Alarm.AFTERHEAT_FROST,
    9: Alarm.BOILER_OVERHEAT, 10: Alarm.REHEAT_OVERHEAT, 11: Alarm.REHEAT_NO_AIRFLOW, 12: Alarm.MOTOR_OVERHEAT,
    13: Alarm.WATER_BOILING, 14: Alarm.CONTROL_SENSOR_ERROR, 15: Alarm.ROOM_TEMPERATURE_LOW, 16: Alarm.SOFTWARE,
    17: Alarm.WATCHDOG, 18: Alarm.SETTINGS_CHANGED, 19: Alarm.CHANGE_FILTER, 20: Alarm.LEGIONELLA_NOT_DONE,
    21: Alarm.POWER_OUTAGE, 22: Alarm.AIR_TEMPERATURE_ERROR, 23: Alarm.WATER_TEMPERATURE_ERROR,
    24: Alarm.CENTRAL_HEAT_TEMPERATURE_ERROR, 25: Alarm.MODEM, 26: Alarm.NETWORK,
    27: Alarm.SENSOR_T1_SHORT, 28: Alarm.SENSOR_T1_OPEN, 29: Alarm.SENSOR_T2_SHORT, 30: Alarm.SENSOR_T2_OPEN,
    31: Alarm.SENSOR_T3_SHORT, 32: Alarm.SENSOR_T3_OPEN, 33: Alarm.SENSOR_T4_SHORT, 34: Alarm.SENSOR_T4_OPEN,
    35: Alarm.SENSOR_T5_SHORT, 36: Alarm.SENSOR_T5_OPEN, 37: Alarm.SENSOR_T6_SHORT, 38: Alarm.SENSOR_T6_OPEN,
    39: Alarm.SENSOR_T7_SHORT, 40: Alarm.SENSOR_T7_OPEN, 41: Alarm.SENSOR_T8_SHORT, 42: Alarm.SENSOR_T8_OPEN,
    43: Alarm.SENSOR_T9_SHORT, 44: Alarm.SENSOR_T9_OPEN, 45: Alarm.SENSOR_T10_SHORT, 46: Alarm.SENSOR_T10_OPEN,
    47: Alarm.SENSOR_T11_SHORT, 48: Alarm.SENSOR_T11_OPEN, 49: Alarm.SENSOR_T12_SHORT, 50: Alarm.SENSOR_T12_OPEN,
    51: Alarm.SENSOR_T13_SHORT, 52: Alarm.SENSOR_T13_OPEN, 53: Alarm.SENSOR_T14_SHORT, 54: Alarm.SENSOR_T14_OPEN,
    55: Alarm.SENSOR_T15_SHORT, 56: Alarm.SENSOR_T15_OPEN, 57: Alarm.SENSOR_T16_SHORT, 58: Alarm.SENSOR_T16_OPEN,
    70: Alarm.ANODE_WORN, 71: Alarm.DEFROST_TIMEOUT_EXCHANGER, 72: Alarm.EVAPORATOR_LOW, 90: Alarm.SLAVE_IO,
    91: Alarm.OPTIONS_MODULE_MISSING, 92: Alarm.PRESET_ERROR, 95: Alarm.SOFTWARE_REJECTED,
    96: Alarm.DAMPER_TEST_FAILED,
}
"""What each of a CTS602's alarm codes means (the CTS602 manual, pages 15-16). 7 and 8 are the same
frost alarm, on plants without and with a T9 sensor."""

CONTROL_STATES: Mapping[int, OperationState] = {
    0: OperationState.OFF, 1: OperationState.SHIFT, 2: OperationState.STOP, 3: OperationState.START,
    4: OperationState.STANDBY, 5: OperationState.VENTILATION_STOP, 6: OperationState.VENTILATION,
    7: OperationState.HEATING, 8: OperationState.COOLING, 9: OperationState.HOT_WATER, 10: OperationState.LEGIONELLA,
    11: OperationState.COOLING_HOT_WATER, 12: OperationState.CENTRAL_HEATING, 13: OperationState.DEFROST,
    14: OperationState.FROST_PROTECTION, 15: OperationState.SERVICE, 16: OperationState.ALARM,
    17: OperationState.HEATING_HOT_WATER,
}
"""What each of a CTS602's control states means (IR 1002 Control.State)."""

HEAT_PUMP_STATES: Mapping[int, OperationState] = {
    0: OperationState.OFF, 1: OperationState.READY, 2: OperationState.HOT_WATER_START_UP, 3: OperationState.HOT_WATER,
    4: OperationState.HEATING_START_UP, 5: OperationState.HEATING, 6: OperationState.HEAT_PUMP_STOP,
    7: OperationState.ELECTRIC_HEATING, 8: OperationState.ELECTRIC_HOT_WATER, 9: OperationState.FORCED_COLD_PUMP,
    10: OperationState.HEAT_PUMP_STOP, 11: OperationState.DEFROST, 12: OperationState.AIR_DEFROST,
    13: OperationState.HOTGAS_DEFROST, 14: OperationState.DRIP_DELAY, 15: OperationState.HOT_WATER_HEAT_PUMP_STOP,
    16: OperationState.HEATING_HEAT_PUMP_STOP, 17: OperationState.STOP, 18: OperationState.HEATING_HEAT_PUMP_STOP,
    19: OperationState.HOT_WATER_HEAT_PUMP_STOP, 20: OperationState.PUMP_EXERCISE, 21: OperationState.FORCED_START_UP,
    22: OperationState.FORCED_RUNNING, 23: OperationState.FORCED_RUNNING,
    24: OperationState.FORCED_RUNNING_HEAT_PUMP_STOP, 25: OperationState.MANUAL, 26: OperationState.COOLING_START_UP,
    27: OperationState.COOLING, 28: OperationState.EXTERNAL_STOP, 29: OperationState.FORCED_LOW_SPEED,
}
"""What each of a heat pump's states means, as found in material published online; several share a text."""

HEAT_SELECTS: Mapping[int, HeatSource] = {
    0: HeatSource.OFF, 1: HeatSource.HEAT_PUMP, 2: HeatSource.HEAT_PUMP_THEN_AFTERHEAT, 3: HeatSource.AFTERHEAT,
    4: HeatSource.AFTERHEAT_THEN_HEAT_PUMP,
}
"""AirTemp.HeatSelect: "0=No heating active, 1=Heatpump only, 2=HP+afterheat, 3=Afterheat only,
4=Afterheat+HP"."""

CENTRAL_HEAT_SOURCES: Mapping[int, HeatSource] = {
    0: HeatSource.OFF, 1: HeatSource.ELECTRIC, 2: HeatSource.HEAT_PUMP, 3: HeatSource.HEAT_PUMP_THEN_ELECTRIC,
}
"""CentralHeat.HeatType: "0=OFF, 1=El, 2=Heatpump, 3=Both (first compressor then electric priority)"."""

HOT_WATER_SUPPLEMENTS: Mapping[int, HeatSource] = {0: HeatSource.OFF, 1: HeatSource.ELECTRIC}
"""HotWater.HeatType: "Use of electricity supplement: 0=OFF, 1=El"."""


def cts602_temperature(key: Key[float], address: int) -> Point[float]:
    """A datapoint holding a temperature in hundredths of a °C."""
    return temperature(key, address, scale=0.01)


def cts602_temperature_setting(key: Key[float], address: int, limits: Limits | None = None) -> Point[float]:
    """A setpoint holding a temperature in hundredths of a °C."""
    return setting(key, address, limits, data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS)


_CTS602_FAN_LEVEL_REREADS = fan_level_rereads(
    PointKey.FAN_LEVEL_CURRENT, PointKey.FAN_LEVEL_SUPPLY, PointKey.FAN_LEVEL_EXTRACT)


CTS602_SECTIONS = (
    section(
        verified=(
            cts602_temperature(PointKey.TEMP_SUPPLY, 33),
            cts602_temperature(PointKey.TEMP_EXHAUST, 35),
            cts602_temperature(PointKey.TEMP_OUTSIDE, 39),
        ),
        reported=(
            cts602_temperature(PointKey.TEMP_CONDENSER, 36),
            cts602_temperature(PointKey.TEMP_EVAPORATOR, 37),
            cts602_temperature(PointKey.TEMP_SUPPLY_AFTER_HEATER, 38),
            cts602_temperature(PointKey.TEMP_HEATER, 40),
            cts602_temperature(PointKey.TEMP_ROOM, 41),
            reading(PointKey.HUMIDITY, 52, data_type=DataType.INT16, scale=0.01, unit=Unit.PERCENT),
            reading(PointKey.CO2_LEVEL, 53, data_type=DataType.INT16, unit=Unit.PPM),
            reading(PointKey.ALARM_1_CODE, 65),
            reading(PointKey.ALARM_2_CODE, 68),
            reading(PointKey.ALARM_3_CODE, 71),
            reading(PointKey.ALARM_1, 65, codes=CTS602_ALARMS),
            reading(PointKey.ALARM_2, 68, codes=CTS602_ALARMS),
            reading(PointKey.ALARM_3, 71, codes=CTS602_ALARMS),
            reading(PointKey.STATE_CODE, 86),
            reading(PointKey.OPERATION_STATE, 86, codes=CONTROL_STATES),
            reading(PointKey.FAN_LEVEL_SUPPLY, 99, data_type=DataType.INT16),
            reading(PointKey.FAN_LEVEL_EXTRACT, 100, data_type=DataType.INT16),
            reading(PointKey.FILTER_REPLACE_TIME_REMAIN, 102, data_type=DataType.INT16, unit=Unit.DAYS),
            state(PointKey.BYPASS_ACTIVE, 187),
            setting(PointKey.FAN_LEVEL, 139, Limits(0, 4, step=1), on_write=_CTS602_FAN_LEVEL_REREADS),
            cts602_temperature_setting(PointKey.TEMP_TARGET, 140, Limits(0, 30, step=0.5)),
            setting(PointKey.FILTER_REPLACE_INTERVAL, 159, Limits(0, 365, step=1), unit=Unit.DAYS),
        ),
        inferred=(
            cts602_temperature(PointKey.TEMP_CONTROLLER, 31),                      # IR 200 Input.T0_Controller
            cts602_temperature(PointKey.TEMP_INTAKE, 32),                          # IR 201 Input.T1_Intake
            cts602_temperature(PointKey.TEMP_ROOM_PANEL, 46),                      # IR 215 Input.T15_Room
            cts602_temperature(PointKey.TEMP_AUX, 47),                             # IR 216 Input.T16
            cts602_temperature(PointKey.TEMP_PREHEAT_INTAKE, 48),                  # IR 217 Input.T17
            # The manual gives the pressures in bar without a scale; its group's other analogue
            # inputs are hundredths, so these are taken to be too.
            reading(PointKey.SUCTION_PRESSURE, 50, data_type=DataType.INT16, scale=0.01,
                    unit=Unit.BAR),                                                # IR 219 Input.pSuc
            reading(PointKey.DISCHARGE_PRESSURE, 51, data_type=DataType.INT16, scale=0.01,
                    unit=Unit.BAR),                                                # IR 220 Input.pDis
            alarm_bit(PointKey.ALARM_STATUS, 64, 7),                               # IR 400 Alarm.Status
            reading(PointKey.ALARM_1_TIME, 66, data_type=DataType.DOS_DATETIME),   # IR 402-403 Alarm.List_1_Date, _Time
            reading(PointKey.ALARM_2_TIME, 69, data_type=DataType.DOS_DATETIME),   # IR 405-406 Alarm.List_2_Date, _Time
            reading(PointKey.ALARM_3_TIME, 72, data_type=DataType.DOS_DATETIME),   # IR 408-409 Alarm.List_3_Date, _Time
            state(PointKey.RUNNING, 84),                                           # IR 1000 Control.RunAct
            reading(PointKey.OPERATION_MODE_CURRENT, 85),                          # IR 1001 Control.ModeAct
            reading(PointKey.TIME_IN_STATE, 87, unit=Unit.SECONDS),                # IR 1003 Control.SecInState
            reading(PointKey.FAN_LEVEL_CURRENT, 98),                               # IR 1100 AirFlow.VentSet
            reading(PointKey.FILTER_REPLACE_TIME_AGO, 101, unit=Unit.DAYS),        # IR 1103 AirFlow.SinceFiltDay
            switch(PointKey.ENABLE, 137),                                          # HR 1001 Control.RunSet
            choice(PointKey.SERVICE_MODE, 141),                                    # HR 1005 Control.ServiceMode
            setting(PointKey.SERVICE_CAPACITY, 142, None, data_type=DataType.INT16, scale=0.01,
                    unit=Unit.PERCENT),                                            # HR 1006 Control.ServicePct
            choice(PointKey.AIR_EXCHANGE_MODE, 154),                               # HR 1100 AirFlow.AirExchMode
            setting(PointKey.FAN_LEVEL_COOLING, 155, None),                        # HR 1101 AirFlow.CoolVent
            setpoint_reading(PointKey.DAMPER_TEST_LAST_DATE, 157,
                             data_type=DataType.DOS_DATE),                         # HR 1103 AirFlow.LastTestDay
            setpoint_reading(PointKey.DAMPER_TEST_STATE, 158),                     # HR 1104 AirFlow.TestState
            cts602_temperature_setting(PointKey.TEMP_WINTER_SUPPLY_MIN, 172),      # HR 1202 AirTemp.TempMinWin
            cts602_temperature_setting(PointKey.TEMP_WINTER_SUPPLY_MAX, 174),      # HR 1204 AirTemp.TempMaxWin
            cts602_temperature_setting(PointKey.TEMP_WINTER_MODE_THRESHOLD, 175),  # HR 1205 AirTemp.TempSummer
            # "[0:Off, 20..40]" is not one range.
            cts602_temperature_setting(PointKey.TEMP_NIGHT_COOLING_DAY_LIMIT, 176),  # HR 1206 AirTemp.NightDayLim
            cts602_temperature_setting(PointKey.TEMP_NIGHT_COOLING_TARGET, 177,
                                       Limits(10, 30)),                            # HR 1207 AirTemp.NightSet
            choice(PointKey.CONTROL_SENSOR, 178),                                  # HR 1208 AirTemp.SensorSelect
            choice(PointKey.HEAT_SOURCE, 179, codes=HEAT_SELECTS),                 # HR 1209 AirTemp.HeatSelect
            cts602_temperature_setting(PointKey.TEMP_HOTWATER_SCALD_PROTECTION, 192),  # HR 1703 HotWater.TempCprMax
            choice(PointKey.HOTWATER_SUPPLEMENT, 193, codes=HOT_WATER_SUPPLEMENTS),  # HR 1704 HotWater.HeatType
            setting(PointKey.TEMP_HOTWATER_BYPASS_OFFSET, 195, Limits(0, 30, step=1),
                    unit=Unit.CELSIUS),                                            # HR 1706 HotWater.TempPri
            cts602_temperature_setting(PointKey.TEMP_CENTRAL_HEAT_OFFSET, 201),    # HR 1800 CentralHeat.HeatExtern
            cts602_temperature_setting(PointKey.TEMP_CENTRAL_HEAT_COMPENSATION,
                                       205),                                       # HR 1804 CentralHeat.SupplyOffset
            setting(PointKey.CENTRAL_HEAT_CURVE, 206, Limits(1, 10, step=1)),      # HR 1805 CentralHeat.CurveSelect
            setting(PointKey.CENTRAL_HEAT_REGULATION_TIME, 209, Limits(0, 25, step=1),
                    unit=Unit.SECONDS),                                            # HR 1808 CentralHeat.RegTime
        ),
    ),
    section(when=slave_model_in(WITH_EXTRACT_AT_T3), verified=(
        cts602_temperature(PointKey.TEMP_EXTRACT, 34),
    )),
    section(when=slave_model_not_in(WITH_EXTRACT_AT_T3), reported=(
        cts602_temperature(PointKey.TEMP_EXTRACT, 41),
    )),
    section(when=slave_model_in(WITH_HOT_WATER_SENSORS), reported=(
        cts602_temperature(PointKey.TEMP_HOTWATER_TOP, 42),
        cts602_temperature(PointKey.TEMP_HOTWATER_BOTTOM, 43),
    )),
    section(when=slave_model_in(WITH_CENTRAL_HEATING), reported=(
        cts602_temperature(PointKey.TEMP_CENTRAL_HEAT_RETURN, 44),
        cts602_temperature(PointKey.TEMP_CENTRAL_HEAT_SUPPLY, 45),
        choice(PointKey.CENTRAL_HEAT_MODE, 202),
        cts602_temperature_setting(PointKey.TEMP_CENTRAL_HEAT_SUPPLY_MIN, 203, Limits(0, 60, step=0.01)),
        cts602_temperature_setting(PointKey.TEMP_CENTRAL_HEAT_SUPPLY_MAX, 204, Limits(0, 60, step=0.01)),
        choice(PointKey.CENTRAL_HEAT_PUMP_MODE, 207),
        choice(PointKey.CENTRAL_HEAT_SOURCE, 208, codes=CENTRAL_HEAT_SOURCES),
    )),
    section(when=slave_model_in(WITH_HEAT_PUMP_READINGS), reported=(
        temperature(PointKey.TEMP_AFTER_CONDENSER, 57, scale=0.1),
        temperature(PointKey.TEMP_BEFORE_CONDENSER, 154, scale=0.1),
        temperature(PointKey.TEMP_HEAT_PUMP_OUTDOOR, 156, scale=0.1),
        state(PointKey.HEAT_PUMP_ACTIVE, 164),
        state(PointKey.HEAT_PUMP_HEATER_ACTIVE, 165),
        reading(PointKey.HEAT_PUMP_STATE, 198, codes=HEAT_PUMP_STATES),
        temperature(PointKey.TEMP_BUFFER_TANK, 252, scale=0.1),
        temperature(PointKey.TEMP_PRESSURE_PIPE, 256, scale=0.1),
        reading(PointKey.HEAT_PUMP_CAPACITY, 268, data_type=DataType.INT16, scale=0.1, unit=Unit.PERCENT),
    )),
    section(when=slave_model_not_in(WITH_HEAT_PUMP_READINGS), inferred=(
        cts602_temperature(PointKey.TEMP_PRESSURE_PIPE, 49),                       # IR 218 Input.T18_PresPibe
    )),
    section(when=slave_model_in(WITH_SACRIFICIAL_ANODE), reported=(
        state(PointKey.SACRIFICIAL_ANODE_OK, 142),
    )),
    section(when=slave_model_not_in(WITHOUT_OPERATION_MODE), reported=(
        choice(PointKey.OPERATION_MODE, 138),
    )),
    section(when=slave_model_in(WITH_COOLING_OFFSET), reported=(
        choice(PointKey.TEMP_COOLING_START_OFFSET, 170),
    )),
    section(when=slave_model_in(WITH_SUMMER_SUPPLY_LIMITS), reported=(
        cts602_temperature_setting(PointKey.TEMP_SUMMER_SUPPLY_MIN, 171, Limits(0, 40, step=0.01)),
        cts602_temperature_setting(PointKey.TEMP_SUMMER_SUPPLY_MAX, 173, Limits(0, 40, step=0.01)),
    )),
    section(when=slave_model_in(WITH_HOT_WATER_SETTINGS), reported=(
        cts602_temperature_setting(PointKey.TEMP_HOTWATER_BOOST, 189, Limits(20, 70, step=0.01)),
        cts602_temperature_setting(PointKey.TEMP_HOTWATER, 190, Limits(20, 70, step=0.01)),
    )),
    section(when=slave_model_in(WITH_COMPRESSOR_PRIORITY), reported=(
        choice(PointKey.COMPRESSOR_PRIORITY, 191),
    )),
    section(when=slave_model_in(WITH_ANTILEGIONELLA), reported=(
        choice(PointKey.ANTILEGIONELLA_DAY, 194),
    )),
    section(when=slave_model_in(WITH_REHEATING), reported=(
        switch(PointKey.REHEAT_ENABLE, 281),
    )),
)

CTS602 = nilan_model("CTS 602", "Nilan", CTS602_SECTIONS)


CTS602_LIGHT_SECTIONS = (
    section(
        reported=(
            cts602_temperature(PointKey.TEMP_EXTRACT, 33),
            cts602_temperature(PointKey.TEMP_EXHAUST, 34),
            cts602_temperature(PointKey.TEMP_SUPPLY, 37),
            cts602_temperature(PointKey.TEMP_OUTSIDE, 38),
            cts602_temperature(PointKey.TEMP_HEATER, 39),
            reading(PointKey.HUMIDITY, 51, data_type=DataType.INT16, scale=0.01, unit=Unit.PERCENT),
            # By its group, IR 222 AirQual.CO2 would be at 52; the address found published is 53.
            reading(PointKey.CO2_LEVEL, 53, data_type=DataType.INT16, unit=Unit.PPM),
            reading(PointKey.ALARM_1_CODE, 64),
            reading(PointKey.ALARM_2_CODE, 67),
            reading(PointKey.ALARM_3_CODE, 70),
            reading(PointKey.ALARM_1, 64, codes=CTS602_ALARMS),
            reading(PointKey.ALARM_2, 67, codes=CTS602_ALARMS),
            reading(PointKey.ALARM_3, 70, codes=CTS602_ALARMS),
            reading(PointKey.STATE_CODE, 85),
            reading(PointKey.OPERATION_STATE, 85, codes=CONTROL_STATES),
            reading(PointKey.FAN_LEVEL_SUPPLY, 98, data_type=DataType.INT16),
            reading(PointKey.FAN_LEVEL_EXTRACT, 99, data_type=DataType.INT16),
            reading(PointKey.FILTER_REPLACE_TIME_REMAIN, 101, data_type=DataType.INT16, unit=Unit.DAYS),
            state(PointKey.BYPASS_ACTIVE, 129),
            setting(PointKey.FAN_LEVEL, 135, Limits(0, 4, step=1), on_write=_CTS602_FAN_LEVEL_REREADS),
            cts602_temperature_setting(PointKey.TEMP_TARGET, 136, Limits(0, 30, step=0.5)),
            setting(PointKey.FILTER_REPLACE_INTERVAL, 153, Limits(0, 365, step=1), unit=Unit.DAYS),
        ),
        inferred=(
            cts602_temperature(PointKey.TEMP_CONTROLLER, 30),                      # IR 200 Input.T0_Controller
            alarm_bit(PointKey.ALARM_STATUS, 63, 7),                               # IR 400 Alarm.Status
            reading(PointKey.ALARM_1_TIME, 65, data_type=DataType.DOS_DATETIME),   # IR 402-403 Alarm.List_1_Date, _Time
            reading(PointKey.ALARM_2_TIME, 68, data_type=DataType.DOS_DATETIME),   # IR 405-406 Alarm.List_2_Date, _Time
            reading(PointKey.ALARM_3_TIME, 71, data_type=DataType.DOS_DATETIME),   # IR 408-409 Alarm.List_3_Date, _Time
            state(PointKey.RUNNING, 83),                                           # IR 1000 Control.RunAct
            reading(PointKey.OPERATION_MODE_CURRENT, 84),                          # IR 1001 Control.ModeAct
            reading(PointKey.TIME_IN_STATE, 86, unit=Unit.SECONDS),                # IR 1003 Control.SecInState
            reading(PointKey.FAN_LEVEL_CURRENT, 97),                               # IR 1100 AirFlow.VentSet
            reading(PointKey.FILTER_REPLACE_TIME_AGO, 100, unit=Unit.DAYS),        # IR 1103 AirFlow.SinceFiltDay
            switch(PointKey.ENABLE, 133),                                          # HR 1001 Control.RunSet
            choice(PointKey.OPERATION_MODE, 134),                                  # HR 1002 Control.ModeSet
            choice(PointKey.SERVICE_MODE, 137),                                    # HR 1005 Control.ServiceMode
            setting(PointKey.SERVICE_CAPACITY, 138, None, data_type=DataType.INT16, scale=0.01,
                    unit=Unit.PERCENT),                                            # HR 1006 Control.ServicePct
            # The manual: once chosen, the weekly self-test cannot be turned off again.
            setpoint_reading(PointKey.DAMPER_TEST_DAY, 150),                       # HR 1102 AirFlow.TestSelect
            setpoint_reading(PointKey.DAMPER_TEST_LAST_DATE, 151,
                             data_type=DataType.DOS_DATE),                         # HR 1103 AirFlow.LastTestDay
            setpoint_reading(PointKey.DAMPER_TEST_STATE, 152),                     # HR 1104 AirFlow.TestState
        ),
    ),
)

CTS602_LIGHT = nilan_model("CTS 602 Light", "Nilan", CTS602_LIGHT_SECTIONS)
