# Controllers

Every point of every controller, generated from the models by `python docs/controllers.py`.
A CTS602's variant is the slave device model its gateway's handshake names; what each
certainty means is in the README.

## Nilan CTS 400

| Key | Read | Written | Unit | Certainty |
|---|---|---|---|---|
| `alarm_1` | datapoint 51 |  |  | verified |
| `alarm_1_code` | datapoint 51 |  |  | verified |
| `alarm_1_info` | datapoint 56 |  |  | verified |
| `alarm_2` | datapoint 52 |  |  | verified |
| `alarm_2_code` | datapoint 52 |  |  | verified |
| `alarm_2_info` | datapoint 57 |  |  | verified |
| `alarm_3` | datapoint 53 |  |  | verified |
| `alarm_3_code` | datapoint 53 |  |  | verified |
| `alarm_3_info` | datapoint 58 |  |  | verified |
| `alarm_reset` |  | setpoint 30 |  | verified |
| `alarm_status` | datapoint 50 |  |  | verified |
| `bypass_active` | datapoint 23 |  |  | verified |
| `co2_level` | datapoint 47 |  | ppm | verified |
| `co2_threshold` | setpoint 35 | setpoint 35 | ppm | verified |
| `defrost_active` | datapoint 91 |  |  | verified |
| `defrost_break_time` | setpoint 43 | setpoint 43 | min | verified |
| `defrost_max_time` | setpoint 41 | setpoint 41 | min | verified |
| `enable` | setpoint 70 | setpoint 70 |  | verified |
| `fan_dutycycle_extract` | datapoint 24 |  | % | verified |
| `fan_dutycycle_supply` | datapoint 25 |  | % | verified |
| `fan_level` | setpoint 69 | setpoint 69 |  | verified |
| `fan_level1_extract_preset` | setpoint 63 | setpoint 63 | % | verified |
| `fan_level1_supply_preset` | setpoint 59 | setpoint 59 | % | verified |
| `fan_level2_extract_preset` | setpoint 64 | setpoint 64 | % | verified |
| `fan_level2_supply_preset` | setpoint 60 | setpoint 60 | % | verified |
| `fan_level3_extract_preset` | setpoint 65 | setpoint 65 | % | verified |
| `fan_level3_supply_preset` | setpoint 61 | setpoint 61 | % | verified |
| `fan_level4_extract_preset` | setpoint 66 | setpoint 66 | % | verified |
| `fan_level4_supply_preset` | setpoint 62 | setpoint 62 | % | verified |
| `fan_level_current` | datapoint 63 |  |  | verified |
| `fan_level_high_co2` | setpoint 80 | setpoint 80 |  | verified |
| `fan_level_high_humidity` | setpoint 33 | setpoint 33 |  | verified |
| `fan_level_high_humidity_time` | setpoint 34 | setpoint 34 | min | verified |
| `fan_level_low_humidity` | setpoint 32 | setpoint 32 |  | verified |
| `filter_ok` | datapoint 49 |  |  | verified |
| `filter_replace_interval` | setpoint 50 | setpoint 50 | d | verified |
| `filter_replace_reset` |  | setpoint 51 |  | verified |
| `filter_replace_time_ago` | datapoint 77 |  | d | verified |
| `filter_replace_time_remain` | datapoint 110 |  | d | verified |
| `humidity` | datapoint 31 |  | % | verified |
| `humidity_average` | datapoint 46 |  | % | verified |
| `humidity_high_active` | datapoint 64 |  |  | verified |
| `humidity_high_level` | datapoint 66 |  |  | verified |
| `humidity_high_level_time` | datapoint 70 |  | min | verified |
| `humidity_low_threshold` | setpoint 31 | setpoint 31 | % | verified |
| `temp_defrost_high_threshold` | setpoint 40 | setpoint 40 | °C | verified |
| `temp_defrost_low_threshold` | setpoint 39 | setpoint 39 | °C | verified |
| `temp_exhaust` | datapoint 30 |  | °C | verified |
| `temp_extract` | datapoint 29 |  | °C | verified |
| `temp_outside` | datapoint 27 |  | °C | verified |
| `temp_regulation_dead_band` | setpoint 38 | setpoint 38 | °C | verified |
| `temp_supply` | datapoint 28 |  | °C | verified |
| `temp_supply_max` | setpoint 58 | setpoint 58 | °C | verified |
| `temp_supply_min` | setpoint 57 | setpoint 57 | °C | verified |
| `temp_target` | setpoint 37 | setpoint 37 | °C | verified |
| `temp_winter_mode_threshold` | setpoint 45 | setpoint 45 | °C | verified |
| `voc_level` | datapoint 48 |  | ppm | verified |
| `voc_threshold` | setpoint 36 | setpoint 36 | ppm | verified |
| `winter_mode_active` | datapoint 72 |  |  | verified |

## Nilan CTS 602

