# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

import datetime
from .packet import SetControlCommandRequest
from .utils import (
    TwosCompliment,
    get_bit as _get_bit,
    set_bit as _set_bit
)


HEAT_SET_POINT_TEMPERATURE_MODIFY = 0x01
COOL_SET_POINT_TEMPERATURE_MODIFY = 0x02
HEAT_PROFILE_CHANGE = 0x03
COOL_PROFILE_CHANGE = 0x04
SYSTEM_SWITCH_MODIFY = 0x05
PERMANENT_SET_POINT_TEMP_HOLD_MODIFY = 0x06
FAN_KEY_SELECTION = 0x07
HOLD_OVERRIDE = 0x08
BEEPER_ENABLE = 0x09
FAHRENHEIT_CELSIUS_DISPLAY = 0x0C
COMFORT_RECOVERY_MODIFY = 0x0E
REAL_TIME_DAY_OVERRIDE = 0x0F
CHANGE_FILTER_TIME_REMAINING = 0x14
VACATION_MODE = 0x15
HIGH_ALARM_LIMIT_CHANGE = 0x16
LOW_ALARM_LIMIT_CHANGE = 0x17
HIGH_OUTDOOR_ALARM_LIMIT_CHANGE = 0x18
LOW_OUTDOOR_ALARM_LIMIT_CHANGE = 0x19
TEMP_DISPLAY_ADJ_FACTOR_CHANGE = 0x1A
CLEAR_COMPRESSOR_RUN_TIME = 0x2D
RESET_MICRO = 0x31
COMPRESSOR_LOCKOUT = 0x33
HOLD_RELEASE = 0x3D
PROGRAM_INTERVAL_TYPE_MODIFICATION = 0x3E
COMMUNICATIONS_RECEIVER_ON_OFF = 0x3F
FORCE_PHONE_NUMBER_DISPLAY = 0x40
RESTORE_FACTORY_DEFAULTS = 0x45
CUSTOM_MESSAGE_AREA_DISPLAY_DATA = 0x46
SET_POINT_TEMP_AND_TEMPORARY_HOLD = 0x47
CONTINUOUS_DISPLAY_LIGHT = 0x48
ADVANCE_REAL_TIME_DAY_OVERRIDE = 0x4E
KEYPAD_LOCKOUT = 0x4F
TEST_MODE = 0x50
SUBSYSTEM_INSTALLATION_TEST = 0x51
AUTO_PAIRING_REQUEST_1 = 0x52
PAIRING_OWNERSHIP_REQUEST_1 = 0x53
SET_POINT_TEMP_TIME_HOLD = 0x53
COMFORT_MODE_MODIFICATION = 0x55
LIMITED_HEAT_AND_COOL_RANGE = 0x56
AUTO_PAIRING_REQUEST_2 = 0x57
PAIRING_OWNERSHIP_REQUEST_2 = 0x58
REVERSING_VALVE_CONFIG = 0x59
HUM_DEHUM_CONFIG = 0x5A
CHANGE_UV_LIGHT_MAINTENANCE_TIMER = 0x5B
CHANGE_HUMIDIFIER_PAD_MAINT_TIMERALL = 0x5C
DEHUMIDIFICATION_SET_POINT_MODIFY = 0x5D
HUMIDIFICATION_SET_POINT_MODIFY = 0x5E
DAMPER_POSITION_DEMAND = 0x60
SUBSYSTEM_BUSY_STATUS = 0x61
DEHUMIDIFICATION_DEMAND = 0x62
HUMIDIFICATION_DEMAND = 0x63
HEAT_DEMAND = 0x64
COOL_DEMAND = 0x65
FAN_DEMAND = 0x66
BACK_UP_HEAT_DEMAND = 0x67
DEFROST_DEMAND = 0x68
AUX_HEAT_DEMAND = 0x69
SET_MOTOR_SPEED = 0x6A
SET_MOTOR_TORQUE = 0x6B
SET_AIRFLOW_DEMAND = 0x6C
SET_CONTROL_MODE = 0x6D
SET_DEMAND_RAMP_RATE = 0x6E
SET_MOTOR_DIRECTION = 0x6F
SET_MOTOR_TORQUE_PERCENT = 0x70
SET_MOTOR_POSITION_DEMAND = 0x71
SET_BLOWER_COEFFICIENT_1 = 0x72
SET_BLOWER_COEFFICIENT_2 = 0x73
SET_BLOWER_COEFFICIENT_3 = 0x74
SET_BLOWER_COEFFICIENT_4 = 0x75
SET_BLOWER_COEFFICIENT_5 = 0x76
SET_BLOWER_IDENTIFICATION_0 = 0x77
SET_BLOWER_IDENTIFICATION_1 = 0x78
SET_BLOWER_IDENTIFICATION_2 = 0x79
SET_BLOWER_IDENTIFICATION_3 = 0x7A
SET_BLOWER_IDENTIFICATION_4 = 0x7B
SET_BLOWER_IDENTIFICATION_5 = 0x7C
SET_SPEED_LIMIT = 0x7F
SET_TORQUE_LIMIT = 0x80
SET_AIRFLOW_LIMIT = 0x81
SET_POWER_OUTPUT_LIMIT = 0x82
SET_DEVICE_TEMPERATURE_LIMIT = 0x83
STOP_MOTOR_BY_BRAKING = 0x85
RUN_STOP_MOTOR = 0x86
SET_DEMAND_RAMP_TIME = 0x88
SET_INDUCER_RAMP_RATE = 0x89
SET_BLOWER_COEFFICIENT_6 = 0x8A
SET_BLOWER_COEFFICIENT_7 = 0x8B
SET_BLOWER_COEFFICIENT_8 = 0x8C
SET_BLOWER_COEFFICIENT_9 = 0x8D
SET_BLOWER_COEFFICIENT_10 = 0x8E
PUBLISH_PRICE = 0xE0
WATER_HEATER_MODIFY = 0xF0


