# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

import datetime


WH_TYPE_UNKNOWN = 0x00
WH_TYPE_GAS = 0x01
WH_TYPE_ELECTRIC = 0x02
WH_TYPE_GAS_TANKLESS = 0x03
WH_TYPE_SOLAR = 0x04
WH_TYPE_HEAT_PUMP = 0x05
WH_TYPE_UNAVAILABLE = 0xFF

WH_APPLICATION_RESIDENTIAL = 0x00
WH_APPLICATION_COMMERCIAL = 0x01

WH_FUEL_TYPE_NATURAL_GAS = 0x00
WH_FUEL_TYPE_PROPANE = 0x01
WH_FUEL_TYPE_ELECTRIC = 0x02
WH_FUEL_TYPE_ASHP = 0x03
WH_FUEL_TYPE_GSHP = 0x04
WH_FUEL_TYPE_SOLAR = 0x05
WH_FUEL_TYPE_OTHER = 0xFF

WH_NOT_INSTALLED = 0x00
WH_INSTALLED = 0x01
WH_UNAVAILABLE = 0xFF

WH_IGNITER_TYPE_NOT_INSTALLED = 0x00
WH_IGNITER_TYPE_HOT_SURFACE = 0x01
WH_IGNITER_TYPE_SPARK = 0x02
WH_IGNITER_TYPE_UNKNOWN = 0xFF

WH_LOCKOUT_NOT_ALLOWED = 0x00
WH_LOCKOUT_INDEFINATE = 0xFF

WH_PROGRAM_PROFILE_TYPE_NON_PROGRAMMABLE = 0x00
WH_PROGRAM_PROFILE_TYPE_7_DAY = 0x01
WH_PROGRAM_PROFILE_TYPE_5_2 = 0x02
WH_PROGRAM_PROFILE_TYPE_5_1_1 = 0x03
WH_PROGRAM_PROFILE_TYPE_UNAVAILABLE = 0xFF

WH_PROGRAM_INTERVAL_TYPE_NON_PROGRAMMABLE = 0x00
WH_PROGRAM_INTERVAL_TYPE_2_STEP = 0x01
WH_PROGRAM_INTERVAL_TYPE_4_STEP = 0x02
WH_PROGRAM_INTERVAL_TYPE_UNAVAILABLE = 0xFF


class WaterHeaterConfig0MDI(bytearray):
    id = 0

    @property
    def type(self):
        """returns one of WH_TYPE_* constants"""
        return self[0]

    @property
    def application(self):
        """returns on of WH_APPLICATION_* constants"""
        return self[1]

    @property
    def number_of_stages(self):
        return self[2]

    @property
    def oem_max_allowed_temperature(self):
        return self[3]

    @property
    def user_max_allowed_temperature(self):
        return self[4]

    @property
    def oem_max_allowed_differential(self):
        return self[5]

    @property
    def user_max_allowed_differential(self):
        return self[6]

    @property
    def gallon_capacity(self):
        return self[7]

    @property
    def fuel_type(self):
        """returns one of WH_FUEL_TYPE_* constants"""
        return self[8]

    @property
    def has_fvs_sensor(self):
        return bool(self[9])

    @property
    def has_flame_sensor(self):
        return bool(self[10])

    @property
    def has_pressure_switch(self):
        return bool(self[11])

    @property
    def thermistor_count(self):
        return self[12]

    @property
    def ignitor_type(self):
        """returns one of WH_IGNITER_TYPE_* constants"""

        return self[13]

    @property
    def has_gas_valve(self):
        return bool(self[14])

    @property
    def has_limit_switch(self):
        return bool(self[15])

    @property
    def has_vent_switch(self):
        return bool(self[16])

    @property
    def has_condensate_overflow_switch(self):
        return bool(self[17])

    @property
    def has_water_leak_sensor(self):
        return bool(self[18])

    @property
    def has_compressor(self):
        return bool(self[19])

    @property
    def has_upper_heating_element(self):
        return bool(self[25])

    @property
    def has_lower_heating_element(self):
        return bool(self[26])

    @property
    def has_collector_pump(self):
        return bool(self[27])

    @property
    def max_allowed_lockout_time(self):
        """returns 1-254 or one of WH_LOCKOUT_* constants"""
        return self[28]

    @property
    def has_vacation_mode(self):
        return bool(self[29])

    @property
    def has_setback_mode(self):
        return bool(self[30])

    @property
    def has_inlet_water_temp_sensor(self):
        return bool(self[31])

    @property
    def has_hx_outlet_temp_sensor(self):
        return bool(self[32])

    @property
    def has_mixed_water_temp_sensor(self):
        return bool(self[33])

    @property
    def has_inlet_water_pressure_sensor(self):
        return bool(self[34])

    @property
    def has_outlet_water_pressure_sensor(self):
        return bool(self[35])

    @property
    def has_gas_pressure_sensor(self):
        return bool(self[36])

    @property
    def has_gas_manifold_pressure_sensor(self):
        return bool(self[37])

    @property
    def has_exhaust_temperature_sensor(self):
        return bool(self[38])

    @property
    def has_input_line_voltage_sensor(self):
        return bool(self[39])

    @property
    def has_collector_inlet_temp_sensor(self):
        return bool(self[40])

    @property
    def has_collector_outlet_temp_sensor(self):
        return bool(self[41])

    @property
    def has_upper_outlet_temp_sensor(self):
        return bool(self[42])

    @property
    def has_lower_inlet_temp_sensor(self):
        return bool(self[43])

    @property
    def max_program_hold_time(self):

        return self[49] << 8 | self[50]

    @property
    def has_keypad_lockout(self):
        return bool(self[51])

    @property
    def has_realtime_clock_lockout(self):
        return bool(self[52])

    @property
    def has_beeper(self):
        return bool(self[53])

    @property
    def communications_fault_timer(self):
        return self[54] << 8 | self[55]

    @property
    def program_profile_type(self):
        """returns one of WH_PROGRAM_PROFILE_TYPE_* constants"""
        return self[56]

    @property
    def program_interval_type(self):
        """returns one of WH_PROGRAM_INTERVAL_TYPE_* constants"""
        return self[57]

    @property
    def supports_daylight_savings(self):
        return bool(self[58])

    @property
    def gmt_offset(self):
        return self[59] / 4.0

    @property
    def display_contrast(self):
        return self[60]


