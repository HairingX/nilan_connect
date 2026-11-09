"""Nilan's CTS602 Light as a model, and how it is talked to over micro_nabto.

Sources:
    Nilan, "Protocol description Nilan CTS602Light Modbus" version 20, in this repository's
    docs/models: the registers, their scales and their groups. The gateway's addresses were found
    in material published online; within one of the manual's register groups the gateway keeps
    the manual's order and spacing, so an inferred point is placed from a known address in its
    group, and its comment names the manual's register.
"""
from __future__ import annotations

from modbus_event_connect import DataType, Limits, Model, Unit
from modbus_event_connect.micro_nabto import MicroNabtoProfile

from ._cts602 import (
    CONTROL_STATES,
    CTS602_ALARMS,
    CTS602_FAN_LEVEL_REREADS,
    FILTER_INTERVALS,
    cts602_temperature,
    cts602_temperature_setting,
)
from ._keys import PointKey
from ._points import (
    GATEWAY_TIMING,
    GATEWAY_ZEROS,
    alarm_bit,
    choice,
    reading,
    section,
    setpoint_reading,
    setting,
    state,
    switch,
)

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
            setting(PointKey.FAN_LEVEL, 135, Limits(0, 4, step=1), on_write=CTS602_FAN_LEVEL_REREADS),
            cts602_temperature_setting(PointKey.TEMP_TARGET, 136, Limits(0, 30, step=0.5)),
            # HR 1105 AirFlow.FiltAlmType by its group: a period chosen from fixed ones, not days.
            choice(PointKey.FILTER_REPLACE_INTERVAL_CHOICE, 153, codes=FILTER_INTERVALS),
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

CTS602_LIGHT = Model("CTS 602 Light", "Nilan", CTS602_LIGHT_SECTIONS, timing=GATEWAY_TIMING)

CTS602_LIGHT_MICRO_NABTO = MicroNabtoProfile(
    model=CTS602_LIGHT,
    max_registers=64,           # a CTS 402 answered 108, so this leaves room
    later_answer_wait=5.0,      # not measured on this controller, so longer than a CTS400's
    zeros=GATEWAY_ZEROS,
)