class ControlCommandRefreshTimer(bytearray):

    @property
    def minutes(self):
        if not len(self):
            self.append(0x00)

        return self[0] >> 4

    @minutes.setter
    def minutes(self, value):
        if not len(self):
            self.append(0x00)

        if value > 15:
            value = 15
        value <<= 4
        value |= self[0] & 0xF

        self.pop(0)
        self.append(value)

    @property
    def seconds(self):
        if not len(self):
            self.append(0x00)

        return (self[0] & 0xF) * 3.75

    @seconds.setter
    def seconds(self, value):
        if not len(self):
            self.append(0x00)

        value /= 3.75
        value = int(round(value))
        value |= (self[0] >> 4) << 4

        self.pop(0)
        self.append(value)


class CommandPacketBase(SetControlCommandRequest):
    _command_code = 0x00
    _payload_length = 0
    _packet_number = 0x00
    _payload = bytearray()
    
    def __init__(self, *args, **kwargs):
        SetControlCommandRequest.__init__(self, *args, **kwargs)

        if len(self) <= 11:
            self.payload_command_code = self._command_code

    @property
    def payload_command_data(self):
        if len(self) == 17:
            return self[12] << 8 | self[13]
        else:
            return self[12]

    @payload_command_data.setter
    def payload_command_data(self, value):

        while len(self) < 12 + len(value):
            self.append(0x00)

        if len(value) == 2:
            self[12] = value >> 8 & 0xFF
            self[13] = value & 0xFF
        else:
            self[12] = value


class HeatSetPointTemperatureModify(CommandPacketBase):
    _command_code = HEAT_SET_POINT_TEMPERATURE_MODIFY
    _payload_length = 1
    
    def set_command_data(self, value):
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


class CoolSetPointTemperatureModify(CommandPacketBase):
    _command_code = COOL_SET_POINT_TEMPERATURE_MODIFY
    _payload_length = 1
    
    def set_command_data(self, value):
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


HEAT_PROFILE_CHANGE_MODE_NON_PROGRMMABLE = 0x00
HEAT_PROFILE_CHANGE_MODE_5_1_1 = 0x01
HEAT_PROFILE_CHANGE_MODE_7 = 0x02
HEAT_PROFILE_CHANGE_MODE_5_2 = 0x03

HEAT_PROFILE_CHANGE_INTERVAL_4_STEP = 0x00
HEAT_PROFILE_CHANGE_INTERVAL_2_STEP = 0x01
HEAT_PROFILE_CHANGE_INTERVAL_NON_PROGRAMMABLE = 0x02


class HeatProfileChange(CommandPacketBase):
    _command_code = HEAT_PROFILE_CHANGE
    _payload_length = 0

    def set_command_data(self, interval, mode, data):
        """
        :param interval: one of HEAT_PROFILE_CHANGE_MODE_* constants
        :param mode: one of HEAT_PROFILE_CHANGE_INTERVAL_* constants
        :param data:
        :return:
        """

        control = 0

        control = _set_bit(control, 0, _get_bit(interval, 0))
        control = _set_bit(control, 1, _get_bit(interval, 1))
        control = _set_bit(control, 2, _get_bit(mode, 0))
        control = _set_bit(control, 3, _get_bit(mode, 1))

        while len(self) < 14 + len(data):
            self.append(0x00)

        self[13] = control

        for i, item in data:
            self[i + 14] = item

        self._payload_length = len(data) + 1


COOL_PROFILE_CHANGE_MODE_NON_PROGRMMABLE = 0x00
COOL_PROFILE_CHANGE_MODE_5_1_1 = 0x01
COOL_PROFILE_CHANGE_MODE_7 = 0x02
COOL_PROFILE_CHANGE_MODE_5_2 = 0x03

COOL_PROFILE_CHANGE_INTERVAL_4_STEP = 0x00
COOL_PROFILE_CHANGE_INTERVAL_2_STEP = 0x01
COOL_PROFILE_CHANGE_INTERVAL_NON_PROGRAMMABLE = 0x02


class CoolProfileChange(CommandPacketBase):
    _command_code = COOL_PROFILE_CHANGE
    _payload_length = 0

    def set_command_data(self, interval, mode, data):
        """
        :param interval: one of COOL_PROFILE_CHANGE_MODE_* constants
        :param mode: one of COOL_PROFILE_CHANGE_INTERVAL_* constants
        :param data:
        :return:
        """

        control = 0

        control = _set_bit(control, 0, _get_bit(interval, 0))
        control = _set_bit(control, 1, _get_bit(interval, 1))
        control = _set_bit(control, 2, _get_bit(mode, 0))
        control = _set_bit(control, 3, _get_bit(mode, 1))

        while len(self) < 14 + len(data):
            self.append(0x00)

        self[13] = control

        for i, item in data:
            self[i + 14] = item

        self._payload_length = len(data) + 1