| Key | Read | Written | Unit | Certainty | Variants |
|---|---|---|---|---|---|
| `air_exchange_mode` | setpoint 154 | setpoint 154 |  | inferred | all |
| `alarm_1` | datapoint 65 |  |  | reported | all |
| `alarm_1_code` | datapoint 65 |  |  | reported | all |
| `alarm_1_time` | datapoint 66 |  |  | inferred | all |
| `alarm_2` | datapoint 68 |  |  | reported | all |
| `alarm_2_code` | datapoint 68 |  |  | reported | all |
| `alarm_2_time` | datapoint 69 |  |  | inferred | all |
| `alarm_3` | datapoint 71 |  |  | reported | all |
| `alarm_3_code` | datapoint 71 |  |  | reported | all |
| `alarm_3_time` | datapoint 72 |  |  | inferred | all |
| `alarm_status` | datapoint 64 bit 7 |  |  | inferred | all |
| `antilegionella_day` | setpoint 194 | setpoint 194 |  | reported | 3, 4, 9, 10, 11, 12, 18, 19, 20, 21, 23, 30, 32, 34, 38, 43, 44, 45, 144, 244 |
| `bypass_active` | datapoint 187 |  |  | reported | all |
| `central_heat_curve` | setpoint 206 | setpoint 206 |  | inferred | all |
| `central_heat_mode` | setpoint 202 | setpoint 202 |  | reported | 20, 21, 23, 38, 43, 45, 244 |
| `central_heat_pump_mode` | setpoint 207 | setpoint 207 |  | reported | 20, 21, 23, 38, 43, 45, 244 |
| `central_heat_regulation_time` | setpoint 209 | setpoint 209 | s | inferred | all |
| `central_heat_source` | setpoint 208 | setpoint 208 |  | reported | 20, 21, 23, 38, 43, 45, 244 |
| `co2_level` | datapoint 53 |  | ppm | reported | all |
| `compressor_priority` | setpoint 191 | setpoint 191 |  | reported | 2, 9, 10, 12, 13, 30, 31, 32, 38, 43, 44, 144, 244 |
| `control_sensor` | setpoint 178 | setpoint 178 |  | inferred | all |
| `damper_test_last_date` | setpoint 157 |  |  | inferred | all |
| `damper_test_state` | setpoint 158 |  |  | inferred | all |
| `discharge_pressure` | datapoint 51 |  | bar | inferred | all |
| `enable` | setpoint 137 | setpoint 137 |  | inferred | all |
| `fan_level` | setpoint 139 | setpoint 139 |  | reported | all |
| `fan_level_cooling` | setpoint 155 | setpoint 155 |  | inferred | all |
| `fan_level_current` | datapoint 98 |  |  | inferred | all |
| `fan_level_extract` | datapoint 100 |  |  | reported | all |
| `fan_level_supply` | datapoint 99 |  |  | reported | all |
| `filter_replace_interval` | setpoint 159 | setpoint 159 | d | reported | all |
| `filter_replace_time_ago` | datapoint 101 |  | d | inferred | all |
| `filter_replace_time_remain` | datapoint 102 |  | d | reported | all |
| `heat_pump_active` | datapoint 164 |  |  | reported | 44, 144, 244 |
| `heat_pump_capacity` | datapoint 268 |  | % | reported | 44, 144, 244 |
| `heat_pump_heater_active` | datapoint 165 |  |  | reported | 44, 144, 244 |
| `heat_pump_state` | datapoint 198 |  |  | reported | 44, 144, 244 |
| `heat_source` | setpoint 179 | setpoint 179 |  | inferred | all |
| `hotwater_supplement` | setpoint 193 | setpoint 193 |  | inferred | all |
| `humidity` | datapoint 52 |  | % | reported | all |
| `operation_mode` | setpoint 138 | setpoint 138 |  | reported | all but 23 |
| `operation_mode_current` | datapoint 85 |  |  | inferred | all |
| `operation_state` | datapoint 86 |  |  | reported | all |
| `reheat_enable` | setpoint 281 | setpoint 281 |  | reported | 2, 3, 4, 9, 10, 11, 12, 13, 18, 19, 20, 21, 23, 26, 27, 30, 31, 33, 34, 35, 36, 38, 39, 40, 41, 43, 44, 45, 144, 244 |
| `running` | datapoint 84 |  |  | inferred | all |
| `sacrificial_anode_ok` | datapoint 142 |  |  | reported | 9, 10, 11, 12, 18, 19, 20, 21, 23, 30, 34, 38, 43, 44, 144, 244 |
| `service_capacity` | setpoint 142 | setpoint 142 | % | inferred | all |
| `service_mode` | setpoint 141 | setpoint 141 |  | inferred | all |
| `state_code` | datapoint 86 |  |  | reported | all |
| `suction_pressure` | datapoint 50 |  | bar | inferred | all |
| `temp_after_condenser` | datapoint 57 |  | °C | reported | 44, 144, 244 |
| `temp_aux` | datapoint 47 |  | °C | inferred | all |
| `temp_before_condenser` | datapoint 154 |  | °C | reported | 44, 144, 244 |
| `temp_buffer_tank` | datapoint 252 |  | °C | reported | 44, 144, 244 |
| `temp_central_heat_compensation` | setpoint 205 | setpoint 205 | °C | inferred | all |
| `temp_central_heat_offset` | setpoint 201 | setpoint 201 | °C | inferred | all |
| `temp_central_heat_return` | datapoint 44 |  | °C | reported | 20, 21, 23, 38, 43, 45, 244 |
| `temp_central_heat_supply` | datapoint 45 |  | °C | reported | 20, 21, 23, 38, 43, 45, 244 |
| `temp_central_heat_supply_max` | setpoint 204 | setpoint 204 | °C | reported | 20, 21, 23, 38, 43, 45, 244 |
| `temp_central_heat_supply_min` | setpoint 203 | setpoint 203 | °C | reported | 20, 21, 23, 38, 43, 45, 244 |
| `temp_condenser` | datapoint 36 |  | °C | reported | all |
| `temp_controller` | datapoint 31 |  | °C | inferred | all |
| `temp_cooling_start_offset` | setpoint 170 | setpoint 170 |  | reported | 4, 9, 10, 12, 19, 21, 26, 30, 32, 33, 35, 36, 38, 39, 40, 41, 43, 44, 45, 144, 244 |
| `temp_evaporator` | datapoint 37 |  | °C | reported | all |
| `temp_exhaust` | datapoint 35 |  | °C | verified | all |
| `temp_extract` | datapoint 34 |  | °C | verified | 2, 13, 27, 31 |
| `temp_extract` | datapoint 41 |  | °C | reported | all but 2, 13, 27, 31 |
| `temp_heat_pump_outdoor` | datapoint 156 |  | °C | reported | 44, 144, 244 |
| `temp_heater` | datapoint 40 |  | °C | reported | all |
| `temp_hotwater` | setpoint 190 | setpoint 190 | °C | reported | 9, 10, 11, 12, 13, 18, 19, 20, 21, 23, 30, 31, 32, 34, 38, 43, 44, 144, 244 |
| `temp_hotwater_boost` | setpoint 189 | setpoint 189 | °C | reported | 9, 10, 11, 12, 13, 18, 19, 20, 21, 23, 30, 31, 32, 34, 38, 43, 44, 144, 244 |
| `temp_hotwater_bottom` | datapoint 43 |  | °C | reported | 9, 10, 11, 12, 18, 19, 20, 21, 23, 30, 32, 34, 38, 43, 44, 144, 244 |
| `temp_hotwater_bypass_offset` | setpoint 195 | setpoint 195 | °C | inferred | all |
| `temp_hotwater_scald_protection` | setpoint 192 | setpoint 192 | °C | inferred | all |
| `temp_hotwater_top` | datapoint 42 |  | °C | reported | 9, 10, 11, 12, 18, 19, 20, 21, 23, 30, 32, 34, 38, 43, 44, 144, 244 |
| `temp_intake` | datapoint 32 |  | °C | inferred | all |
| `temp_night_cooling_day_limit` | setpoint 176 | setpoint 176 | °C | inferred | all |
| `temp_night_cooling_target` | setpoint 177 | setpoint 177 | °C | inferred | all |
| `temp_outside` | datapoint 39 |  | °C | verified | all |
| `temp_preheat_intake` | datapoint 48 |  | °C | inferred | all |
| `temp_pressure_pipe` | datapoint 256 |  | °C | reported | 44, 144, 244 |
| `temp_pressure_pipe` | datapoint 49 |  | °C | inferred | all but 44, 144, 244 |
| `temp_room` | datapoint 41 |  | °C | reported | all |
| `temp_room_panel` | datapoint 46 |  | °C | inferred | all |
| `temp_summer_supply_max` | setpoint 173 | setpoint 173 | °C | reported | 2, 4, 9, 10, 12, 13, 19, 21, 26, 30, 31, 32, 33, 34, 35, 36, 38, 39, 40, 41, 43, 44, 45, 144, 244 |
| `temp_summer_supply_min` | setpoint 171 | setpoint 171 | °C | reported | 2, 4, 9, 10, 12, 13, 19, 21, 26, 30, 31, 32, 33, 34, 35, 36, 38, 39, 40, 41, 43, 44, 45, 144, 244 |
| `temp_supply` | datapoint 33 |  | °C | verified | all |
| `temp_supply_after_heater` | datapoint 38 |  | °C | reported | all |
| `temp_target` | setpoint 140 | setpoint 140 | °C | reported | all |
| `temp_winter_mode_threshold` | setpoint 175 | setpoint 175 | °C | inferred | all |
| `temp_winter_supply_max` | setpoint 174 | setpoint 174 | °C | inferred | all |
| `temp_winter_supply_min` | setpoint 172 | setpoint 172 | °C | inferred | all |
| `time_in_state` | datapoint 87 |  | s | inferred | all |

