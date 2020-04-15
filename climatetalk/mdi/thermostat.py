# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from ..utils import (
    get_bit as _get_bit,
    set_bit as _set_bit
)

THERMOSTAT_SYSTEM_TYPE_UNKNOWN = 0x00
THERMOSTAT_SYSTEM_TYPE_CONVENTIONAL = 0x01
THERMOSTAT_SYSTEM_TYPE_HEAT_PUMP = 0x02
THERMOSTAT_SYSTEM_TYPE_DUAL_FUEL = 0x03
THERMOSTAT_SYSTEM_TYPE_COOLING = 0x04
THERMOSTAT_SYSTEM_TYPE_GAS_HEAT = 0x05
THERMOSTAT_SYSTEM_TYPE_ELECTRIC_HEAT = 0x06
THERMOSTAT_SYSTEM_TYPE_ELECTRIC_ONLY = 0x07
THERMOSTAT_SYSTEM_TYPE_FAN_ONLY = 0x08
THERMOSTAT_SYSTEM_TYPE_GEOTHERMAL_HEAT_PUMP = 0x09
THERMOSTAT_SYSTEM_TYPE_GEOTHERMAL_DUAL_FUEL = 0x0A
THERMOSTAT_SYSTEM_TYPE_BOILER = 0x0B
THERMOSTAT_SYSTEM_TYPE_BOILER_HEAT_PUMP = 0x0C
THERMOSTAT_SYSTEM_TYPE_UNUSED = 0x7F
THERMOSTAT_SYSTEM_TYPE_OTHER = 0xFF

THERMOSTAT_ENABLED = 0x01
THERMOSTAT_DISABLED = 0x00

THERMOSTAT_CAPABLE = 0x01
THERMOSTAT_NOT_CAPABLE = 0x00

THERMOSTAT_SCALE_FAHRENHEIT = 0x01
THERMOSTAT_SCALE_CELSIUS = 0x00

THERMOSTAT_CYCLE_RATE_FAST = 0xFF
THERMOSTAT_CYCLE_RATE_SLOW = 0xFE

THERMOSTAT_SENSOR_WEIGHT_DEFAULT = 0x00
THERMOSTAT_SENSOR_WEIGHT_LOW = 0x01
THERMOSTAT_SENSOR_WEIGHT_MEDIUM = 0x02
THERMOSTAT_SENSOR_WEIGHT_HIGH = 0x03

THERMOSTAT_TYPE_COMMERCIAL = 0x01
THERMOSTAT_TYPE_RESIDENTIAL = 0x00

THERMOSTAT_PROFILE_TYPE_NON_PROGRAMMABLE = 0x00
THERMOSTAT_PROFILE_TYPE_7_DAY = 0x01
THERMOSTAT_PROFILE_TYPE_5_1_1 = 0x02
THERMOSTAT_PROFILE_TYPE_5_2 = 0x03

THERMOSTAT_INTERVAL_TYPE_NON_PROGRMMABLE = 0x00
THERMOSTAT_INTERVAL_TYPE_2_STEP = 0x01
THERMOSTAT_INTERVAL_TYPE_4_STEP = 0x02

THERMOSTAT_KEYPAD_LOCKOUT_OFF = 0x00
THERMOSTAT_KEYPAD_LOCKOUT_PARTIAL = 0x01
THERMOSTAT_KEYPAD_LOCKOUT_FULL = 0x02