SYSTEM_SWITCH_MODIFY_OFF = 0x00
SYSTEM_SWITCH_MODIFY_COOL = 0x01
SYSTEM_SWITCH_MODIFY_AUTO = 0x02
SYSTEM_SWITCH_MODIFY_HEAT = 0x03
SYSTEM_SWITCH_MODIFY_BACKUP_HEAT = 0x04


class SystemSwitchModify(CommandPacketBase):
    _command_code = SYSTEM_SWITCH_MODIFY
    _payload_length = 1

    def set_command_data(self, value):
        """
        :param value: one of SYSTEM_SWITCH_MODIFY_* constants
        :return:
        """
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


class PermanentSetPointTempHoldModify(CommandPacketBase):
    _command_code = PERMANENT_SET_POINT_TEMP_HOLD_MODIFY
    _payload_length = 1

    def set_command_data(self, value):
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


FAN_KEY_SELECTION_AUTO = 0x00
FAN_KEY_SELECTION_MANUAL = 0x01


class FanKeySelection(CommandPacketBase):
    _command_code = FAN_KEY_SELECTION
    _payload_length = 1

    def set_command_data(self, state, demand=None):
        """
        :param state: one of FAN_KEY_SELECTION_* constants
        :param demand:
        :return:
        """

        while len(self) < 14:
            self.append(0x00)

        self[13] = state

        if state == FAN_KEY_SELECTION_MANUAL:
            while len(self) < 15:
                self.append(0x00)

            self[14] = demand
            self._payload_length = 2


HOLD_OVERRIDE_ENABLE = 0x01
HOLD_OVERRIDE_DISBALE = 0x00


class HoldOverride(CommandPacketBase):
    _command_code = HOLD_OVERRIDE
    _payload_length = 1

    def set_command_data(self, value):
        """
        :param value: one of HOLD_OVERRIDE_* constants
        :return:
        """
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


BEEPER_ENABLE_TRUE = 0x01
BEEPER_ENABLE_FALSE = 0x00


class BeeperEnable(CommandPacketBase):
    _command_code = BEEPER_ENABLE
    _payload_length = 1

    def set_command_data(self, value):
        """
        :param value: one of BEEPER_ENABLE_* constants
        :return:
        """
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


FAHRENHEIT_CELSIUS_DISPLAY_FAHRENHEIT = 0x01
FAHRENHEIT_CELSIUS_DISPLAY_CELSIUS = 0x00


class FahrenheitCelsiusDisplay(CommandPacketBase):
    _command_code = FAHRENHEIT_CELSIUS_DISPLAY
    _payload_length = 1

    def set_command_data(self, value):
        """
        :param value: one of FAHRENHEIT_CELSIUS_DISPLAY_* constants
        :return:
        """
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


COMFORT_RECOVERY_MODIFY_ENABLE = 0x01
COMFORT_RECOVERY_MODIFY_DISABLE = 0x00


class ComfortRecoveryModify(CommandPacketBase):
    _command_code = COMFORT_RECOVERY_MODIFY
    _payload_length = 1

    def set_command_data(self, capable, state):
        """
        :param capable: True/False
        :param state: one of COMFORT_RECOVERY_MODIFY_* constants
        :return:
        """

        config = 0
        config = _set_bit(config, 0, bool(state))
        config = _set_bit(config, 7, capable)

        while len(self) < 14:
            self.append(0x00)

        self[13] = config


class RealTimeDayOverride(CommandPacketBase):
    _command_code = REAL_TIME_DAY_OVERRIDE
    _payload_length = 6

    def set_command_data(self, value):
        """
        :param value:
        :type value: datetime.datetime
        :return:
        """

        while len(self) < 19:
            self.append(0x00)

        year = value.year - 2000
        month = value.month - 1
        date = value.day
        day = value.weekday()
        hour = value.hour
        minute = value.minute

        self[13] = year
        self[14] = month
        self[15] = date
        self[16] = day
        self[17] = hour
        self[18] = minute


class ChangeFilterTimeRemaining(CommandPacketBase):
    _command_code = CHANGE_FILTER_TIME_REMAINING
    _payload_length = 0

    def set_command_data(self, reset, hours=None):
        while len(self) < 14:
            self.append(0x00)

        self[13] = reset
        self._payload_length = 1

        if hours is not None:
            high_byte = hours >> 8 & 0xFF
            low_byte = hours & 0xFF

            while len(self) < 16:
                self.append(0x00)

            self[14] = low_byte
            self[15] = high_byte

            self._payload_length = 3


VACATION_MODE_ENABLE = 0x01
VACATION_MODE_DISABLE = 0x00


class VacationMode(CommandPacketBase):
    _command_code = VACATION_MODE
    _payload_length = 0

    def set_command_data(self, state, heat_setpoint=None, cool_setpoint=None):
        """
        :param state: one of VACATION_MODE_* constants
        :param heat_setpoint:
        :param cool_setpoint:
        :return:
        """
        while len(self) < 14:
            self.append(0x00)

        self[13] = state

        if None not in (heat_setpoint, cool_setpoint):
            while len(self) < 16:
                self.append(0x00)

            self[14] = heat_setpoint
            self[15] = cool_setpoint


class HighAlarmLimitChange(CommandPacketBase):
    _command_code = HIGH_ALARM_LIMIT_CHANGE
    _payload_length = 1

    def set_command_data(self, value):
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


class LowAlarmLimitChange(CommandPacketBase):
    _command_code = LOW_ALARM_LIMIT_CHANGE
    _payload_length = 1

    def set_command_data(self, value):
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