## Nilan CTS 602 Light

| Key | Read | Written | Unit | Certainty |
|---|---|---|---|---|
| `alarm_1` | datapoint 64 |  |  | reported |
| `alarm_1_code` | datapoint 64 |  |  | reported |
| `alarm_1_time` | datapoint 65 |  |  | inferred |
| `alarm_2` | datapoint 67 |  |  | reported |
| `alarm_2_code` | datapoint 67 |  |  | reported |
| `alarm_2_time` | datapoint 68 |  |  | inferred |
| `alarm_3` | datapoint 70 |  |  | reported |
| `alarm_3_code` | datapoint 70 |  |  | reported |
| `alarm_3_time` | datapoint 71 |  |  | inferred |
| `alarm_status` | datapoint 63 bit 7 |  |  | inferred |
| `bypass_active` | datapoint 129 |  |  | reported |
| `co2_level` | datapoint 53 |  | ppm | reported |
| `damper_test_day` | setpoint 150 |  |  | inferred |
| `damper_test_last_date` | setpoint 151 |  |  | inferred |
| `damper_test_state` | setpoint 152 |  |  | inferred |
| `enable` | setpoint 133 | setpoint 133 |  | inferred |
| `fan_level` | setpoint 135 | setpoint 135 |  | reported |
| `fan_level_current` | datapoint 97 |  |  | inferred |
| `fan_level_extract` | datapoint 99 |  |  | reported |
| `fan_level_supply` | datapoint 98 |  |  | reported |
| `filter_replace_interval` | setpoint 153 | setpoint 153 | d | reported |
| `filter_replace_time_ago` | datapoint 100 |  | d | inferred |
| `filter_replace_time_remain` | datapoint 101 |  | d | reported |
| `humidity` | datapoint 51 |  | % | reported |
| `operation_mode` | setpoint 134 | setpoint 134 |  | inferred |
| `operation_mode_current` | datapoint 84 |  |  | inferred |
| `operation_state` | datapoint 85 |  |  | reported |
| `running` | datapoint 83 |  |  | inferred |
| `service_capacity` | setpoint 138 | setpoint 138 | % | inferred |
| `service_mode` | setpoint 137 | setpoint 137 |  | inferred |
| `state_code` | datapoint 85 |  |  | reported |
| `temp_controller` | datapoint 30 |  | °C | inferred |
| `temp_exhaust` | datapoint 34 |  | °C | reported |
| `temp_extract` | datapoint 33 |  | °C | reported |
| `temp_heater` | datapoint 39 |  | °C | reported |
| `temp_outside` | datapoint 38 |  | °C | reported |
| `temp_supply` | datapoint 37 |  | °C | reported |
| `temp_target` | setpoint 136 | setpoint 136 | °C | reported |
| `time_in_state` | datapoint 86 |  | s | inferred |

