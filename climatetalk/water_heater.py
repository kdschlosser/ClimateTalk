# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser


import threading
import datetime
from .packet import (
    GetConfigurationRequest,
    GetConfigurationResponse,
    SetConfigurationRequest,

from .utils import get_bit as _get_bit, set_bit as _set_bit


# supported packets a water heater can receive

# GetConfigurationRequest
# GetStatusRequest
# SetControlCommandRequest
# SetDisplayMessageRequest
# SetDiagnosticsRequest
# GetSensorDataRequest
# SetIdentificationRequest
# GetIdentificationRequest
# SetManufacturerDeviceDataRequest
# GetManufacturerDeviceDataRequest
# SetNetwork NodeListRequest
# GetUserMenuRequest
# SetUserMenuUpdateRequest
# SetEchoRequest


# packets that can be sent from a water heater
# GetConfigurationResponse
# GetStatusResponse
# SetControlCommandResponse
# SetDisplayMessageResponse
# SetDiagnosticsResponse
# GetDiagnosticsResponse
# GetSensor DataResponse
# GetUserMenuResponse
# SetUserMenuUpdateResponse
# SetEchoResponse


# water heater config messages

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

WH_TYPE_BYTE = 0x00
WH_APPLICATION_BYTE = 0x01
WH_STAGES_BYTE = 0x02
WH_MAX_OEM_SET_BYTE = 0x03
WH_MAX_INSTALLER_SET_BYTE = 0x04
WH_MAX_OEM_DIFF_BYTE = 0x05
WH_MAX_INSTALLER_DIFF_BYTE = 0x06
WH_CAPACITY_BYTE = 0x07
WH_FUEL_TYPE_BYTE = 0x08
WH_FVS_SENSOR_BYTE = 0x09
WH_FLAME_SENSOR_BYTE = 0x0A
WH_PRESSURE_SWITCH_BYTE = 0x0B
WH_THERMISTOR_COUNT_BYTE = 0x0C
WH_IGNITOR_TYPE_BYTE = 0x0D
WH_GAS_VALVE_BYTE = 0x0E
WH_LIMIT_SWITCH_BYTE = 0x0F
WH_VENT_SWITCH_BYTE = 0x10
WH_CONDENSATE_SWITCH_BYTE = 0x11
WH_LEAK_SENSOR_BYTE = 0x12
WH_COMPRESSOR_BYTE = 0x13
WH_UPPER_ELEMENT_BYTE = 0x19
WH_LOWER_ELEMENT_BYTE = 0x1A
WH_COLLECTOR_PUMP_BYTE = 0x1B
WH_MAX_LOCKOUT_TIME_BYTE = 0x1C
WH_VACATION_MODE_BYTE = 0x1D
WH_SETBACK_MODE_BYTE = 0x1E
WH_INLET_WATER_TEMP_SENSOR_BYTE = 0x1F
WH_HX_OUTLET_TEMP_SENSOR_BYTE = 0x20
WH_MIXED_WATER_TEMP_SENSOR_BYTE = 0x21
WH_INLET_WATER_PRESSURE_SENSOR_BYTE = 0x22
WH_OUTLET_WATER_PRESSURE_SENSOR_BYTE = 0x23
WH_INLET_GAS_PRESSURE_SENSOR_BYTE = 0x24
WH_MANIFOLD_GAS_PRESSURE_SENSOR_BYTE = 0x25
WH_EXHAUST_TEMPERATURE_SENSOR_BYTE = 0x26
WH_INPUT_LINE_VOLTAGE_SENSOR_BYTE = 0x27
WH_COLLECTOR_INLET_TEMP_SENSOR_BYTE = 0x28
WH_COLLECTOR_OUTLET_TEMP_SENSOR_BYTE = 0x29
WH_UPPER_OUTLET_TEMP_SENSOR_BYTE = 0x2A
WH_LOWER_INLET_TEMP_SENSOR_BYTE = 0x2B
WH_MAX_PROG_HOLD_TIME_1_BYTE = 0x31
WH_MAX_PROG_HOLD_TIME_2_BYTE = 0x32
WH_KEYPAD_LOCKOUT_BYTE = 0x33
WH_REAL_TIME_CLOCK_LOCKOUT_BYTE = 0x34
WH_BEEPER_INSTALLED_BYTE = 0x35
WH_COM_FAULT_TIMER_1_BYTE = 0x36
WH_COM_FAULT_TIMER_2_BYTE = 0x37
WH_PROG_PROFILE_TYPE_BYTE = 0x38
WH_PROG_INTERVAL_TYPE_BYTE = 0x39
WH_DAYLIGHT_SAVINGS_AVAIL_BYTE = 0x3A
WH_GMT_OFFSET_BYTE = 0x3B
WH_DISPLAY_CONTRAST_BYTE = 0x3C

CONFIG_0_DB_ID = 0x00
CONFIG_0_LENGTH = 61

CONFIG_1_DB_ID = 0x01
CONFIG_1_LENGTH = 112

CONFIG_2_DB_ID = 0x02
CONFIG_2_LENGTH = 32

CONFIG_3_DB_ID = 0x03
CONFIG_3_LENGTH = 56

CONFIG_4_DB_ID = 0x04
CONFIG_4_LENGTH = 16


class WaterHeater(object):

    def __init__(self, address, subnet, mac_address, session_id, rs485):
        self._rs485 = rs485
        self.address = address
        self.subnet = subnet
        self.mac_address = mac_address
        self.session_id = session_id
        self.__stored_config = None
        self._receive_event = threading.Event()
        self._receive_data = []

    @property
    def schedule(self):
        prog_type = self.program_profile_type
        prog_intv = self.program_interval_type

        if prog_type == WH_PROGRAM_PROFILE_TYPE_7_DAY:
            if prog_intv == WH_PROGRAM_INTERVAL_TYPE_4_STEP:
                return Schedule7(self, CONFIG_1_DB_ID, self._rs485)

            elif prog_intv == WH_PROGRAM_INTERVAL_TYPE_2_STEP:
                return Schedule7(self, CONFIG_3_DB_ID, self._rs485)

        elif prog_type == WH_PROGRAM_PROFILE_TYPE_5_2:
            if prog_intv == WH_PROGRAM_INTERVAL_TYPE_4_STEP:
                return Schedule52(self, CONFIG_2_DB_ID, self._rs485)

            elif prog_intv == WH_PROGRAM_INTERVAL_TYPE_2_STEP:
                return Schedule52(self, CONFIG_4_DB_ID, self._rs485)

    def _packet_callback(self, packet):
        self._receive_data.append(packet)
        self._receive_event.set()

    @property
    def _config(self):
        request = GetConfigurationRequest()
        self._rs485.write(request)

        def _do():
            self._receive_event.wait()
            for packet in self._receive_data[:]:
                if (
                    isinstance(packet, GetConfigurationResponse) and
                    packet.db_id_tag == CONFIG_0_DB_ID
                ):
                    self._receive_data.remove(packet)
                    return bytearray(packet.payload_data)

        data = _do()

        while data is None:
            data = _do()

        return data

    @property
    def _stored_config(self):
        if self.__stored_config is None:
            self.__stored_config = self._config

        return self.__stored_config

    @property
    def type(self):
        """returns one of WH_TYPE_* constants"""
        return self._stored_config[WH_TYPE_BYTE]

    @property
    def application(self):
        """returns on of WH_APPLICATION_* constants"""
        return self._stored_config[WH_APPLICATION_BYTE]

    @property
    def number_of_stages(self):
        return self._stored_config[WH_STAGES_BYTE]

    @property
    def oem_max_allowed_temperature(self):
        return self._stored_config[WH_MAX_OEM_SET_BYTE]

    @property
    def user_max_allowed_temperature(self):
        return self._config[WH_MAX_INSTALLER_SET_BYTE]

    @property
    def oem_max_allowed_differential(self):
        return self._stored_config[WH_MAX_OEM_DIFF_BYTE]

    @property
    def user_max_allowed_differential(self):
        return self._config[WH_MAX_INSTALLER_DIFF_BYTE]

    @property
    def gallon_capacity(self):
        return self._stored_config[WH_CAPACITY_BYTE]

    @property
    def fuel_type(self):
        """returns one of WH_FUEL_TYPE_* constants"""
        return self._stored_config[WH_FUEL_TYPE_BYTE]

    @property
    def has_fvs_sensor(self):
        return self._stored_config[WH_FVS_SENSOR_BYTE]

    @property
    def has_flame_sensor(self):
        return self._stored_config[WH_FLAME_SENSOR_BYTE]

    @property
    def has_pressure_switch(self):
        return self._stored_config[WH_PRESSURE_SWITCH_BYTE]

    @property
    def thermistor_count(self):
        return self._stored_config[WH_THERMISTOR_COUNT_BYTE]

    @property
    def ignitor_type(self):
        """returns one of WH_IGNITER_TYPE_* constants"""

        return self._stored_config[WH_IGNITOR_TYPE_BYTE]

    @property
    def has_gas_valve(self):
        return self._stored_config[WH_GAS_VALVE_BYTE]

    @property
    def has_limit_switch(self):
        return self._stored_config[WH_LIMIT_SWITCH_BYTE]

    @property
    def has_vent_switch(self):
        return self._stored_config[WH_VENT_SWITCH_BYTE]

    @property
    def has_condensate_overflow_switch(self):
        return self._stored_config[WH_CONDENSATE_SWITCH_BYTE]

    @property
    def has_water_leak_sensor(self):
        return self._stored_config[WH_LEAK_SENSOR_BYTE]

    @property
    def has_compressor(self):
        return self._stored_config[WH_COMPRESSOR_BYTE]

    @property
    def has_upper_heating_element(self):
        return self._stored_config[WH_UPPER_ELEMENT_BYTE]

    @property
    def has_lower_heating_element(self):
        return self._stored_config[WH_LOWER_ELEMENT_BYTE]

    @property
    def has_collector_pump(self):
        return self._stored_config[WH_COLLECTOR_PUMP_BYTE]

    @property
    def max_allowed_lockout_time(self):
        """returns 1-254 or one of WH_LOCKOUT_* constants"""
        return self._config[WH_MAX_LOCKOUT_TIME_BYTE]

    @property
    def has_vacation_mode(self):
        return self._stored_config[WH_VACATION_MODE_BYTE]

    @property
    def has_setback_mode(self):
        return self._stored_config[WH_SETBACK_MODE_BYTE]

    @property
    def has_inlet_water_temp_sensor(self):
        return self._stored_config[WH_INLET_WATER_TEMP_SENSOR_BYTE]

    @property
    def has_outlet_water_temp_sensor(self):
        return self._stored_config[WH_HX_OUTLET_TEMP_SENSOR_BYTE]

    @property
    def has_mixed_water_temp_sensor(self):
        return self._stored_config[WH_MIXED_WATER_TEMP_SENSOR_BYTE]

    @property
    def has_inlet_water_pressure_sensor(self):
        return self._stored_config[WH_INLET_WATER_PRESSURE_SENSOR_BYTE]

    @property
    def has_outlet_water_pressure_sensor(self):
        return self._stored_config[WH_OUTLET_WATER_PRESSURE_SENSOR_BYTE]

    @property
    def has_gas_pressure_sensor(self):
        return self._stored_config[WH_INLET_GAS_PRESSURE_SENSOR_BYTE]

    @property
    def has_gas_manifold_pressure_sensor(self):
        return self._stored_config[WH_MANIFOLD_GAS_PRESSURE_SENSOR_BYTE]

    @property
    def has_exhaust_temperature_sensor(self):
        return self._stored_config[WH_EXHAUST_TEMPERATURE_SENSOR_BYTE]

    @property
    def has_input_line_voltage_sensor(self):
        return self._stored_config[WH_INPUT_LINE_VOLTAGE_SENSOR_BYTE]

    @property
    def has_collector_inlet_temp_sensor(self):
        return self._stored_config[WH_COLLECTOR_INLET_TEMP_SENSOR_BYTE]

    @property
    def has_collector_outlet_temp_sensor(self):
        return self._stored_config[WH_COLLECTOR_OUTLET_TEMP_SENSOR_BYTE]

    @property
    def has_upper_outlet_temp_sensor(self):
        return self._stored_config[WH_UPPER_OUTLET_TEMP_SENSOR_BYTE]

    @property
    def has_lower_inlet_temp_sensor(self):
        return self._stored_config[WH_LOWER_INLET_TEMP_SENSOR_BYTE]

    @property
    def max_program_hold_time(self):
        config = self._config

        return config[WH_MAX_PROG_HOLD_TIME_1_BYTE] << 8 | config[WH_MAX_PROG_HOLD_TIME_2_BYTE]

    @property
    def has_keypad_lockout(self):
        return self._stored_config[WH_KEYPAD_LOCKOUT_BYTE]

    @property
    def has_realtime_clock_lockout(self):
        return self._stored_config[WH_REAL_TIME_CLOCK_LOCKOUT_BYTE]

    @property
    def has_beeper(self):
        return self._stored_config[WH_BEEPER_INSTALLED_BYTE]

    @property
    def communications_fault_timer(self):
        config = self._config

        return config[WH_COM_FAULT_TIMER_1_BYTE] << 8 | config[WH_COM_FAULT_TIMER_2_BYTE]

    @property
    def program_profile_type(self):
        """returns one of WH_PROGRAM_PROFILE_TYPE_* constants"""
        return self._stored_config[WH_PROG_PROFILE_TYPE_BYTE]

    @property
    def program_interval_type(self):
        """returns one of WH_PROGRAM_INTERVAL_TYPE_* constants"""
        return self._stored_config[WH_PROG_INTERVAL_TYPE_BYTE]

    @property
    def supports_daylight_savings(self):
        return self._stored_config[WH_DAYLIGHT_SAVINGS_AVAIL_BYTE]

    @property
    def gmt_offset(self):
        return self._config[WH_GMT_OFFSET_BYTE]

    @property
    def display_contrast(self):
        return self._config[WH_DISPLAY_CONTRAST_BYTE]


class ScheduleBase(object):
    def __init__(self, parent, db_id, rs485):
        self._parent = parent
        self._db_id = db_id
        self._rs485 = rs485

    def _config(self, config=None):
        if config is None:
            request = GetConfigurationRequest()
            request.destination = self._parent.address
            request.subnet = self._parent.subnet

            self._rs485.write(request)

            def _do():
                self._parent._receive_event.wait()
                for packet in self._parent._receive_data[:]:
                    if (
                        isinstance(packet, GetConfigurationResponse) and
                        packet.db_id_tag == self._db_id
                    ):
                        self._parent._receive_data.remove(packet)
                        return bytearray(packet.payload_data)

            data = _do()
            while data is None:
                data = _do()

            return data

        else:
            request = SetConfigurationRequest()
            request.destination = self._parent.address
            request.subnet = self._parent.subnet

            self._rs485.write(request)

            def _do():
                self._parent._receive_event.wait()
                for packet in self._parent._receive_data[:]:
                    if (
                        isinstance(packet, SetConfigurationResponse) and
                        packet.db_id_tag == self._db_id
                    ):
                        self._parent._receive_data.remove(packet)
                        return False

                return True

            while _do():
                pass


class Schedule7(ScheduleBase):

    @property
    def monday(self):
        if self._db_id == CONFIG_1_DB_ID:
            return Monday4(self._config, 56)
        else:
            # CONFIG_3_DB_ID
            return Monday2(self._config, 30)

    @property
    def tuesday(self):
        if self._db_id == CONFIG_1_DB_ID:
            return Tuesday4(self._config, 56)
        else:
            # CONFIG_3_DB_ID
            return Tuesday2(self._config, 30)

    @property
    def wednesday(self):
        if self._db_id == CONFIG_1_DB_ID:
            return Wednesday4(self._config, 56)
        else:
            # CONFIG_3_DB_ID
            return Wednesday2(self._config, 30)

    @property
    def thursday(self):
        if self._db_id == CONFIG_1_DB_ID:
            return Thrusday4(self._config, 56)
        else:
            # CONFIG_3_DB_ID
            return Thrusday2(self._config, 30)

    @property
    def friday(self):
        if self._db_id == CONFIG_1_DB_ID:
            return Friday4(self._config, 56)
        else:
            # CONFIG_3_DB_ID
            return Friday2(self._config, 30)

    @property
    def saturday(self):
        if self._db_id == CONFIG_1_DB_ID:
            return Saturday4(self._config, 56)
        else:
            # CONFIG_3_DB_ID
            return Saturday2(self._config, 30)

    @property
    def sunday(self):
        if self._db_id == CONFIG_1_DB_ID:
            return Sunday4(self._config, 56)
        else:
            # CONFIG_3_DB_ID
            return Sunday2(self._config, 30)


class Schedule52(ScheduleBase):

    @property
    def week(self):
        if self._db_id == CONFIG_2_DB_ID:
            return Week4(self._config, 16)
        else:
            # CONFIG_4_DB_ID
            return Week2(self._config, 8)

    @property
    def weekend(self):
        if self._db_id == CONFIG_2_DB_ID:
            return Weekend4(self._config, 16)
        else:
            # CONFIG_4_DB_ID
            return Weekend2(self._config, 8)


class Program2Day(object):
    class TimeBytes(object):
        morning = 0
        afternoon = 0

    class TempBytes(object):
        morning = 0
        afternoon = 0

    _time_bytes = TimeBytes
    _temp_bytes = TempBytes

    def __init__(self, config_func, cool_offset):
        self._config_func = config_func
        self._cool_offset = cool_offset

    @property
    def _config(self):
        return self._config_func()

    @_config.setter
    def _config(self, value):
        self._config_func(value)

    def _get_time(self, byte_num):
        data = self._config[byte_num]

        hour = 0
        for i in range(6, 1, -1):
            _set_bit(hour, i - 2, _get_bit(data, i))

        if _get_bit(data, 0):
            if _get_bit(data, 1):
                minute = 45
            else:
                minute = 15
        elif _get_bit(data, 1):
            minute = 30
        else:
            minute = 0

        return datetime.time(hour=hour, minute=minute)

    def _set_time(self, byte_num, value):
        hour = value.hour
        minute = value.minute

        if minute >= 45:
            data = 3
        elif minute >= 30:
            data = 2
        elif minute >= 15:
            data = 1
        else:
            data = 0

        for i in range(4, -1, -1):
            _set_bit(data, i + 2, _get_bit(hour, i))

        config = self._config
        config[byte_num] = data

        self._config = config

    def _get_temp(self, byte_num):
        return self._config[byte_num]

    def _set_temp(self, byte_num, value):
        pass

    @property
    def morning_heat_start_time(self):
        return self._get_time(self._time_bytes.morning)

    @morning_heat_start_time.setter
    def morning_heat_start_time(self, value):
        self._set_time(self._time_bytes.morning, value)

    @property
    def morning_heat_temp(self):
        return self._get_temp(self._temp_bytes.morning)

    @morning_heat_temp.setter
    def morning_heat_temp(self, value):
        self._set_temp(self._temp_bytes.morning, value)

    @property
    def afternoon_heat_start_time(self):
        return self._get_time(self._time_bytes.afternoon)

    @afternoon_heat_start_time.setter
    def afternoon_heat_start_time(self, value):
        self._set_time(self._time_bytes.afternoon, value)

    @property
    def afternoon_heat_temp(self):
        return self._get_temp(self._temp_bytes.afternoon)

    @afternoon_heat_temp.setter
    def afternoon_heat_temp(self, value):
        self._set_temp(self._temp_bytes.afternoon, value)

    @property
    def morning_cool_start_time(self):
        return self._get_time(self._time_bytes.morning + self._cool_offset)

    @morning_cool_start_time.setter
    def morning_cool_start_time(self, value):
        self._set_time(self._time_bytes.morning + self._cool_offset, value)

    @property
    def morning_cool_temp(self):
        return self._get_temp(self._temp_bytes.morning + self._cool_offset)

    @morning_cool_temp.setter
    def morning_cool_temp(self, value):
        self._set_temp(self._temp_bytes.morning + self._cool_offset, value)

    @property
    def afternoon_cool_start_time(self):
        return self._get_time(self._time_bytes.afternoon + self._cool_offset)

    @afternoon_cool_start_time.setter
    def afternoon_cool_start_time(self, value):
        self._set_time(self._time_bytes.afternoon + self._cool_offset, value)

    @property
    def afternoon_cool_temp(self):
        return self._get_temp(self._temp_bytes.afternoon + self._cool_offset)

    @afternoon_cool_temp.setter
    def afternoon_cool_temp(self, value):
        self._set_temp(self._temp_bytes.afternoon + self._cool_offset, value)


class Program4Day(Program2Day):
    class TimeBytes(object):
        morning = 0
        afternoon = 0
        evening = 0
        night = 0

    class TempBytes(object):
        morning = 0
        afternoon = 0
        evening = 0
        night = 0

    _time_bytes = TimeBytes
    _temp_bytes = TempBytes

    @property
    def evening_heat_start_time(self):
        return self._get_time(self._time_bytes.evening)

    @evening_heat_start_time.setter
    def evening_heat_start_time(self, value):
        self._set_time(self._time_bytes.evening, value)

    @property
    def evening_heat_temp(self):
        return self._get_temp(self._temp_bytes.evening)

    @evening_heat_temp.setter
    def evening_heat_temp(self, value):
        self._set_temp(self._temp_bytes.evening, value)

    @property
    def night_heat_start_time(self):
        return self._get_time(self._time_bytes.night)

    @night_heat_start_time.setter
    def night_heat_start_time(self, value):
        self._set_time(self._time_bytes.night, value)

    @property
    def night_heat_temp(self):
        return self._get_temp(self._temp_bytes.night)

    @night_heat_temp.setter
    def night_heat_temp(self, value):
        self._set_temp(self._temp_bytes.night, value)

    @property
    def evening_cool_start_time(self):
        return self._get_time(self._time_bytes.evening + self._cool_offset)

    @evening_cool_start_time.setter
    def evening_cool_start_time(self, value):
        self._set_time(self._time_bytes.evening + self._cool_offset, value)

    @property
    def evening_cool_temp(self):
        return self._get_temp(self._temp_bytes.evening + self._cool_offset)

    @evening_cool_temp.setter
    def evening_cool_temp(self, value):
        self._set_temp(self._temp_bytes.evening + self._cool_offset, value)

    @property
    def night_cool_start_time(self):
        return self._get_time(self._time_bytes.night + self._cool_offset)

    @night_cool_start_time.setter
    def night_cool_start_time(self, value):
        self._set_time(self._time_bytes.night + self._cool_offset, value)

    @property
    def night_cool_temp(self):
        return self._get_temp(self._temp_bytes.night + self._cool_offset)

    @night_cool_temp.setter
    def night_cool_temp(self, value):
        self._set_temp(self._temp_bytes.night + self._cool_offset, value)


class Monday4(Program4Day):
    class TimeBytes(object):
        morning = 0
        afternoon = 2
        evening = 4
        night = 6

    class TempBytes(object):
        morning = 1
        afternoon = 3
        evening = 5
        night = 7

    _time_bytes = TimeBytes
    _temp_bytes = TempBytes


class Tuesday4(Program4Day):
    class TimeBytes(object):
        morning = 8
        afternoon = 10
        evening = 12
        night = 14

    class TempBytes(object):
        morning = 9
        afternoon = 11
        evening = 13
        night = 15

    _time_bytes = TimeBytes
    _temp_bytes = TempBytes


class Wednesday4(Program4Day):
    class TimeBytes(object):
        morning = 16
        afternoon = 18
        evening = 20
        night = 22

    class TempBytes(object):
        morning = 17
        afternoon = 19
        evening = 21
        night = 23

    _time_bytes = TimeBytes
    _temp_bytes = TempBytes


class Thrusday4(Program4Day):
    class TimeBytes(object):
        morning = 24
        afternoon = 26
        evening = 28
        night = 30

    class TempBytes(object):
        morning = 25
        afternoon = 27
        evening = 29
        night = 31

    _time_bytes = TimeBytes
    _temp_bytes = TempBytes


class Friday4(Program4Day):
    class TimeBytes(object):
        morning = 32
        afternoon = 34
        evening = 36
        night = 38

    class TempBytes(object):
        morning = 33
        afternoon = 35
        evening = 37
        night = 39

    _time_bytes = TimeBytes
    _temp_bytes = TempBytes


class Saturday4(Program4Day):
    class TimeBytes(object):
        morning = 40
        afternoon = 42
        evening = 44
        night = 46

    class TempBytes(object):
        morning = 41
        afternoon = 43
        evening = 45
        night = 47

    _time_bytes = TimeBytes
    _temp_bytes = TempBytes


class Sunday4(Program4Day):
    class TimeBytes(object):
        morning = 48
        afternoon = 50
        evening = 52
        night = 54

    class TempBytes(object):
        morning = 49
        afternoon = 51
        evening = 53
        night = 55

    _time_bytes = TimeBytes
    _temp_bytes = TempBytes


class Monday2(Program4Day):
    class TimeBytes(object):
        morning = 0
        afternoon = 2

    class TempBytes(object):
        morning = 1
        afternoon = 3

    _time_bytes = TimeBytes
    _temp_bytes = TempBytes


class Tuesday2(Program4Day):
    class TimeBytes(object):
        morning = 4
        afternoon = 6

    class TempBytes(object):
        morning = 5
        afternoon = 7

    _time_bytes = TimeBytes
    _temp_bytes = TempBytes


class Wednesday2(Program4Day):
    class TimeBytes(object):
        morning = 8
        afternoon = 10

    class TempBytes(object):
        morning = 9
        afternoon = 11

    _time_bytes = TimeBytes
    _temp_bytes = TempBytes


class Thrusday2(Program4Day):
    class TimeBytes(object):
        morning = 12
        afternoon = 14

    class TempBytes(object):
        morning = 13
        afternoon = 15

    _time_bytes = TimeBytes
    _temp_bytes = TempBytes


class Friday2(Program4Day):
    class TimeBytes(object):
        morning = 16
        afternoon = 18

    class TempBytes(object):
        morning = 17
        afternoon = 19

    _time_bytes = TimeBytes
    _temp_bytes = TempBytes


class Saturday2(Program4Day):
    class TimeBytes(object):
        morning = 20
        afternoon = 22

    class TempBytes(object):
        morning = 21
        afternoon = 23

    _time_bytes = TimeBytes
    _temp_bytes = TempBytes


class Sunday2(Program4Day):
    class TimeBytes(object):
        morning = 24
        afternoon = 26

    class TempBytes(object):
        morning = 25
        afternoon = 29

    _time_bytes = TimeBytes
    _temp_bytes = TempBytes


class Week4(Program4Day):
    class TimeBytes(object):
        morning = 0
        afternoon = 2
        evening = 4
        night = 6

    class TempBytes(object):
        morning = 1
        afternoon = 3
        evening = 5
        night = 7

    _time_bytes = TimeBytes
    _temp_bytes = TempBytes


class Weekend4(Program4Day):
    class TimeBytes(object):
        morning = 8
        afternoon = 10
        evening = 12
        night = 14

    class TempBytes(object):
        morning = 9
        afternoon = 11
        evening = 13
        night = 15

    _time_bytes = TimeBytes
    _temp_bytes = TempBytes


class Week2(Program2Day):
    class TimeBytes(object):
        morning = 0
        afternoon = 2

    class TempBytes(object):
        morning = 1
        afternoon = 3

    _time_bytes = TimeBytes
    _temp_bytes = TempBytes


class Weekend2(Program4Day):
    class TimeBytes(object):
        morning = 4
        afternoon = 6

    class TempBytes(object):
        morning = 5
        afternoon = 7

    _time_bytes = TimeBytes
    _temp_bytes = TempBytes