class HighOutdoorAlarmLimitChange(CommandPacketBase):
    _command_code = HIGH_OUTDOOR_ALARM_LIMIT_CHANGE
    _payload_length = 1

    def set_command_data(self, value):
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


class LowOutdoorAlarmLimitChange(CommandPacketBase):
    _command_code = LOW_OUTDOOR_ALARM_LIMIT_CHANGE
    _payload_length = 1

    def set_command_data(self, value):
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


class TempDisplayAdjFactorChange(CommandPacketBase):
    _command_code = TEMP_DISPLAY_ADJ_FACTOR_CHANGE
    _payload_length = 1

    def set_command_data(self, value):
        """
        :param value: one of COMPRESSOR_LOCKOUT_* constants
        :return:
        """
        while len(self) < 14:
            self.append(0x00)

        self[13] = TwosCompliment.encode(value, 8)


class ClearCompressorRunTime(CommandPacketBase):
    _command_code = CLEAR_COMPRESSOR_RUN_TIME
    _payload_length = 0


class ResetMicro(CommandPacketBase):
    _command_code = RESET_MICRO
    _payload_length = 0


COMPRESSOR_LOCKOUT_ENABLE = 0x01
COMPRESSOR_LOCKOUT_DISABLE = 0x00


class CompressorLockout(CommandPacketBase):
    _command_code = COMPRESSOR_LOCKOUT
    _payload_length = 1

    def set_command_data(self, value):
        """
        :param value: one of COMPRESSOR_LOCKOUT_* constants
        :return:
        """
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


class HoldRelease(CommandPacketBase):
    _command_code = HOLD_RELEASE
    _payload_length = 0


PROGRAM_INTERVAL_TYPE_MODIFICATION_4_STEP = 0x00
PROGRAM_INTERVAL_TYPE_MODIFICATION_2_STEP = 0x01
PROGRAM_INTERVAL_TYPE_MODIFICATION_NON_PROGRAMMABLE = 0x02


class ProgramIntervalTypeModification(CommandPacketBase):
    _command_code = PROGRAM_INTERVAL_TYPE_MODIFICATION
    _payload_length = 1

    def set_command_data(self, value):
        """
        :param value: one of PROGRAM_INTERVAL_TYPE_MODIFICATION_* constants
        :return:
        """
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


COMMUNICATIONS_RECEIVER_ON = 0x01
COMMUNICATIONS_RECEIVER_OFF = 0x00


class CommunicationsReceiverOnOff(CommandPacketBase):
    _command_code = COMMUNICATIONS_RECEIVER_ON_OFF
    _payload_length = 1

    def set_command_data(self, value):
        """
        :param value: COMMUNICATIONS_RECEIVER_ON or COMMUNICATIONS_RECEIVER_OFF
        :return:
        """
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


FORCE_PHONE_NUMBER_DISPLAY_ENABLE = 0x01
FORCE_PHONE_NUMBER_DISPLAY_DISABLE = 0x00


class ForcePhoneNumberDisplay(CommandPacketBase):
    _command_code = FORCE_PHONE_NUMBER_DISPLAY
    _payload_length = 1

    def set_command_data(self, value):
        """
        :param value: one of FORCE_PHONE_NUMBER_DISPLAY_* constants
        :return:
        """
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


class RestoreFactoryDefaults(CommandPacketBase):
    _command_code = RESTORE_FACTORY_DEFAULTS
    _payload_length = 1

    def set_command_data(self):
        while len(self) < 14:
            self.append(0x00)


class CustomMessageAreaDisplayData(CommandPacketBase):
    _command_code = CUSTOM_MESSAGE_AREA_DISPLAY_DATA
    _payload_length = 0

    def set_command_data(self, area_id, duration, blink, reverse, text_id, text=None):
        """
        :param area_id: 0 - 7
        :param duration: 0.0 - 7.5
        :param blink: True/False
        :param reverse: True/False
        :param text_id: 0 - 7
        :param text:
        :return:
        """

        active_id = text_id
        config = int(duration * 2)
        config |= area_id >> 4

        while len(self) < 15:
            self.append(0x00)

        self[13] = config
        self[14] = active_id

        self._payload_length = 2

        if text is not None:
            mod_index = text_id
            mod_index = _set_bit(mod_index, 6, reverse)
            mod_index = _set_bit(mod_index, 7, blink)
            data = bytearray(len(text))

            for char in text:
                if char == '\n':
                    data.append(0x00)
                else:
                    data.append(ord(char))

            while len(self) < 16 + len(data):
                self.append(0x00)

            self[15] = mod_index
            for i, item in enumerate(data):
                self[i + 16] = item

            self._payload_length = 3 + len(data)


class SetPointTempAndTemporaryHold(CommandPacketBase):
    _command_code = SET_POINT_TEMP_AND_TEMPORARY_HOLD
    _payload_length = 1

    def set_command_data(self, value):
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


CONTINUOUS_DISPLAY_LIGHT_ENABLE = 0x01
CONTINUOUS_DISPLAY_LIGHT_DISABLE = 0x02


class ContinuousDisplayLight(CommandPacketBase):
    _command_code = CONTINUOUS_DISPLAY_LIGHT
    _payload_length = 1

    def set_command_data(self, value):
        """
        :param value: one of CONTINUOUS_DISPLAY_LIGHT_* constants
        :return:
        """
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