## Genvex Optima 250

| Key | Read | Written | Unit | Certainty |
|---|---|---|---|---|
| `alarm_bits` | datapoint 101 |  |  | reported |
| `alarm_external_filter` | datapoint 101 bit 5 |  |  | reported |
| `alarm_external_stop` | datapoint 101 bit 0 |  |  | reported |
| `alarm_fan_error` | datapoint 101 bit 6 |  |  | reported |
| `alarm_frost_failure` | datapoint 101 bit 3 |  |  | reported |
| `alarm_high_pressure` | datapoint 101 bit 2 |  |  | reported |
| `alarm_panel_communication` | datapoint 101 bit 4 |  |  | reported |
| `alarm_sensor_error` | datapoint 101 bit 7 |  |  | reported |
| `bypass_active` | datapoint 104 |  |  | reported |
| `fan_dutycycle_extract` | datapoint 103 |  | % | reported |
| `fan_dutycycle_supply` | datapoint 102 |  | % | reported |
| `fan_level` | setpoint 100 | setpoint 100 |  | reported |
| `fan_level1_extract_preset` | setpoint 9 | setpoint 9 | % | reported |
| `fan_level1_supply_preset` | setpoint 6 | setpoint 6 | % | reported |
| `fan_level2_extract_preset` | setpoint 10 | setpoint 10 | % | reported |
| `fan_level2_supply_preset` | setpoint 7 | setpoint 7 | % | reported |
| `fan_level3_extract_preset` | setpoint 11 | setpoint 11 | % | reported |
| `fan_level3_supply_preset` | setpoint 8 | setpoint 8 | % | reported |
| `fan_rpm_extract` | datapoint 109 |  | /min | reported |
| `fan_rpm_supply` | datapoint 108 |  | /min | reported |
| `filter_ok` | datapoint 101 bit 1 |  |  | reported |
| `filter_replace_interval` | setpoint 4 | setpoint 4 | mo | reported |
| `filter_replace_reset` |  | setpoint 105 |  | reported |
| `humidity` | datapoint 10 |  | % | reported |
| `humidity_control_enable` | setpoint 5 | setpoint 5 |  | reported |
| `reheat_enable` | setpoint 2 | setpoint 2 |  | reported |
| `temp_bypass_open_offset` | setpoint 17 | setpoint 17 | °C | reported |
| `temp_exhaust` | datapoint 3 |  | °C | reported |
| `temp_extract` | datapoint 6 |  | °C | reported |
| `temp_outside` | datapoint 2 |  | °C | reported |
| `temp_supply` | datapoint 0 |  | °C | reported |
| `temp_target` | setpoint 0 | setpoint 0 | °C | reported |

