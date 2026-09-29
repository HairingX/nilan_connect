"""Nilan's CTS602 and CTS602 Light as models.

Sources:
    Nilan, "CTS 602 Modbus user manual" 3.00 (software 2.35), "Protocol description Nilan
    CTS602Light Modbus" version 20 and "Protocol description Nilan CTS602 with HMI350T Modbus"
    version 23, in this repository's docs/models: the registers, their scales and their groups.
    The gateway's addresses, the device variants and what each variant has were found in
    material published online; they are untested unless labelled `Source.TESTED`.

The gateway does not use the manuals' addresses. Within one of a manual's register groups -
blocks of 100, such as the temperatures from input register 200 - it keeps the manual's order and
spacing, so each point labelled `Source.CALCULATED` is placed from a known address in its group.
"""
from __future__ import annotations

from collections.abc import Mapping

from modbus_event_connect import DataType, Limits, Model, PollRate, Section, Unit
from modbus_event_connect.micro_nabto import MicroNabtoOptions

from ._model import (
    PointKey,
    Source,
    calculated,
    choice,
    command,
    labelled,
    reading,
    setting,
    slave_model_in,
    slave_model_not_in,
    state,
    switch,
    temperature,
)
from ._states import Alarm, HeatSource, OperationState

_SENSOR_ALARMS: Mapping[int, Alarm] = {
    **{25 + 2 * t: Alarm[f"SENSOR_T{t}_SHORT"] for t in range(1, 17)},
    **{26 + 2 * t: Alarm[f"SENSOR_T{t}_OPEN"] for t in range(1, 17)},
}

CTS602_ALARMS: Mapping[int, Alarm] = {
    0: Alarm.NONE, 1: Alarm.HARDWARE, 2: Alarm.TIMEOUT, 3: Alarm.FIRE, 4: Alarm.PRESSURE, 5: Alarm.DOOR_OPEN,
    6: Alarm.DEFROST_TIMEOUT_COMPRESSOR, 7: Alarm.AFTERHEAT_FROST, 8: Alarm.AFTERHEAT_FROST,
    9: Alarm.BOILER_OVERHEAT, 10: Alarm.REHEAT_OVERHEAT, 11: Alarm.REHEAT_NO_AIRFLOW, 12: Alarm.MOTOR_OVERHEAT,
    13: Alarm.WATER_BOILING, 14: Alarm.CONTROL_SENSOR_ERROR, 15: Alarm.ROOM_TEMPERATURE_LOW, 16: Alarm.SOFTWARE,
    17: Alarm.WATCHDOG, 18: Alarm.SETTINGS_CHANGED, 19: Alarm.CHANGE_FILTER, 20: Alarm.LEGIONELLA_NOT_DONE,
    21: Alarm.POWER_OUTAGE, 22: Alarm.AIR_TEMPERATURE_ERROR, 23: Alarm.WATER_TEMPERATURE_ERROR,
    24: Alarm.CENTRAL_HEAT_TEMPERATURE_ERROR, 25: Alarm.MODEM, 26: Alarm.NETWORK, **_SENSOR_ALARMS,
    70: Alarm.ANODE_WORN, 71: Alarm.DEFROST_TIMEOUT_EXCHANGER, 72: Alarm.EVAPORATOR_LOW, 90: Alarm.SLAVE_IO,
    91: Alarm.OPTIONS_MODULE_MISSING, 92: Alarm.PRESET_ERROR, 95: Alarm.SOFTWARE_REJECTED,
    96: Alarm.DAMPER_TEST_FAILED,
}
"""What each of a CTS602's alarm codes means (the CTS602 manual, pages 15-16). 7 and 8 are the same
frost alarm, on plants without and with a T9 sensor."""

CONTROL_STATES: Mapping[int, OperationState] = {state.value: state for state in OperationState if state.value <= 17}
"""A CTS602's control states: OperationState numbers them as the manual does."""

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