class AdvanceRealTimeDayOverride(CommandPacketBase):
    _command_code = ADVANCE_REAL_TIME_DAY_OVERRIDE
    _payload_length = 10

    def set_command_data(self, lock, dst, gmt_offset, dt):
        control = 0

        control = _set_bit(control, 7, lock)
        control = _set_bit(control, 0, dst)

        gmt_offset = TwosCompliment.encode(int(gmt_offset * 4), 8)

        s_dt = datetime.datetime(year=2000, month=1, day=1)
        dt -= s_dt
        days = dt.days
        seconds = dt.seconds

        days = [
            days >> 24 & 0xFF,
            days >> 16 & 0xFF,
            days >> 8 & 0xFF,
            days & 0xFF
        ]

        seconds = [
            seconds >> 24 & 0xFF,
            seconds >> 16 & 0xFF,
            seconds >> 8 & 0xFF,
            seconds & 0xFF
        ]

        while len(self) < 23:
            self.append(0x00)

        self[13] = control
        self[14] = gmt_offset
        self[15] = days[0]
        self[16] = days[1]
        self[17] = days[2]
        self[18] = days[3]
        self[19] = seconds[0]
        self[20] = seconds[1]
        self[21] = seconds[2]
        self[22] = seconds[3]


KEYPAD_LOCKOUT_TYPE_FULL = 0x01
KEYPAD_LOCKOUT_TYPE_PARTIAL = 0x00
KEYPAD_LOCKOUT_TYPE_DISABLE = 0xFF


class KeypadLockout(CommandPacketBase):
    _command_code = KEYPAD_LOCKOUT
    _payload_length = 4

    def set_command_data(self, lockout_type, password):
        """
        :param lockout_type: one of KEYPAD_LOCKOUT_TYPE_* constants
        :param password: 1-65535
        :return:
        """

        if lockout_type == KEYPAD_LOCKOUT_TYPE_DISABLE:
            state = 0x00
            lockout_type = 0x00
        else:
            state = 0x01

        high_byte = password >> 8 & 0xFF
        low_byte = password & 0xFF

        while len(self) < 17:
            self.append(0x00)

        self[13] = state
        self[14] = lockout_type
        self[15] = high_byte
        self[16] = low_byte


TEST_MODE_MFG = 0x01
TEST_MODE_CONTROL = 0x02
TEST_MODE_RELIABILITY_PRODUCT = 0x03
TEST_MODE_RELIABILITY_SYSTEM = 0x04
TEST_MODE_OFF = 0xFF


class TestMode(CommandPacketBase):
    _command_code = TEST_MODE
    _payload_length = 2

    def set_command_data(self, mfg_id, code):
        """
        :param mfg_id:
        :param code: one of TEST_MODE_* constants
        :return:
        """
        while len(self) < 15:
            self.append(0x00)

        self[13] = mfg_id
        self[14] = code


SUBSYSTEM_INSTALLATION_TEST_START = 0x01
SUBSYSTEM_INSTALLATION_TEST_STOP = 0x00


class SubsystemInstallationTest(CommandPacketBase):
    _command_code = SUBSYSTEM_INSTALLATION_TEST
    _payload_length = 1

    def set_command_data(self, value):
        """
        :param value: one of SUBSYSTEM_INSTALLATION_TEST_* constants
        :return:
        """
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


class AutoPairingRequest1(CommandPacketBase):
    _command_code = AUTO_PAIRING_REQUEST_1
    _payload_length = 0


class PairingOwnershipRequest1(CommandPacketBase):
    _command_code = PAIRING_OWNERSHIP_REQUEST_1
    _payload_length = 0


class SetPointTempTimeHold(CommandPacketBase):
    _command_code = SET_POINT_TEMP_TIME_HOLD
    _payload_length = 2

    def set_command_data(self, temp, minutes):
        while len(self) < 15:
            self.append(0x00)

        self[13] = temp
        self[14] = minutes


COMFORT_MODE_MODIFICATION_ENABLE = 0x01
COMFORT_MODE_MODIFICATION_DISABLE = 0x00


class ComfortModeModification(CommandPacketBase):
    _command_code = COMFORT_MODE_MODIFICATION
    _payload_length = 1

    def set_command_data(self, value):
        """
        :param value: one of COMFORT_MODE_MODIFICATION_* constants
        :return:
        """
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


class LimitedHeatAndCoolRange(CommandPacketBase):
    _command_code = LIMITED_HEAT_AND_COOL_RANGE
    _payload_length = 2

    def set_command_data(self, min_temp, max_temp):
        while len(self) < 15:
            self.append(0x00)

        self[13] = min_temp
        self[14] = max_temp


AUTO_PAIRING_REQUEST_STATUS_YES = 0x01
AUTO_PAIRING_REQUEST_STATUS_NO = 0x00

AUTO_PAIRING_REQUEST_ACTION_NONE = 0x00
AUTO_PAIRING_REQUEST_ACTION_START = 0x01
AUTO_PAIRING_REQUEST_ACTION_STOP = 0x02
AUTO_PAIRING_REQUEST_ACTION_AUTO = 0xFF


class AutoPairingRequest2(CommandPacketBase):
    _command_code = AUTO_PAIRING_REQUEST_2
    _payload_length = 2

    def set_command_data(self, status_code, action_code):
        """
        :param status_code: one of AUTO_PAIRING_REQUEST_STATUS_* constants
        :param action_code: one of AUTO_PAIRING_REQUEST_ACTION_* constants
        :return:
        """
        while len(self) < 15:
            self.append(0x00)

        self[13] = status_code
        self[14] = action_code