## Genvex Optima 251

| Key | Read | Written | Unit | Certainty |
|---|---|---|---|---|
| `alarm_bits` | datapoint 101 |  |  | reported |
| `alarm_external_filter` | datapoint 101 bit 5 |  |  | reported |
| `alarm_external_stop` | datapoint 101 bit 0 |  |  | reported |
| `alarm_fan_error` | datapoint 101 bit 6 |  |  | reported |
| `alarm_frost_failure` | datapoint 101 bit 3 |  |  | reported |
| `alarm_high_pressure` | datapoint 101 bit 2 |  |  | reported |
| `alarm_panel_communication` | datapoint 101 bit 4 |  |  | reported |
| `alarm_sensor_error` | datapoint 101 bit 7 |  |  | reported |
| `bypass_active` | datapoint 104 |  |  | reported |
| `fan_dutycycle_extract` | datapoint 103 |  | % | reported |
| `fan_dutycycle_supply` | datapoint 102 |  | % | reported |
| `fan_level` | setpoint 100 | setpoint 100 |  | reported |
| `fan_level1_extract_preset` | setpoint 9 | setpoint 9 | % | reported |
| `fan_level1_supply_preset` | setpoint 6 | setpoint 6 | % | reported |
| `fan_level2_extract_preset` | setpoint 10 | setpoint 10 | % | reported |
| `fan_level2_supply_preset` | setpoint 7 | setpoint 7 | % | reported |
| `fan_level3_extract_preset` | setpoint 11 | setpoint 11 | % | reported |
| `fan_level3_supply_preset` | setpoint 8 | setpoint 8 | % | reported |
| `fan_rpm_extract` | datapoint 109 |  | /min | reported |
| `fan_rpm_supply` | datapoint 108 |  | /min | reported |
| `filter_ok` | datapoint 101 bit 1 |  |  | reported |
| `filter_replace_interval` | setpoint 4 | setpoint 4 | mo | reported |
| `filter_replace_reset` |  | setpoint 105 |  | reported |
| `humidity` | datapoint 10 |  | % | reported |
| `humidity_control_enable` | setpoint 5 | setpoint 5 |  | reported |
| `reheat_enable` | setpoint 2 | setpoint 2 |  | reported |
| `temp_bypass_open_offset` | setpoint 17 | setpoint 17 | °C | reported |
| `temp_exhaust` | datapoint 3 |  | °C | reported |
| `temp_extract` | datapoint 6 |  | °C | reported |
| `temp_outside` | datapoint 2 |  | °C | reported |
| `temp_supply` | datapoint 0 |  | °C | reported |
| `temp_target` | setpoint 0 | setpoint 0 | °C | reported |

## Genvex Optima 260

| Key | Read | Written | Unit | Certainty |
|---|---|---|---|---|
| `bypass_active` | datapoint 11 |  |  | reported |
| `fan_dutycycle_extract` | datapoint 10 |  | % | reported |
| `fan_dutycycle_supply` | datapoint 9 |  | % | reported |
| `fan_level` | setpoint 0 | setpoint 0 |  | reported |
| `fan_level1_extract_preset` | setpoint 10 | setpoint 10 | % | reported |
| `fan_level1_supply_preset` | setpoint 7 | setpoint 7 | % | reported |
| `fan_level2_extract_preset` | setpoint 11 | setpoint 11 | % | reported |
| `fan_level2_supply_preset` | setpoint 8 | setpoint 8 | % | reported |
| `fan_level3_extract_preset` | setpoint 12 | setpoint 12 | % | reported |
| `fan_level3_supply_preset` | setpoint 9 | setpoint 9 | % | reported |
| `filter_replace_reset` |  | setpoint 47 |  | reported |
| `humidity` | datapoint 13 |  | % | reported |
| `temp_bypass_open_offset` | setpoint 18 | setpoint 18 | °C | reported |
| `temp_exhaust` | datapoint 3 |  | °C | reported |
| `temp_extract` | datapoint 6 |  | °C | reported |
| `temp_outside` | datapoint 2 |  | °C | reported |
| `temp_supply` | datapoint 0 |  | °C | reported |
| `temp_target` | setpoint 2 | setpoint 2 | °C | reported |

## Genvex Optima 270