class ThermostatMDI(bytearray):
    id = 0

    @property
    def system_type(self):
        """
        :return: one of THERMOSTAT_SYSTEM_TYPE_* constants
        """
        return self[0]

    @property
    def heat_stages(self):
        """
        :return: number of stages, 15 = Variable/Modulating
        """
        return self[1] >> 4 | 0xF

    @property
    def cool_stages(self):
        """
        :return: number of stages, 15 = Variable/Modulating
        """
        return self[1] & 0xFF

    @property
    def balance_point_set_temp(self):
        """
        :return:
            0x00 = Balance Point System is off
            0xFF = Default value indicating that this is not being used
            0x01 - 0x7F =
        """
        return self[2]

    @property
    def filter_time(self):
        """
        :return: hours
        """
        return self[3] << 8 | self[4]

    @property
    def temp_adjustment_offset(self):
        return self[5]

    @property
    def programmable_hold_time(self):
        """
        :return:
            0x00 = disabled
            0xFFFF = default value
        """
        return self[6] << 8 | self[7]

    @property
    def max_temp(self):
        """
        :return: 0xFF = not set/default
        """
        return self[8]

    @property
    def min_temp(self):
        """
        :return: 0xFF = not set/default
        """
        return self[9]

    @property
    def emr_state(self):
        """
        :return: THERMOSTAT_ENABLED or THERMOSTAT_DISABLED
        """
        return int(_get_bit(self[10], 7))

    @property
    def keypad_lockout(self):
        """
        :return: one of THERMOSTAT_KEYPAD_LOCKOUT_* constants
        """
        if _get_bit(self[10], 6):
            if _get_bit(self[22], 2):
                return THERMOSTAT_KEYPAD_LOCKOUT_PARTIAL

            elif _get_bit(self[22], 1):
                return THERMOSTAT_KEYPAD_LOCKOUT_FULL

        return THERMOSTAT_KEYPAD_LOCKOUT_OFF

    @property
    def scale(self):
        """
        :return: one of THERMOSTAT_SCALE_* constants
        """

        return int(_get_bit(self[10], 5))

    @property
    def fast_second_stage(self):
        """
        :return: THERMOSTAT_ENABLED or THERMOSTAT_DISABLED
        """
        return int(_get_bit(self[10], 4))

    @property
    def continious_display_light(self):
        """
        :return: THERMOSTAT_ENABLED or THERMOSTAT_DISABLED
        """
        return int(_get_bit(self[10], 3))

    @property
    def compressor_lockout(self):
        """
        :return: THERMOSTAT_ENABLED or THERMOSTAT_DISABLED
        """
        return int(_get_bit(self[10], 2))

    @property
    def heat_cycle_rate(self):
        """
        :return: % or one of THERMOSTAT_CYCLE_RATE_* constants
        """
        if self[20]:
            return float(self[21]) * 0.5

        return int(_get_bit(self[10], 2)) + 254

    @property
    def cool_cycle_rate(self):
        """
        :return: % or one of THERMOSTAT_CYCLE_RATE_* constants
        """
        if self[21]:
            return float(self[21]) * 0.5
        return int(_get_bit(self[10], 2)) + 254

    @property
    def sensor_d_weight(self):
        """
        :return: one of THERMOSTAT_SENSOR_WEIGHT_* constants
        """
        res = 0
        res = _set_bit(res, 1, _get_bit(self[11], 7))
        res = _set_bit(res, 0, _get_bit(self[11], 6))

        return res

    @property
    def sensor_c_weight(self):
        """
        :return: one of THERMOSTAT_SENSOR_WEIGHT_* constants
        """
        res = 0
        res = _set_bit(res, 1, _get_bit(self[11], 5))
        res = _set_bit(res, 0, _get_bit(self[11], 4))

        return res

    @property
    def sensor_b_weight(self):
        """
        :return: one of THERMOSTAT_SENSOR_WEIGHT_* constants
        """
        res = 0
        res = _set_bit(res, 1, _get_bit(self[11], 3))
        res = _set_bit(res, 0, _get_bit(self[11], 2))

        return res

    @property
    def sensor_a_weight(self):
        """
        :return: one of THERMOSTAT_SENSOR_WEIGHT_* constants
        """
        res = 0
        res = _set_bit(res, 1, _get_bit(self[11], 1))
        res = _set_bit(res, 0, _get_bit(self[11], 0))

        return res

    @property
    def sensor_local_weight(self):
        """
        :return: one of THERMOSTAT_SENSOR_WEIGHT_* constants
        """
        res = 0
        res = _set_bit(res, 1, _get_bit(self[12], 7))
        res = _set_bit(res, 0, _get_bit(self[12], 6))

        return res

    @property
    def type(self):
        """
        :return: one of THERMOSTAT_TYPE_* constants
        """
        return int(_get_bit(self[12], 4))

    @property
    def schedule_profile_type(self):
        """
        :return: one of THERMOSTAT_PROFILE_TYPE_* constants
        """
        res = 0
        res = _set_bit(res, 1, _get_bit(self[12], 3))
        res = _set_bit(res, 0, _get_bit(self[12], 2))

        return res

    @property
    def schedule_interval_type(self):
        """
        :return: one of THERMOSTAT_INTERVAL_TYPE_* constants
        """
        res = 0
        res = _set_bit(res, 1, _get_bit(self[12], 1))
        res = _set_bit(res, 0, _get_bit(self[12], 0))

        return res

    @property
    def air_handler_lockout_temp(self):
        """
        :return: 0xFF = not set/default
        """
        return self[13]

    @property
    def uv_lamp_time(self):
        """
        :return: days
            0x0000 = disabled
            0xFFFF = default
        """
        return self[14] << 8 | self[15]

    @property
    def humidifier_pad_time(self):
        """
        :return: hours
            0x0000 = disabled
            0xFFFF = default
        """
        return self[16] << 8 | self[17]

    @property
    def aux_heat_stages(self):
        """
        :return: 0x0F = modulating
        """
        return self[18] << 4 & 0xF

    @property
    def fan_stages(self):
        """
        :return: 0x0F = modulating
        """
        return self[18] & 0xF

    @property
    def aux_heat_cycle_rate(self):
        """
        :return: Default/Unused is 0; Percentage - 0.5% Increments.
        """
        return self[19]

    @property
    def clock_lockout(self):
        """
        :return: THERMOSTAT_ENABLED or THERMOSTAT_DISABLED
        """
        return int(_get_bit(self[22], 7))

    @property
    def ob_mode(self):
        """
        :return: 0 = O Mode/Unavailable;  1 = B Mode
        """
        return int(_get_bit(self[22], 6))

    @property
    def beep(self):
        """
        :return: THERMOSTAT_ENABLED or THERMOSTAT_DISABLED
        """
        return int(_get_bit(self[22], 5))

    @property
    def daylight_savings(self):
        """
        :return: THERMOSTAT_ENABLED or THERMOSTAT_DISABLED
        """
        return int(_get_bit(self[22], 0))

    @property
    def gmt_offset(self):
        return self[23] / 4

    @property
    def display_contrast(self):
        return self[24]

    @property
    def communication_timeout(self):
        """
        :return: seconds
        """
        return self[25] << 8 | self[26]

    @property
    def display_phone_number_on_fault(self):
        """
        :return: THERMOSTAT_ENABLED or THERMOSTAT_DISABLED
        """
        return int(_get_bit(self[27], 0))

    @property
    def indoor_unit_node_type(self):
        """
        :return: one of node_types.NODE_TYPE_* constants
        """
        return self[28]

    @property
    def outdoor_unit_node_type(self):
        """
        :return: one of node_types.NODE_TYPE_* constants
        """
        return self[29]

    @property
    def humidification_capable(self):
        """
        :return: THERMOSTAT_CAPABLE or THERMOSTAT_NOT_CAPABLE
        """
        return int(_get_bit(self[30], 3))

    @property
    def dehumidification_capable(self):
        """
        :return: THERMOSTAT_CAPABLE or THERMOSTAT_NOT_CAPABLE
        """
        return int(_get_bit(self[30], 2))

    @property
    def independent_humidification_capable(self):
        """
        :return: THERMOSTAT_CAPABLE or THERMOSTAT_NOT_CAPABLE
        """
        return int(_get_bit(self[30], 1))

    @property
    def independent_dehumidification_capable(self):
        """
        :return: THERMOSTAT_CAPABLE or THERMOSTAT_NOT_CAPABLE
        """
        return int(_get_bit(self[30], 0))

    @property
    def allowed_schedule_profiles(self):
        res = []
        if _get_bit(self[31], 3):  # 5-2
            res += [THERMOSTAT_PROFILE_TYPE_5_2]
        if _get_bit(self[31], 2):  # 7-day
            res += [THERMOSTAT_PROFILE_TYPE_7_DAY]
        if _get_bit(self[31], 1):  # 5-1-1
            res += [THERMOSTAT_PROFILE_TYPE_5_1_1]
        if _get_bit(self[31], 0):  # Non Programmable
            res += [THERMOSTAT_PROFILE_TYPE_NON_PROGRAMMABLE]

        return res

    @property
    def allowed_schedule_intervals(self):
        res = []
        if _get_bit(self[32], 2):  # 2 step
            res += [THERMOSTAT_INTERVAL_TYPE_2_STEP]
        if _get_bit(self[32], 1):  # Non Programmable
            res += [THERMOSTAT_INTERVAL_TYPE_NON_PROGRMMABLE]
        if _get_bit(self[32], 0):  # 4 step
            res += [THERMOSTAT_INTERVAL_TYPE_4_STEP]

        return res