class PairingOwnershipRequest2(CommandPacketBase):
    _command_code = PAIRING_OWNERSHIP_REQUEST_2
    _payload_length = 1

    def set_command_data(self, value):
        """
        :param value: one of REVERSING_VALVE_CONFIG_* constants
        :return:
        """

        while len(self) < 14:
            self.append(0x00)

        self[13] = value


REVERSING_VALVE_CONFIG_O_MODE = 0x00
REVERSING_VALVE_CONFIG_B_MODE = 0x01


class ReversingValveConfig(CommandPacketBase):
    _command_code = REVERSING_VALVE_CONFIG
    _payload_length = 1

    def set_command_data(self, value):
        """
        :param value: on of REVERSING_VALVE_CONFIG_* constants
        :return:
        """
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


class HumDehumConfig(CommandPacketBase):
    _command_code = HUM_DEHUM_CONFIG
    _payload_length = 0

    def set_command_data(self, h_ind, h_mode, d_ind, d_mode):
        while len(self) < 15:
            self.append(0x00)

        h_config = 0
        d_config = 0

        h_config = _set_bit(h_config, 7, h_ind)
        h_config = _set_bit(h_config, 0, h_mode)

        d_config = _set_bit(d_config, 7, d_ind)
        d_config = _set_bit(d_config, 0, d_mode)

        self[13] = h_config
        self[14] = d_config


class ChangeUvLightMaintenanceTimer(CommandPacketBase):
    _command_code = CHANGE_UV_LIGHT_MAINTENANCE_TIMER
    _payload_length = 0

    def set_command_data(self, reset, hours=None):
        while len(self) < 14:
            self.append(0x00)

        self[13] = reset
        self._payload_length = 1

        if hours is not None:
            high_byte = hours >> 8 & 0xFF
            low_byte = hours & 0xFF

            while len(self) < 16:
                self.append(0x00)

            self[14] = low_byte
            self[15] = high_byte

            self._payload_length = 3


class ChangeHumidifierPadMaintTimerall(CommandPacketBase):
    _command_code = CHANGE_HUMIDIFIER_PAD_MAINT_TIMERALL
    _payload_length = 0

    def set_command_data(self, reset, hours=None):
        while len(self) < 14:
            self.append(0x00)

        self[13] = reset
        self._payload_length = 1

        if hours is not None:
            high_byte = hours >> 8 & 0xFF
            low_byte = hours & 0xFF

            while len(self) < 16:
                self.append(0x00)

            self[14] = low_byte
            self[15] = high_byte

            self._payload_length = 3


class DehumidificationSetPointModify(CommandPacketBase):
    _command_code = DEHUMIDIFICATION_SET_POINT_MODIFY
    _payload_length = 0


class HumidificationSetPointModify(CommandPacketBase):
    _command_code = HUMIDIFICATION_SET_POINT_MODIFY
    _payload_length = 0


class DamperPositionDemand(CommandPacketBase):
    _command_code = DAMPER_POSITION_DEMAND
    _payload_length = 2

    def set_command_data(self, refresh_timer, value):
        minute = refresh_timer.minute
        second = refresh_timer.second

        timer = ControlCommandRefreshTimer()

        timer.seconds = second
        timer.minutes = minute

        value = timer + bytearray([int(value * 2)])

        while len(self) < 15:
            self.append(0x00)

        self[13] = value[0]
        self[14] = value[1]


SUBSYSTEM_BUSY_STATUS_BUSY = 0x01
SUBSYSTEM_BUSY_STATUS_READY = 0x00


class SubsystemBusyStatus(CommandPacketBase):
    _command_code = SUBSYSTEM_BUSY_STATUS
    _payload_length = 2

    def set_command_data(self, refresh_timer, value):
        """
        :param refresh_timer:
        :param value: one of SUBSYSTEM_BUSY_STATUS_* constants
        :return:
        """
        minute = refresh_timer.minute
        second = refresh_timer.second

        timer = ControlCommandRefreshTimer()

        timer.seconds = second
        timer.minutes = minute

        value = timer + bytearray([value])

        while len(self) < 15:
            self.append(0x00)

        self[13] = value[0]
        self[14] = value[1]


class DemandBase(CommandPacketBase):
    _command_code = 0x0
    _payload_length = 2

    def set_command_data(self, refresh_timer, value):
        minute = refresh_timer.minute
        second = refresh_timer.second

        timer = ControlCommandRefreshTimer()

        timer.seconds = second
        timer.minutes = minute

        value = timer + bytearray([int(value * 2)])

        while len(self) < 15:
            self.append(0x00)

        self[13] = value[0]
        self[14] = value[1]


class DehumidificationDemand(DemandBase):
    _command_code = DEHUMIDIFICATION_DEMAND


class HumidificationDemand(DemandBase):
    _command_code = HUMIDIFICATION_DEMAND


class HeatDemand(DemandBase):
    _command_code = HEAT_DEMAND


class CoolDemand(DemandBase):
    _command_code = COOL_DEMAND


FAN_DEMAND_MANUAL = 0x00
FAN_DEMAND_COOL = 0x01
FAN_DEMAND_HEAT = 0x02
FAN_DEMAND_AUX_HEAT = 0x03
FAN_DEMAND_EMERGENCY_HEAT = 0x04
FAN_DEMAND_DEFROST = 0x05