| Key | Read | Written | Unit | Certainty |
|---|---|---|---|---|
| `alarm_bits` | datapoint 114 |  |  | verified |
| `alarm_bits_high` | datapoint 115 |  |  | verified |
| `alarm_external_stop` | datapoint 114 bit 1 |  |  | verified |
| `alarm_extract_fan_error` | datapoint 114 bit 14 |  |  | verified |
| `alarm_fire_box_1_error` | datapoint 115 bit 4 |  |  | verified |
| `alarm_fire_box_2_error` | datapoint 115 bit 5 |  |  | verified |
| `alarm_fire_damper_1_error` | datapoint 115 bit 0 |  |  | verified |
| `alarm_fire_damper_2_error` | datapoint 115 bit 1 |  |  | verified |
| `alarm_fire_damper_3_error` | datapoint 115 bit 2 |  |  | verified |
| `alarm_fire_damper_4_error` | datapoint 115 bit 3 |  |  | verified |
| `alarm_fire_test_error` | datapoint 114 bit 12 |  |  | verified |
| `alarm_frost_failure` | datapoint 114 bit 15 |  |  | verified |
| `alarm_humidity_sensor_error` | datapoint 114 bit 11 |  |  | verified |
| `alarm_rotor` | datapoint 115 bit 6 |  |  | verified |
| `alarm_sensor_t1_error` | datapoint 114 bit 2 |  |  | verified |
| `alarm_sensor_t2_error` | datapoint 114 bit 3 |  |  | verified |
| `alarm_sensor_t3_error` | datapoint 114 bit 4 |  |  | verified |
| `alarm_sensor_t4_error` | datapoint 114 bit 5 |  |  | verified |
| `alarm_sensor_t5_error` | datapoint 114 bit 6 |  |  | verified |
| `alarm_sensor_t6_error` | datapoint 114 bit 7 |  |  | verified |
| `alarm_sensor_t7_error` | datapoint 114 bit 8 |  |  | verified |
| `alarm_sensor_t8_error` | datapoint 114 bit 9 |  |  | verified |
| `alarm_sensor_t9_error` | datapoint 114 bit 10 |  |  | verified |
| `alarm_supply_fan_error` | datapoint 114 bit 13 |  |  | verified |
| `boost_enable` | setpoint 30 | setpoint 70 |  | verified |
| `boost_time` | setpoint 70 | setpoint 150 | min | verified |
| `bypass_active` | datapoint 53 |  |  | verified |
| `bypass_fan_increase` | setpoint 57 | setpoint 124 | % | verified |
| `bypass_position` | datapoint 40 |  |  | verified |
| `fan_dutycycle_extract` | datapoint 19 |  | % | verified |
| `fan_dutycycle_supply` | datapoint 18 |  | % | verified |
| `fan_level` | setpoint 7 | setpoint 24 |  | verified |
| `fan_rpm_extract` | datapoint 36 |  | /min | verified |
| `fan_rpm_supply` | datapoint 35 |  | /min | verified |
| `filter_ok` | datapoint 114 bit 0 |  |  | verified |
| `filter_replace_interval` | setpoint 100 | setpoint 210 | d | verified |
| `filter_replace_reset` |  | setpoint 110 |  | verified |
| `humidity` | datapoint 26 |  | % | verified |
| `humidity_control_enable` | setpoint 6 | setpoint 22 |  | verified |
| `preheat_output` | datapoint 41 |  | % | verified |
| `reheat_enable` | setpoint 3 | setpoint 16 |  | verified |
| `reheat_output` | datapoint 42 |  | % | verified |
| `rotor_speed` | datapoint 50 |  | /min | verified |
| `temp_bypass_close_offset` | setpoint 29 | setpoint 68 | °C | verified |
| `temp_bypass_fan_increase_offset` | setpoint 58 | setpoint 126 | °C | verified |
| `temp_bypass_open_offset` | setpoint 21 | setpoint 52 | °C | verified |
| `temp_exhaust` | datapoint 22 |  | °C | verified |
| `temp_extract` | datapoint 23 |  | °C | verified |
| `temp_frost_protection` | datapoint 24 |  | °C | verified |
| `temp_outside` | datapoint 21 |  | °C | verified |
| `temp_supply` | datapoint 20 |  | °C | verified |
| `temp_target` | setpoint 1 | setpoint 12 | °C | verified |

## Genvex Optima 301

