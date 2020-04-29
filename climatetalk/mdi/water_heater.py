# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

import datetime
import threading

from ..packet import (
    GetConfigurationRequest,
    GetStatusRequest
)


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


class WaterHeaterMDI(object):

    def __init__(self, network, address, subnet, mac_address, session_id):
        self.network = network
        self.address = address
        self.subnet = subnet
        self.mac_address = mac_address
        self.session_id = session_id

    def _send(self, packet):
        """
        :type packet: .. py:class:: climatetalk.packet.Packet
        :return:
        """
        packet.destination = self.address
        packet.subnet = self.subnet
        packet.packet_number = 0x00
        self.network.send(packet)

    def _get_status_mdi(self, byte_num, num_bytes):
        num_bytes += 1

        packet = GetStatusRequest()
        packet.destination = self.address
        packet.subnet = self.subnet
        packet.packet_number = 0x00

        event = threading.Event()

        data = bytearray()

        def callback(response):
            data.extend(
                response.payload_data[byte_num:byte_num + num_bytes]
            )
            GetConfigurationRequest.message_type.disconnect(
                self.address,
                self.subnet
            )
            event.set()

        GetConfigurationRequest.message_type.connect(
            self.address,
            self.subnet,
            callback
        )

        self.network.send(packet)
        event.wait()
        return data

    def _get_mdi(self, byte_num, num_bytes):
        num_bytes += 1

        packet = GetConfigurationRequest()
        packet.destination = self.address
        packet.subnet = self.subnet
        packet.packet_number = 0x00

        event = threading.Event()

        data = bytearray()

        def callback(response):
            data.extend(
                response.payload_data[byte_num:byte_num + num_bytes]
            )
            GetConfigurationRequest.message_type.disconnect(
                self.address,
                self.subnet
            )
            event.set()

        GetConfigurationRequest.message_type.connect(
            self.address,
            self.subnet,
            callback
        )

        self.network.send(packet)
        event.wait()
        return data

    def _has(self, byte_num):
        return bool(self._get_mdi(byte_num, 0)[0])

    @property
    def type(self):
        """returns one of WH_TYPE_* constants"""
        data = self._get_mdi(0, 0)
        return data[0]

    @property
    def application(self):
        """returns on of WH_APPLICATION_* constants"""
        data = self._get_mdi(1, 0)
        return data[0]

    @property
    def number_of_stages(self):
        data = self._get_mdi(5, 0)
        return data[0]

    @property
    def oem_max_allowed_temperature(self):
        data = self._get_mdi(3, 0)
        return data[0]

    @property
    def user_max_allowed_temperature(self):
        data = self._get_mdi(4, 0)
        return data[0]

    @property
    def oem_max_allowed_differential(self):
        data = self._get_mdi(5, 0)
        return data[0]

    @property
    def user_max_allowed_differential(self):
        data = self._get_mdi(6, 0)
        return data[0]

    @property
    def gallon_capacity(self):
        data = self._get_mdi(7, 0)
        return data[0]

    @property
    def fuel_type(self):
        """returns one of WH_FUEL_TYPE_* constants"""
        data = self._get_mdi(8, 0)
        return data[0]

    @property
    def has_fvs_sensor(self):
        return self._has(9)

    @property
    def has_flame_sensor(self):
        return self._has(10)

    @property
    def has_pressure_switch(self):
        return self._has(11)

    @property
    def thermistor_count(self):
        data = self._get_mdi(13, 0)
        return data[0]

    @property
    def ignitor_type(self):
        """returns one of WH_IGNITER_TYPE_* constants"""
        data = self._get_mdi(13, 0)
        return data[0]

    @property
    def has_gas_valve(self):
        return self._has(14)

    @property
    def has_limit_switch(self):
        return self._has(15)

    @property
    def has_vent_switch(self):
        return self._has(16)

    @property
    def has_condensate_overflow_switch(self):
        return self._has(17)

    @property
    def has_water_leak_sensor(self):
        return self._has(18)

    @property
    def has_compressor(self):
        return self._has(19)

    @property
    def has_upper_heating_element(self):
        return self._has(25)

    @property
    def has_lower_heating_element(self):
        return self._has(26)

    @property
    def has_collector_pump(self):
        return self._has(27)

    @property
    def max_allowed_lockout_time(self):
        """returns 1-254 or one of WH_LOCKOUT_* constants"""
        data = self._get_mdi(28, 0)
        return data[0]

    @property
    def has_vacation_mode(self):
        return self._has(29)

    @property
    def has_setback_mode(self):
        return self._has(30)

    @property
    def has_inlet_water_temp_sensor(self):
        return self._has(31)

    @property
    def has_hx_outlet_temp_sensor(self):
        return self._has(32)

    @property
    def has_mixed_water_temp_sensor(self):
        return self._has(33)

    @property
    def has_inlet_water_pressure_sensor(self):
        return self._has(34)

    @property
    def has_outlet_water_pressure_sensor(self):
        return self._has(35)

    @property
    def has_gas_pressure_sensor(self):
        return self._has(36)

    @property
    def has_gas_manifold_pressure_sensor(self):
        return self._has(37)

    @property
    def has_exhaust_temperature_sensor(self):
        return self._has(38)

    @property
    def has_input_line_voltage_sensor(self):
        return self._has(39)

    @property
    def has_collector_inlet_temp_sensor(self):
        return self._has(40)

    @property
    def has_collector_outlet_temp_sensor(self):
        return self._has(41)

    @property
    def has_upper_outlet_temp_sensor(self):
        return self._has(42)

    @property
    def has_lower_inlet_temp_sensor(self):
        return self._has(43)

    @property
    def max_program_hold_time(self):
        data = self._get_mdi(49, 1)
        return data[0] << 8 | data[1]

    @property
    def has_keypad_lockout(self):
        return self._has(51)

    @property
    def has_realtime_clock_lockout(self):
        return self._has(52)

    @property
    def has_beeper(self):
        return self._has(53)

    @property
    def communications_fault_timer(self):
        data = self._get_mdi(54, 1)
        return data[0] << 8 | data[1]

    @property
    def program_profile_type(self):
        """returns one of WH_PROGRAM_PROFILE_TYPE_* constants"""
        data = self._get_mdi(56, 0)
        return data[0]

    @property
    def program_interval_type(self):
        """returns one of WH_PROGRAM_INTERVAL_TYPE_* constants"""
        data = self._get_mdi(57, 0)
        return data[0]

    @property
    def supports_daylight_savings(self):
        return self._has(58)

    @property
    def gmt_offset(self):
        data = self._get_mdi(59, 0)
        return data[0] / 4.0

    @property
    def display_contrast(self):
        data = self._get_mdi(60, 0)
        return data[0]

    def _is_on(self, byte_num):
        data = self._get_status_mdi(byte_num, 0)[0]
        if data != 0xFF:
            return bool(data)

    @property
    def critical_fault(self):
        data = self._get_status_mdi(1, 0)
        return data[0]

    @property
    def minor_fault(self):
        data = self._get_status_mdi(2, 0)
        return data[0]

    @property
    def tank_temp(self):
        """
        :return: 0x00 = unknown 0xFF = probe failure
        """
        data = self._get_status_mdi(3, 0)
        return data[0]

    @property
    def setpoint(self):
        data = self._get_status_mdi(4, 0)
        return data[0]

    @property
    def max_setpoint(self):
        data = self._get_status_mdi(5, 0)
        return data[0]

    @property
    def state(self):
        """
        :return: one of WH_CONTROL_STATE_* constants
        """
        data = self._get_status_mdi(6, 0)
        return data[0]

    @property
    def fvs_sensor_status(self):
        """
        :return: one of WH_SENSOR_STATE_* constants
        """
        data = self._get_status_mdi(7, 0)
        return data[0]

    @property
    def has_flame(self):
        return self._is_on(8)

    @property
    def pws_open(self):
        value = self._get_status_mdi(9, 0)[0]
        if value != 0xFF:
            return not value

    @property
    def thermistor_status(self):
        """
        :return: one of WH_SENSOR_STATE_* constants
        """
        data = self._get_status_mdi(10, 0)
        return data[0]

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
        value = self._get_status_mdi(17, 0)[0]
        if value != 0xFF:
            return not value

    @property
    def is_vent_switch_open(self):
        value = self._get_status_mdi(18, 0)[0]
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
        data = self._get_status_mdi(30, 0)
        return data[0]

    @property
    def lockout_time_remaining(self):
        data = self._get_status_mdi(31, 0)
        return data[0]

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
        data = self._get_status_mdi(36, 0)
        return data[0]

    @property
    def hx_outet_temp(self):
        data = self._get_status_mdi(37, 0)
        return data[0]

    @property
    def mixed_water_temp(self):
        data = self._get_status_mdi(38, 0)
        return data[0]

    @property
    def inlet_water_pressure(self):
        data = self._get_status_mdi(39, 0)
        return data[0]

    @property
    def outlet_water_pressure(self):
        data = self._get_status_mdi(40, 0)
        return data[0]

    @property
    def inlet_gas_pressure(self):
        value = self._get_status_mdi(41, 0)[0]
        if value != 0xFF:
            return value / 10.0

    @property
    def gas_manifold_pressure(self):
        value = self._get_status_mdi(42, 0)[0]
        if value != 0xFF:
            return value / 10.0

    @property
    def exhaust_temperature(self):
        value = self._get_status_mdi(43, 0)[0]
        if value != 0xFF:
            return value * 10

    @property
    def draft_inducer_speed(self):
        data = self._get_status_mdi(44, 1)
        return data[0] << 8 | data[1]

    @property
    def gas_demand(self):
        data = self._get_status_mdi(46, 0)
        return data[0]

    @property
    def water_flow_demand(self):
        data = self._get_status_mdi(47, 0)
        return data[0]

    @property
    def line_voltage(self):
        data = self._get_status_mdi(48, 1)
        return data[0] << 8 | data[1]

    @property
    def line_voltage_status(self):
        """
        :return: one of WH_LINE_VOLTAGE_STATUS_* constants
        """
        data = self._get_status_mdi(50, 0)
        return data[0]

    @property
    def collector_inlet_temp(self):
        data = self._get_status_mdi(51, 0)
        return data[0]

    @property
    def collector_outlet_temp(self):
        data = self._get_status_mdi(52, 0)
        return data[0]

    @property
    def collector_pump_speed(self):
        data = self._get_status_mdi(53, 1)
        return data[0] << 8 | data[1]

    @property
    def collector_pump_flow_rate(self):
        data = self._get_status_mdi(55, 1)
        return data[0] << 8 | data[1]

    @property
    def setback_temp(self):
        data = self._get_status_mdi(57, 0)
        return data[0]

    @property
    def vacation_temp(self):
        data = self._get_status_mdi(58, 0)
        return data[0]

    @property
    def cycle_count(self):
        data = self._get_status_mdi(59, 1)
        return data[0] << 8 | data[1]

    @property
    def total_time(self):
        data = self._get_status_mdi(62, 4)
        value = (
            data[0] << 24 |
            data[1] << 16 |
            data[2] << 8 |
            data[3]
        )

        return datetime.timedelta(minutes=value)

    @property
    def running_time(self):
        data = self._get_status_mdi(66, 4)
        value = (
                data[0] << 24 |
                data[1] << 16 |
                data[2] << 8 |
                data[3]
        )

        return datetime.timedelta(minutes=value)

    @property
    def upper_outlet_temp(self):
        data = self._get_status_mdi(70, 0)
        return data[0]

    @property
    def aux_1_temp(self):
        data = self._get_status_mdi(71, 0)
        return data[0]

    @property
    def aux_2_temp(self):
        data = self._get_status_mdi(72, 0)
        return data[0]

    @property
    def lower_inlet_temp(self):
        data = self._get_status_mdi(73, 0)
        return data[0]

    @property
    def number_stages_on(self):
        data = self._get_status_mdi(74, 0)
        return data[0]

    @property
    def modulation_percent(self):
        data = self._get_status_mdi(75, 0)
        return data[0]

    @property
    def number_elements_on(self):
        data = self._get_status_mdi(76, 0)
        return data[0]

    @property
    def total_energy_consumption(self):
        data = self._get_status_mdi(66, 4)
        value = (
                data[0] << 24 |
                data[1] << 16 |
                data[2] << 8 |
                data[3]
        )
        return value