WH_CONTROL_STATE_IDLE = 0x00
WH_CONTROL_STATE_PRE_PURGE = 0x01
WH_CONTROL_STATE_IGNITER_WARMUP = 0x02
WH_CONTROL_STATE_IGNITER_ACTIVATION = 0x03
WH_CONTROL_STATE_IGNITER_VERIFICATION = 0x04
WH_CONTROL_STATE_INTER_PURGE = 0x05
WH_CONTROL_STATE_HEATING = 0x06
WH_CONTROL_STATE_POST_PURGE = 0x07
WH_CONTROL_STATE_FAULT = 0x08
WH_CONTROL_STATE_UNUSED = 0xFF

WH_SENSOR_STATE_OK = 0x00
WH_SENSOR_STATE_FAULT = 0x01
WH_SENSOR_STATE_UNKNOWN = 0xFF

WH_LOCKOUT_TYPE_NONE = 0x00
WH_LOCKOUT_TYPE_PERMANENT = 0x01
WH_LOCKOUT_TYPE_TEMPORARY = 0x02
WH_LOCKOUT_TYPE_GRID_SMART = 0x03
WH_LOCKOUT_TYPE_UNAVAILABLE = 0xFF

WH_LINE_VOLTAGE_STATUS_UNKNOWN = 0x00
WH_LINE_VOLTAGE_STATUS_UNDER = 0x01
WH_LINE_VOLTAGE_STATUS_NORMAL = 0x02
WH_LINE_VOLTAGE_STATUS_OVER = 0x03