class FanDemand(CommandPacketBase):
    _command_code = FAN_DEMAND
    _payload_length = 3

    def set_command_data(self, refresh_timer, mode, value):
        """

        :param refresh_timer:
        :param mode: one of FAN_DEMAND_* constants
        :param value:
        :return:
        """

        while len(self) < 16:
            self.append(0x00)

        minute = refresh_timer.minute
        second = refresh_timer.second

        timer = ControlCommandRefreshTimer()

        timer.seconds = second
        timer.minutes = minute

        value = timer + bytearray([mode, int(value * 2)])

        self[13] = value[0]
        self[14] = value[1]
        self[15] = value[2]


class BackUpHeatDemand(DemandBase):
    _command_code = BACK_UP_HEAT_DEMAND


class DefrostDemand(DemandBase):
    _command_code = DEFROST_DEMAND


class AuxHeatDemand(DemandBase):
    _command_code = AUX_HEAT_DEMAND


class SetMotorSpeed(CommandPacketBase):
    _command_code = SET_MOTOR_SPEED
    _payload_length = 2

    def set_command_data(self, value):
        value *= 4

        high_byte = value >> 8 & 0xFF
        low_byte = value & 0xFF
        while len(self) < 15:
            self.append(0x00)

        self[13] = low_byte
        self[14] = high_byte


class SetMotorTorque(CommandPacketBase):
    _command_code = SET_MOTOR_TORQUE
    _payload_length = 2

    def set_command_data(self, value):
        value *= 2048

        high_byte = value >> 8 & 0xFF
        low_byte = value & 0xFF
        while len(self) < 15:
            self.append(0x00)

        self[13] = low_byte
        self[14] = high_byte


class SetAirflowDemand(CommandPacketBase):
    _command_code = SET_AIRFLOW_DEMAND
    _payload_length = 2

    def set_command_data(self, value):
        value *= 4

        high_byte = value >> 8 & 0xFF
        low_byte = value & 0xFF
        while len(self) < 15:
            self.append(0x00)

        self[13] = low_byte
        self[14] = high_byte


SET_CONTROL_MODE_SPEED = 0x00  # SetMotorSpeed
SET_CONTROL_MODE_TORQUE = 0x01  # SetMotorTorque
SET_CONTROL_MODE_AIRFLOW = 0x02  # SetAirflowDemand


class SetControlMode(CommandPacketBase):
    _command_code = SET_CONTROL_MODE
    _payload_length = 1

    def set_command_data(self, value):
        """
        :param value: on of SET_CONTROL_MODE_* constants
        :return:
        """
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


class SetDemandRampRate(CommandPacketBase):
    _command_code = SET_DEMAND_RAMP_RATE
    _payload_length = 1

    def set_command_data(self, value):
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


SET_MOTOR_DIRECTION_CLOCKWISE = 0x01
SET_MOTOR_DIRECTION_COUNTER_CLOCKWISE = 0x00


class SetMotorDirection(CommandPacketBase):
    _command_code = SET_MOTOR_DIRECTION
    _payload_length = 1

    def set_command_data(self, value):
        """
        :param value: on of SET_MOTOR_DIRECTION_* constants
        :return:
        """
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


class SetMotorTorquePercent(CommandPacketBase):
    _command_code = SET_MOTOR_TORQUE_PERCENT
    _payload_length = 2

    def set_command_data(self, value):
        value *= 65535
        value //= 100

        high_byte = value >> 8 & 0xFF
        low_byte = value & 0xFF
        while len(self) < 15:
            self.append(0x00)

        self[13] = low_byte
        self[14] = high_byte


class SetMotorPositionDemand(CommandPacketBase):
    _command_code = SET_MOTOR_POSITION_DEMAND
    _payload_length = 2

    def set_command_data(self, value):
        high_byte = value >> 8 & 0xFF
        low_byte = value & 0xFF
        while len(self) < 15:
            self.append(0x00)

        self[13] = low_byte
        self[14] = high_byte


class SetBlowerCoefficientBase(CommandPacketBase):
    _command_code = 0x00
    _payload_length = 2

    def set_command_data(self, value):
        high_byte = value >> 8 & 0xFF
        low_byte = value & 0xFF
        while len(self) < 15:
            self.append(0x00)

        self[13] = low_byte
        self[14] = high_byte


class SetBlowerCoefficient1(SetBlowerCoefficientBase):
    _command_code = SET_BLOWER_COEFFICIENT_1


class SetBlowerCoefficient2(SetBlowerCoefficientBase):
    _command_code = SET_BLOWER_COEFFICIENT_2


class SetBlowerCoefficient3(SetBlowerCoefficientBase):
    _command_code = SET_BLOWER_COEFFICIENT_3


class SetBlowerCoefficient4(SetBlowerCoefficientBase):
    _command_code = SET_BLOWER_COEFFICIENT_4


class SetBlowerCoefficient5(SetBlowerCoefficientBase):
    _command_code = SET_BLOWER_COEFFICIENT_5


class SetBlowerIdentificationBase(CommandPacketBase):
    _command_code = 0x00
    _payload_length = 2

    def set_command_data(self, value):
        high_byte = value >> 8 & 0xFF
        low_byte = value & 0xFF
        while len(self) < 15:
            self.append(0x00)

        self[13] = low_byte
        self[14] = high_byte