| Key | Read | Written | Unit | Certainty |
|---|---|---|---|---|
| `alarm_bits` | datapoint 101 |  |  | reported |
| `alarm_external_filter` | datapoint 101 bit 5 |  |  | reported |
| `alarm_external_stop` | datapoint 101 bit 0 |  |  | reported |
| `alarm_fan_error` | datapoint 101 bit 6 |  |  | reported |
| `alarm_frost_failure` | datapoint 101 bit 3 |  |  | reported |
| `alarm_high_pressure` | datapoint 101 bit 2 |  |  | reported |
| `alarm_panel_communication` | datapoint 101 bit 4 |  |  | reported |
| `alarm_sensor_error` | datapoint 101 bit 7 |  |  | reported |
| `bypass_active` | datapoint 104 |  |  | reported |
| `cooling_enable` | setpoint 2 | setpoint 2 |  | reported |
| `cooling_temperature` | setpoint 1 | setpoint 1 |  | reported |
| `fan_dutycycle_extract` | datapoint 103 |  | % | reported |
| `fan_dutycycle_supply` | datapoint 102 |  | % | reported |
| `fan_level` | setpoint 100 | setpoint 100 |  | reported |
| `fan_level1_extract_preset` | setpoint 9 | setpoint 9 | % | reported |
| `fan_level1_supply_preset` | setpoint 6 | setpoint 6 | % | reported |
| `fan_level2_extract_preset` | setpoint 10 | setpoint 10 | % | reported |
| `fan_level2_supply_preset` | setpoint 7 | setpoint 7 | % | reported |
| `fan_level3_extract_preset` | setpoint 11 | setpoint 11 | % | reported |
| `fan_level3_supply_preset` | setpoint 8 | setpoint 8 | % | reported |
| `filter_ok` | datapoint 101 bit 1 |  |  | reported |
| `filter_replace_reset` |  | setpoint 105 |  | reported |
| `humidity` | datapoint 10 |  | % | reported |
| `preheat_enable` | setpoint 20 | setpoint 20 |  | reported |
| `temp_before_condenser` | datapoint 4 |  | °C | reported |
| `temp_evaporator` | datapoint 5 |  | °C | reported |
| `temp_exhaust` | datapoint 3 |  | °C | reported |
| `temp_hotwater_bottom` | datapoint 7 |  | °C | reported |
| `temp_hotwater_top` | datapoint 6 |  | °C | reported |
| `temp_outside` | datapoint 2 |  | °C | reported |
| `temp_room` | datapoint 9 |  | °C | reported |
| `temp_supply` | datapoint 0 |  | °C | reported |
| `temp_target` | setpoint 0 | setpoint 0 | °C | reported |

## Genvex Optima 312

| Key | Read | Written | Unit | Certainty |
|---|---|---|---|---|
| `alarm_bits` | datapoint 101 |  |  | reported |
| `alarm_external_filter` | datapoint 101 bit 5 |  |  | reported |
| `alarm_external_stop` | datapoint 101 bit 0 |  |  | reported |
| `alarm_fan_error` | datapoint 101 bit 6 |  |  | reported |
| `alarm_frost_failure` | datapoint 101 bit 3 |  |  | reported |
| `alarm_high_pressure` | datapoint 101 bit 2 |  |  | reported |
| `alarm_panel_communication` | datapoint 101 bit 4 |  |  | reported |
| `alarm_sensor_error` | datapoint 101 bit 7 |  |  | reported |
| `bypass_active` | datapoint 104 |  |  | reported |
| `defrost_active` | datapoint 14 |  |  | reported |
| `fan_dutycycle_extract` | datapoint 103 |  | % | reported |
| `fan_dutycycle_supply` | datapoint 102 |  | % | reported |
| `fan_level` | setpoint 100 | setpoint 100 |  | reported |
| `fan_level1_extract_preset` | setpoint 9 | setpoint 9 | % | reported |
| `fan_level1_supply_preset` | setpoint 6 | setpoint 6 | % | reported |
| `fan_level2_extract_preset` | setpoint 10 | setpoint 10 | % | reported |
| `fan_level2_supply_preset` | setpoint 7 | setpoint 7 | % | reported |
| `fan_level3_extract_preset` | setpoint 11 | setpoint 11 | % | reported |
| `fan_level3_supply_preset` | setpoint 8 | setpoint 8 | % | reported |
| `filter_ok` | datapoint 101 bit 1 |  |  | reported |
| `filter_replace_reset` |  | setpoint 105 |  | reported |
| `heat_pump_active` | datapoint 11 |  |  | reported |
| `heat_pump_heater_active` | datapoint 12 |  |  | reported |
| `heat_pump_room_heating` | datapoint 16 |  |  | reported |
| `heat_pump_water_heating` | datapoint 15 |  |  | reported |
| `hotwater_heater_enable` | setpoint 2 | setpoint 2 |  | reported |
| `humidity` | datapoint 10 |  | % | reported |
| `reheat_active` | datapoint 13 |  |  | reported |
| `reheat_enable` | setpoint 21 | setpoint 21 |  | reported |
| `temp_before_condenser` | datapoint 4 |  | °C | reported |
| `temp_evaporator` | datapoint 5 |  | °C | reported |
| `temp_exhaust` | datapoint 3 |  | °C | reported |
| `temp_hotwater` | setpoint 1 | setpoint 1 | °C | reported |
| `temp_hotwater_bottom` | datapoint 7 |  | °C | reported |
| `temp_hotwater_top` | datapoint 6 |  | °C | reported |
| `temp_outside` | datapoint 2 |  | °C | reported |
| `temp_room` | datapoint 9 |  | °C | reported |
| `temp_supply` | datapoint 0 |  | °C | reported |
| `temp_target` | setpoint 0 | setpoint 0 | °C | reported |