class WaterHeaterStatus0MDI(bytearray):

    id = 0

    def _is_on(self, byte_num):
        value = self[byte_num]
        if value != 0xFF:
            return bool(value)

    @property
    def critical_fault(self):
        return self[1]

    @property
    def minor_fault(self):
        return self[2]

    @property
    def tank_temp(self):
        """
        :return: 0x00 = unknown 0xFF = probe failure
        """
        return self[3]

    @property
    def setpoint(self):
        return self[4]

    @property
    def max_setpoint(self):
        return self[5]

    @property
    def state(self):
        """
        :return: one of WH_CONTROL_STATE_* constants
        """
        return self[6]

    @property
    def fvs_sensor_status(self):
        """
        :return: one of WH_SENSOR_STATE_* constants
        """
        return self[7]

    @property
    def has_flame(self):
        return self._is_on(8)

    @property
    def pws_open(self):
        value = self[9]
        if value != 0xFF:
            return not value

    @property
    def thermistor_status(self):
        """
        :return: one of WH_SENSOR_STATE_* constants
        """
        return self[10]

    @property
    def is_igniter_on(self):
        return self._is_on(11)

    @property
    def is_gas_valve_open(self):
        return self._is_on(12)

    @property
    def has_call_for_heat(self):
        return self._is_on(13)

    @property
    def is_draft_inducer_running(self):
        return self._is_on(16)

    @property
    def is_limit_switch_open(self):
        value = self[17]
        if value != 0xFF:
            return not value

    @property
    def is_vent_switch_open(self):
        value = self[18]
        if value != 0xFF:
            return not value

    @property
    def has_condensate_overflow(self):
        return self._is_on(19)

    @property
    def has_water_leak(self):
        return self._is_on(20)

    @property
    def has_conpressor_fault(self):
        return self._is_on(21)

    @property
    def is_upper_element_on(self):
        return self._is_on(27)

    @property
    def is_lower_element_on(self):
        return self._is_on(28)

    @property
    def is_collector_pump_on(self):
        return self._is_on(29)

    @property
    def lockout_type(self):
        """
        :return: one of WH_LOCKOUT_TYPE_* constants
        """
        return self[30]

    @property
    def lockout_time_remaining(self):
        return self[31]

    @property
    def retry_in_progress(self):
        return self._is_on(32)

    @property
    def recycle_in_progress(self):
        return self._is_on(33)

    @property
    def is_vacation_mode_on(self):
        return self._is_on(34)

    @property
    def is_setback_on(self):
        return self._is_on(34)

    @property
    def inlet_water_temp(self):
        return self[36]

    @property
    def hx_outet_temp(self):
        return self[37]

    @property
    def mixed_water_temp(self):
        return self[38]

    @property
    def inlet_water_pressure(self):
        return self[39]

    @property
    def outlet_water_pressure(self):
        return self[40]

    @property
    def inlet_gas_pressure(self):
        value = self[41]
        if value != 0xFF:
            return value / 10.0

    @property
    def gas_manifold_pressure(self):
        value = self[42]
        if value != 0xFF:
            return value / 10.0

    @property
    def exhaust_temperature(self):
        value = self[43]
        if value != 0xFF:
            return value * 10

    @property
    def draft_inducer_speed(self):
        return self[44] << 8 | self[45]

    @property
    def gas_demand(self):
        return self[46]

    @property
    def water_flow_demand(self):
        return self[47]

    @property
    def line_voltage(self):
        return self[48] << 8 | self[49]

    @property
    def line_voltage_status(self):
        """
        :return: one of WH_LINE_VOLTAGE_STATUS_* constants
        """
        return self[50]

    @property
    def collector_inlet_temp(self):
        return self[51]

    @property
    def collector_outlet_temp(self):
        return self[52]

    @property
    def collector_pump_speed(self):
        return self[53] << 8 | self[54]

    @property
    def collector_pump_flow_rate(self):
        return self[55] << 8 | self[56]

    @property
    def setback_temp(self):
        return self[57]

    @property
    def vacation_temp(self):
        return self[58]

    @property
    def cycle_count(self):
        return self[59] << 8 | self[60]

    @property
    def total_time(self):
        value = (
            self[62] << 24 |
            self[63] << 16 |
            self[64] << 8 |
            self[65]
        )

        return datetime.timedelta(minutes=value)

    @property
    def running_time(self):
        value = (
                self[66] << 24 |
                self[67] << 16 |
                self[68] << 8 |
                self[69]
        )

        return datetime.timedelta(minutes=value)

    @property
    def upper_outlet_temp(self):
        return self[70]

    @property
    def aux_1_temp(self):
        return self[71]

    @property
    def aux_2_temp(self):
        return self[72]

    @property
    def lower_inlet_temp(self):
        return self[73]

    @property
    def number_stages_on(self):
        return self[74]

    @property
    def modulation_percent(self):
        return self[75]

    @property
    def number_elements_on(self):
        return self[76]

    @property
    def total_energy_consumption(self):
        value = (
            self[66] << 24 |
            self[67] << 16 |
            self[68] << 8 |
            self[69]
        )
        return value