class SetBlowerIdentification0(SetBlowerIdentificationBase):
    _command_code = SET_BLOWER_IDENTIFICATION_0


class SetBlowerIdentification1(SetBlowerIdentificationBase):
    _command_code = SET_BLOWER_IDENTIFICATION_1


class SetBlowerIdentification2(SetBlowerIdentificationBase):
    _command_code = SET_BLOWER_IDENTIFICATION_2


class SetBlowerIdentification3(SetBlowerIdentificationBase):
    _command_code = SET_BLOWER_IDENTIFICATION_3


class SetBlowerIdentification4(SetBlowerIdentificationBase):
    _command_code = SET_BLOWER_IDENTIFICATION_4


class SetBlowerIdentification5(SetBlowerIdentificationBase):
    _command_code = SET_BLOWER_IDENTIFICATION_5


class SetSpeedLimit(CommandPacketBase):
    _command_code = SET_SPEED_LIMIT
    _payload_length = 2

    def set_command_data(self, value):
        value *= 4

        high_byte = value >> 8 & 0xFF
        low_byte = value & 0xFF
        while len(self) < 15:
            self.append(0x00)

        self[13] = low_byte
        self[14] = high_byte


class SetTorqueLimit(CommandPacketBase):
    _command_code = SET_TORQUE_LIMIT
    _payload_length = 2

    def set_command_data(self, value):
        value *= 2048

        high_byte = value >> 8 & 0xFF
        low_byte = value & 0xFF
        while len(self) < 15:
            self.append(0x00)

        self[13] = low_byte
        self[14] = high_byte


class SetAirflowLimit(CommandPacketBase):
    _command_code = SET_AIRFLOW_LIMIT
    _payload_length = 2

    def set_command_data(self, value):
        value *= 4

        high_byte = value >> 8 & 0xFF
        low_byte = value & 0xFF
        while len(self) < 15:
            self.append(0x00)

        self[13] = low_byte
        self[14] = high_byte


class SetPowerOutputLimit(CommandPacketBase):
    _command_code = SET_POWER_OUTPUT_LIMIT
    _payload_length = 2

    def set_command_data(self, value):
        value *= 2

        high_byte = value >> 8 & 0xFF
        low_byte = value & 0xFF
        while len(self) < 15:
            self.append(0x00)

        self[13] = low_byte
        self[14] = high_byte


class SetDeviceTemperatureLimit(CommandPacketBase):
    _command_code = SET_DEVICE_TEMPERATURE_LIMIT
    _payload_length = 2

    def set_command_data(self, value):
        value *= 128
        value = TwosCompliment.encode(value, 16)

        high_byte = value >> 8 & 0xFF
        low_byte = value & 0xFF
        while len(self) < 15:
            self.append(0x00)

        self[13] = low_byte
        self[14] = high_byte


STOP_MOTOR_BY_BRAKING_ENABLE = 0x01
STOP_MOTOR_BY_BRAKING_DISABLE = 0x02


class StopMotorByBraking(CommandPacketBase):
    _command_code = STOP_MOTOR_BY_BRAKING
    _payload_length = 2

    def set_command_data(self, braking, seconds):
        """
        :param braking: one of STOP_MOTOR_BY_BRAKING_* constants
        :param seconds: time to wait before applying brakes
        :return:
        """
        while len(self) < 15:
            self.append(0x00)

        self[13] = braking
        self[14] = seconds


RUN_STOP_MOTOR_COMMAND_STOP = 0x00
RUN_STOP_MOTOR_COMMAND_RUN = 0x01


class RunStopMotor(CommandPacketBase):
    _command_code = RUN_STOP_MOTOR
    _payload_length = 1

    def set_command_data(self, value):
        """
        :param value: one if RUN_STOP_MOTOR_COMMAND_* constants
        """
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


class SetDemandRampTime(CommandPacketBase):
    _command_code = SET_DEMAND_RAMP_TIME
    _payload_length = 1

    def set_command_data(self, value):
        """
        :param value: seconds
        """
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


class SetInducerRampRate(CommandPacketBase):
    _command_code = SET_INDUCER_RAMP_RATE
    _payload_length = 1

    def set_command_data(self, value):
        """
        :param value:
            0x00: Slew the demand as fast as possible
            0x01-0x7F: Objective Ramp Rate = value RPM/Sec
            0x80: Slew the demand as fast as possible0x81-0xFFObjective speed slew rate = (10*value) RPM/sec
        """
        while len(self) < 14:
            self.append(0x00)

        self[13] = value


class SetBlowerCoefficient6(SetBlowerCoefficientBase):
    _command_code = SET_BLOWER_COEFFICIENT_6


class SetBlowerCoefficient7(SetBlowerCoefficientBase):
    _command_code = SET_BLOWER_COEFFICIENT_7


class SetBlowerCoefficient8(SetBlowerCoefficientBase):
    _command_code = SET_BLOWER_COEFFICIENT_8


class SetBlowerCoefficient9(SetBlowerCoefficientBase):
    _command_code = SET_BLOWER_COEFFICIENT_9


class SetBlowerCoefficient10(SetBlowerCoefficientBase):
    _command_code = SET_BLOWER_COEFFICIENT_10


class PublishPrice(CommandPacketBase):
    _command_code = PUBLISH_PRICE
    _payload_length = 0


class WaterHeaterModify(CommandPacketBase):
    _command_code = WATER_HEATER_MODIFY
    _payload_length = 0