CTS602_SECTIONS: tuple[Section, ...] = (
    Section(labelled(Source.TESTED, (
        temperature(PointKey.TEMP_SUPPLY, 33, scale=0.01),
        temperature(PointKey.TEMP_EXHAUST, 35, scale=0.01),
        temperature(PointKey.TEMP_OUTSIDE, 39, scale=0.01),
    ))),
    Section(labelled(Source.TESTED, (
        temperature(PointKey.TEMP_EXTRACT, 34, scale=0.01),
    )), when=slave_model_in({2, 13, 27, 31})),
    Section(labelled(Source.UNTESTED, (
        temperature(PointKey.TEMP_CONDENSER, 36, scale=0.01),
        temperature(PointKey.TEMP_EVAPORATOR, 37, scale=0.01),
        temperature(PointKey.TEMP_SUPPLY_AFTER_HEATER, 38, scale=0.01),
        temperature(PointKey.TEMP_HEATER, 40, scale=0.01),
        temperature(PointKey.TEMP_ROOM, 41, scale=0.01),
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
        command(PointKey.FILTER_REPLACE_RESET, 71),
        setting(PointKey.FAN_LEVEL, 139, Limits(0, 4, step=1)),
        setting(PointKey.TEMP_TARGET, 140, Limits(0, 30, step=0.5), data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),
        setting(PointKey.FILTER_REPLACE_INTERVAL, 159, Limits(0, 365, step=1), unit=Unit.DAYS),
    ))),
    Section(labelled(Source.UNTESTED, (
        temperature(PointKey.TEMP_EXTRACT, 41, scale=0.01),
    )), when=slave_model_not_in({2, 13, 27, 31})),
    Section(labelled(Source.UNTESTED, (
        temperature(PointKey.TEMP_HOTWATER_TOP, 42, scale=0.01),
        temperature(PointKey.TEMP_HOTWATER_BOTTOM, 43, scale=0.01),
    )), when=slave_model_in({9, 10, 11, 12, 18, 19, 20, 21, 23, 30, 32, 34, 38, 43, 44, 144, 244})),
    Section(labelled(Source.UNTESTED, (
        temperature(PointKey.TEMP_CENTRAL_HEAT_RETURN, 44, scale=0.01),
        temperature(PointKey.TEMP_CENTRAL_HEAT_SUPPLY, 45, scale=0.01),
        choice(PointKey.CENTRAL_HEAT_MODE, 202),
        setting(PointKey.TEMP_CENTRAL_HEAT_SUPPLY_MIN, 203, Limits(0, 60, step=0.01), data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),
        setting(PointKey.TEMP_CENTRAL_HEAT_SUPPLY_MAX, 204, Limits(0, 60, step=0.01), data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),
        choice(PointKey.CENTRAL_HEAT_PUMP_MODE, 207),
        choice(PointKey.CENTRAL_HEAT_SOURCE, 208, codes=CENTRAL_HEAT_SOURCES),
    )), when=slave_model_in({20, 21, 23, 38, 43, 45, 244})),
    Section(labelled(Source.UNTESTED, (
        temperature(PointKey.TEMP_AFTER_CONDENSER, 57, scale=0.1),
        temperature(PointKey.TEMP_BEFORE_CONDENSER, 154, scale=0.1),
        temperature(PointKey.TEMP_HEAT_PUMP_OUTDOOR, 156, scale=0.1),
        state(PointKey.HEAT_PUMP_ACTIVE, 164),
        state(PointKey.HEAT_PUMP_HEATER_ACTIVE, 165),
        reading(PointKey.HEAT_PUMP_STATE, 198, codes=HEAT_PUMP_STATES),
        temperature(PointKey.TEMP_BUFFER_TANK, 252, scale=0.1),
        temperature(PointKey.TEMP_PRESSURE_PIPE, 256, scale=0.1),
        reading(PointKey.HEAT_PUMP_CAPACITY, 268, data_type=DataType.INT16, scale=0.1, unit=Unit.PERCENT),
    )), when=slave_model_in({44, 144, 244})),
    Section(labelled(Source.UNTESTED, (
        state(PointKey.SACRIFICIAL_ANODE_OK, 142),
    )), when=slave_model_in({9, 10, 11, 12, 18, 19, 20, 21, 23, 30, 34, 38, 43, 44, 144, 244})),
    Section(labelled(Source.UNTESTED, (
        choice(PointKey.OPERATION_MODE, 138),
    )), when=slave_model_not_in({23})),
    Section(labelled(Source.UNTESTED, (
        choice(PointKey.TEMP_COOLING_START_OFFSET, 170),
    )), when=slave_model_in({4, 9, 10, 12, 19, 21, 26, 30, 32, 33, 35, 36, 38, 39, 40, 41, 43, 44, 45, 144, 244})),
    Section(labelled(Source.UNTESTED, (
        setting(PointKey.TEMP_SUMMER_SUPPLY_MIN, 171, Limits(0, 40, step=0.01), data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),
        setting(PointKey.TEMP_SUMMER_SUPPLY_MAX, 173, Limits(0, 40, step=0.01), data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),
    )), when=slave_model_in({2, 4, 9, 10, 12, 13, 19, 21, 26, 30, 31, 32, 33, 34, 35, 36, 38, 39, 40, 41, 43, 44, 45, 144, 244})),
    Section(labelled(Source.UNTESTED, (
        setting(PointKey.TEMP_HOTWATER_BOOST, 189, Limits(20, 70, step=0.01), data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),
        setting(PointKey.TEMP_HOTWATER, 190, Limits(20, 70, step=0.01), data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),
    )), when=slave_model_in({9, 10, 11, 12, 13, 18, 19, 20, 21, 23, 30, 31, 32, 34, 38, 43, 44, 144, 244})),
    Section(labelled(Source.UNTESTED, (
        choice(PointKey.COMPRESSOR_PRIORITY, 191),
    )), when=slave_model_in({2, 9, 10, 12, 13, 30, 31, 32, 38, 43, 44, 144, 244})),
    Section(labelled(Source.UNTESTED, (
        choice(PointKey.ANTILEGIONELLA_DAY, 194),
    )), when=slave_model_in({3, 4, 9, 10, 11, 12, 18, 19, 20, 21, 23, 30, 32, 34, 38, 43, 44, 45, 144, 244})),
    Section(labelled(Source.UNTESTED, (
        switch(PointKey.REHEAT_ENABLE, 281),
    )), when=slave_model_in({2, 3, 4, 9, 10, 11, 12, 13, 18, 19, 20, 21, 23, 26, 27, 30, 31, 33, 34, 35, 36, 38, 39, 40, 41, 43, 44, 45, 144, 244})),
    Section(labelled(Source.CALCULATED, (
        calculated(PointKey.ENABLE, 137, setpoint=True, data_type=DataType.BOOL),  # HR 1001 Control.RunSet
        calculated(PointKey.SERVICE_MODE, 141, setpoint=True),  # HR 1005 Control.ServiceMode
        calculated(PointKey.SERVICE_CAPACITY, 142, setpoint=True, data_type=DataType.INT16, scale=0.01, unit=Unit.PERCENT),  # HR 1006 Control.ServicePct
        calculated(PointKey.AIR_EXCHANGE_MODE, 154, setpoint=True),  # HR 1100 AirFlow.AirExchMode
        calculated(PointKey.FAN_LEVEL_COOLING, 155, setpoint=True),  # HR 1101 AirFlow.CoolVent
        calculated(PointKey.DAMPER_TEST_DAY, 156, setpoint=True),  # HR 1102 AirFlow.TestSelect
        calculated(PointKey.DAMPER_TEST_LAST_DATE, 157, setpoint=True, data_type=DataType.DOS_DATE),  # HR 1103 AirFlow.LastTestDay
        calculated(PointKey.DAMPER_TEST_STATE, 158, setpoint=True),  # HR 1104 AirFlow.TestState
        calculated(PointKey.TEMP_WINTER_SUPPLY_MIN, 172, setpoint=True, data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),  # HR 1202 AirTemp.TempMinWin
        calculated(PointKey.TEMP_WINTER_SUPPLY_MAX, 174, setpoint=True, data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),  # HR 1204 AirTemp.TempMaxWin
        calculated(PointKey.TEMP_WINTER_MODE_THRESHOLD, 175, setpoint=True, data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),  # HR 1205 AirTemp.TempSummer
        calculated(PointKey.TEMP_NIGHT_COOLING_DAY_LIMIT, 176, setpoint=True, data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),  # HR 1206 AirTemp.NightDayLim
        calculated(PointKey.TEMP_NIGHT_COOLING_TARGET, 177, setpoint=True, data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),  # HR 1207 AirTemp.NightSet
        calculated(PointKey.CONTROL_SENSOR, 178, setpoint=True),  # HR 1208 AirTemp.SensorSelect
        calculated(PointKey.HEAT_SOURCE, 179, setpoint=True, codes=HEAT_SELECTS),  # HR 1209 AirTemp.HeatSelect
        calculated(PointKey.TEMP_HOTWATER_SCALD_PROTECTION, 192, setpoint=True, data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),  # HR 1703 HotWater.TempCprMax
        calculated(PointKey.HOTWATER_SUPPLEMENT, 193, setpoint=True, codes=HOT_WATER_SUPPLEMENTS),  # HR 1704 HotWater.HeatType
        calculated(PointKey.TEMP_HOTWATER_BYPASS_OFFSET, 195, setpoint=True, unit=Unit.CELSIUS),  # HR 1706 HotWater.TempPri
        calculated(PointKey.TEMP_CENTRAL_HEAT_OFFSET, 201, setpoint=True, data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),  # HR 1800 CentralHeat.HeatExtern
        calculated(PointKey.TEMP_CENTRAL_HEAT_COMPENSATION, 205, setpoint=True, data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),  # HR 1804 CentralHeat.SupplyOffset
        calculated(PointKey.CENTRAL_HEAT_CURVE, 206, setpoint=True),  # HR 1805 CentralHeat.CurveSelect
        calculated(PointKey.CENTRAL_HEAT_REGULATION_TIME, 209, setpoint=True),  # HR 1808 CentralHeat.RegTime
        calculated(PointKey.TEMP_CONTROLLER, 31, data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),  # IR 200 Input.T0_Controller
        calculated(PointKey.TEMP_INTAKE, 32, data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),  # IR 201 Input.T1_Intake
        calculated(PointKey.TEMP_ROOM_PANEL, 46, data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),  # IR 215 Input.T15_Room
        calculated(PointKey.TEMP_AUX, 47, data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),  # IR 216 Input.T16
        calculated(PointKey.TEMP_PREHEAT_INTAKE, 48, data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),  # IR 217 Input.T17
        # The manual gives these in bar without a scale; its group's other analogue inputs are
        # hundredths, so these are taken to be too.
        calculated(PointKey.SUCTION_PRESSURE, 50, data_type=DataType.INT16, scale=0.01, unit=Unit.BAR),  # IR 219 Input.pSuc
        calculated(PointKey.DISCHARGE_PRESSURE, 51, data_type=DataType.INT16, scale=0.01, unit=Unit.BAR),  # IR 220 Input.pDis
        calculated(PointKey.ALARM_STATUS, 64, data_type=DataType.bit(7)),  # IR 400 Alarm.Status
        calculated(PointKey.ALARM_1_TIME, 66, data_type=DataType.DOS_DATETIME),  # IR 402-403 Alarm.List_1_Date, _Time
        calculated(PointKey.ALARM_2_TIME, 69, data_type=DataType.DOS_DATETIME),  # IR 405-406 Alarm.List_2_Date, _Time
        calculated(PointKey.ALARM_3_TIME, 72, data_type=DataType.DOS_DATETIME),  # IR 408-409 Alarm.List_3_Date, _Time
        calculated(PointKey.RUNNING, 84, data_type=DataType.BOOL),  # IR 1000 Control.RunAct
        calculated(PointKey.OPERATION_MODE_CURRENT, 85),  # IR 1001 Control.ModeAct
        calculated(PointKey.TIME_IN_STATE, 87, unit=Unit.SECONDS),  # IR 1003 Control.SecInState
        calculated(PointKey.FAN_LEVEL_CURRENT, 98),  # IR 1100 AirFlow.VentSet
        calculated(PointKey.FILTER_REPLACE_TIME_AGO, 101, unit=Unit.DAYS),  # IR 1103 AirFlow.SinceFiltDay
    ))),
    Section(labelled(Source.CALCULATED, (
        calculated(PointKey.TEMP_PRESSURE_PIPE, 49, data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),  # IR 218 Input.T18_PresPibe
    )), when=slave_model_not_in({44, 144, 244})),
)