## Genvex Optima 314

| Key | Read | Written | Unit | Certainty |
|---|---|---|---|---|
| `alarm_bits` | datapoint 114 |  |  | reported |
| `alarm_bits_high` | datapoint 115 |  |  | reported |
| `alarm_external_stop` | datapoint 114 bit 2 |  |  | reported |
| `alarm_extract_fan_error` | datapoint 114 bit 15 |  |  | reported |
| `alarm_fire_box_1_error` | datapoint 115 bit 5 |  |  | reported |
| `alarm_fire_box_2_error` | datapoint 115 bit 6 |  |  | reported |
| `alarm_fire_damper_1_error` | datapoint 115 bit 1 |  |  | reported |
| `alarm_fire_damper_2_error` | datapoint 115 bit 2 |  |  | reported |
| `alarm_fire_damper_3_error` | datapoint 115 bit 3 |  |  | reported |
| `alarm_fire_damper_4_error` | datapoint 115 bit 4 |  |  | reported |
| `alarm_fire_test_error` | datapoint 114 bit 13 |  |  | reported |
| `alarm_flow_temperature_error` | datapoint 115 bit 11 |  |  | reported |
| `alarm_high_pressure` | datapoint 115 bit 9 |  |  | reported |
| `alarm_humidity_sensor_error` | datapoint 114 bit 12 |  |  | reported |
| `alarm_internal_modbus` | datapoint 115 bit 8 |  |  | reported |
| `alarm_low_pressure` | datapoint 115 bit 10 |  |  | reported |
| `alarm_return_temperature_error` | datapoint 115 bit 12 |  |  | reported |
| `alarm_sensor_t10_error` | datapoint 115 bit 13 |  |  | reported |
| `alarm_sensor_t11_error` | datapoint 115 bit 14 |  |  | reported |
| `alarm_sensor_t1_error` | datapoint 114 bit 3 |  |  | reported |
| `alarm_sensor_t2_error` | datapoint 114 bit 4 |  |  | reported |
| `alarm_sensor_t3_error` | datapoint 114 bit 5 |  |  | reported |
| `alarm_sensor_t4_error` | datapoint 114 bit 6 |  |  | reported |
| `alarm_sensor_t5_error` | datapoint 114 bit 7 |  |  | reported |
| `alarm_sensor_t6_error` | datapoint 114 bit 8 |  |  | reported |
| `alarm_sensor_t7_error` | datapoint 114 bit 9 |  |  | reported |
| `alarm_sensor_t8_error` | datapoint 114 bit 10 |  |  | reported |
| `alarm_sensor_t9_error` | datapoint 114 bit 11 |  |  | reported |
| `alarm_supply_fan_error` | datapoint 114 bit 14 |  |  | reported |
| `boost_enable` | setpoint 30 | setpoint 70 |  | reported |
| `boost_time` | setpoint 70 | setpoint 150 | min | reported |
| `bypass_active` | datapoint 12 |  |  | reported |
| `fan_dutycycle_extract` | datapoint 19 |  | % | reported |
| `fan_dutycycle_supply` | datapoint 18 |  | % | reported |
| `fan_level` | setpoint 7 | setpoint 24 |  | reported |
| `fan_rpm_extract` | datapoint 36 |  | /min | reported |
| `fan_rpm_supply` | datapoint 35 |  | /min | reported |
| `filter_ok` | datapoint 114 bit 1 |  |  | reported |
| `filter_replace_interval` | setpoint 100 | setpoint 210 | d | reported |
| `filter_replace_reset` |  | setpoint 110 |  | reported |
| `heat_pump_active` | datapoint 75 |  |  | reported |
| `heat_pump_heater_active` | datapoint 58 |  |  | reported |
| `humidity` | datapoint 26 |  | % | reported |
| `humidity_control_enable` | setpoint 6 | setpoint 22 |  | reported |
| `reheat_enable` | setpoint 3 | setpoint 16 |  | reported |
| `temp_before_condenser` | datapoint 65 |  | °C | reported |
| `temp_evaporator` | datapoint 66 |  | °C | reported |
| `temp_exhaust` | datapoint 22 |  | °C | reported |
| `temp_extract` | datapoint 64 |  | °C | reported |
| `temp_hotwater` | setpoint 122 | setpoint 254 | °C | reported |
| `temp_hotwater_bottom` | datapoint 24 |  | °C | reported |
| `temp_hotwater_top` | datapoint 23 |  | °C | reported |
| `temp_outside` | datapoint 21 |  | °C | reported |
| `temp_supply` | datapoint 20 |  | °C | reported |
| `temp_target` | setpoint 1 | setpoint 12 | °C | reported |