CTS602 = Model(
    "CTS 602", "Nilan", CTS602_SECTIONS,
    options=MicroNabtoOptions(),
    poll_intervals={PollRate.FAST: 10.0, PollRate.SLOW: 180.0},
    read_back_after=1.0,
)


CTS602_LIGHT_SECTIONS: tuple[Section, ...] = (
    Section(labelled(Source.UNTESTED, (
        temperature(PointKey.TEMP_EXTRACT, 33, scale=0.01),
        temperature(PointKey.TEMP_EXHAUST, 34, scale=0.01),
        temperature(PointKey.TEMP_SUPPLY, 37, scale=0.01),
        temperature(PointKey.TEMP_OUTSIDE, 38, scale=0.01),
        temperature(PointKey.TEMP_HEATER, 39, scale=0.01),
        reading(PointKey.HUMIDITY, 51, data_type=DataType.INT16, scale=0.01, unit=Unit.PERCENT),
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
        command(PointKey.FILTER_REPLACE_RESET, 67),
        setting(PointKey.FAN_LEVEL, 135, Limits(0, 4, step=1)),
        setting(PointKey.TEMP_TARGET, 136, Limits(0, 30, step=0.5), data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),
        setting(PointKey.FILTER_REPLACE_INTERVAL, 153, Limits(0, 365, step=1), unit=Unit.DAYS),
    ))),
    Section(labelled(Source.CALCULATED, (
        calculated(PointKey.ENABLE, 133, setpoint=True, data_type=DataType.BOOL),  # HR 1001 Control.RunSet
        calculated(PointKey.OPERATION_MODE, 134, setpoint=True),  # HR 1002 Control.ModeSet
        calculated(PointKey.SERVICE_MODE, 137, setpoint=True),  # HR 1005 Control.ServiceMode
        calculated(PointKey.SERVICE_CAPACITY, 138, setpoint=True, data_type=DataType.INT16, scale=0.01, unit=Unit.PERCENT),  # HR 1006 Control.ServicePct
        calculated(PointKey.DAMPER_TEST_DAY, 150, setpoint=True),  # HR 1102 AirFlow.TestSelect
        calculated(PointKey.DAMPER_TEST_LAST_DATE, 151, setpoint=True, data_type=DataType.DOS_DATE),  # HR 1103 AirFlow.LastTestDay
        calculated(PointKey.DAMPER_TEST_STATE, 152, setpoint=True),  # HR 1104 AirFlow.TestState
        calculated(PointKey.TEMP_CONTROLLER, 30, data_type=DataType.INT16, scale=0.01, unit=Unit.CELSIUS),  # IR 200 Input.T0_Controller
        calculated(PointKey.ALARM_STATUS, 63, data_type=DataType.bit(7)),  # IR 400 Alarm.Status
        calculated(PointKey.ALARM_1_TIME, 65, data_type=DataType.DOS_DATETIME),  # IR 402-403 Alarm.List_1_Date, _Time
        calculated(PointKey.ALARM_2_TIME, 68, data_type=DataType.DOS_DATETIME),  # IR 405-406 Alarm.List_2_Date, _Time
        calculated(PointKey.ALARM_3_TIME, 71, data_type=DataType.DOS_DATETIME),  # IR 408-409 Alarm.List_3_Date, _Time
        calculated(PointKey.RUNNING, 83, data_type=DataType.BOOL),  # IR 1000 Control.RunAct
        calculated(PointKey.OPERATION_MODE_CURRENT, 84),  # IR 1001 Control.ModeAct
        calculated(PointKey.TIME_IN_STATE, 86, unit=Unit.SECONDS),  # IR 1003 Control.SecInState
        calculated(PointKey.FAN_LEVEL_CURRENT, 97),  # IR 1100 AirFlow.VentSet
        calculated(PointKey.FILTER_REPLACE_TIME_AGO, 100, unit=Unit.DAYS),  # IR 1103 AirFlow.SinceFiltDay
    ))),
)

CTS602_LIGHT = Model(
    "CTS 602 Light", "Nilan", CTS602_LIGHT_SECTIONS,
    options=MicroNabtoOptions(),
    poll_intervals={PollRate.FAST: 10.0, PollRate.SLOW: 180.0},
    read_back_after=1.0,
)
