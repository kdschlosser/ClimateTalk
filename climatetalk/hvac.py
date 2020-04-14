
import datetime

from .utils import (
    set_bit as _set_bit,
    get_bit as _get_bit
)
from .commands import (
    # HVAC commands
    HVAC_HEAT_SET_POINT_TEMPERATURE_MODIFY,
    HVAC_COOL_SET_POINT_TEMPERATURE_MODIFY,
    HVAC_HEAT_PROFILE_CHANGE,
    HVAC_COOL_PROFILE_CHANGE,
    HVAC_SYSTEM_SWITCH_MODIFY,
    HVAC_PERMANENT_SET_POINT_TEMP_HOLD_MODIFY,
    HVAC_FAN_KEY_SELECTION,
    HVAC_HOLD_OVERRIDE,
    HVAC_BEEPER_ENABLE,
    HVAC_FAHRENHEIT_CELSIUS_DISPLAY,
    HVAC_COMFORT_RECOVERY_MODIFY,
    HVAC_REAL_TIME_DAY_OVERRIDE,
    HVAC_CHANGE_FILTER_TIME_REMAINING,
    HVAC_VACATION_MODE,
    HVAC_HIGH_ALARM_LIMIT_CHANGE,
    HVAC_LOW_ALARM_LIMIT_CHANGE,
    HVAC_HIGH_OUTDOOR_ALARM_LIMIT_CHANGE,
    HVAC_LOW_OUTDOOR_ALARM_LIMIT_CHANGE,
    HVAC_TEMP_DISPLAY_ADJ_FACTOR_CHANGE,
    HVAC_CLEAR_COMPRESSOR_RUN_TIME,
    HVAC_RESET_MICRO,
    HVAC_COMPRESSOR_LOCKOUT,
    HVAC_HOLD_RELEASE,
    HVAC_PROGRAM_INTERVAL_TYPE_MODIFICATION,
    HVAC_COMMUNICATIONS_RECEIVER_ON_OFF,
    HVAC_FORCE_PHONE_NUMBER_DISPLAY,
    HVAC_RESTORE_FACTORY_DEFAULTS,
    HVAC_CUSTOM_MESSAGE_AREA_DISPLAY_DATA,
    HVAC_SET_POINT_TEMP_AND_TEMPORARY_HOLD,
    HVAC_CONTINUOUS_DISPLAY_LIGHT,
    HVAC_ADVANCE_REAL_TIME_DAY_OVERRIDE,
    HVAC_KEYPAD_LOCKOUT,
    HVAC_TEST_MODE,
    HVAC_SUBSYSTEM_INSTALLATION_TEST,
    HVAC_SET_POINT_TEMP_TIME_HOLD,
    HVAC_COMFORT_MODE_MODIFICATION,
    HVAC_LIMITED_HEAT_AND_COOL_RANGE,
    HVAC_AUTO_PAIRING_REQUEST,
    HVAC_PAIRING_OWNERSHIP_REQUEST,
    HVAC_REVERSING_VALVE_CONFIG,
    HVAC_HUM_DEHUM_CONFIG,
    HVAC_CHANGE_UV_LIGHT_MAINTENANCE_TIMER,
    HVAC_CHANGE_HUMIDIFIER_PAD_MAINT_TIMERALL,
    HVAC_DAMPER_CLOSURE_POSITION_DEMAND,
    HVAC_SUBSYSTEM_BUSY_STATUS,
    HVAC_DEHUMIDIFICATION_DEMAND,
    HVAC_HUMIDIFICATION_DEMAND,
    HVAC_HEAT_DEMAND,
    HVAC_COOL_DEMAND,
    HVAC_FAN_DEMAND,
    HVAC_BACK_UP_HEAT_DEMAND,
    HVAC_DEFROST_DEMAND,
    HVAC_AUX_HEAT_DEMAND,
    HVAC_SET_MOTOR_SPEED,
    HVAC_SET_MOTOR_TORQUE,
    HVAC_SET_AIRFLOW_DEMAND,
    HVAC_SET_MODE,
    HVAC_SET_DEMAND_RAMP_RATE,
    HVAC_SET_MOTOR_DIRECTION,
    HVAC_SET_MOTOR_TORQUE_PERCENT,
    HVAC_SET_MOTOR_POSITION_DEMAND,
    HVAC_SET_BLOWER_COEFFICIENT_1,
    HVAC_SET_BLOWER_COEFFICIENT_2,
    HVAC_SET_BLOWER_COEFFICIENT_3,
    HVAC_SET_BLOWER_COEFFICIENT_4,
    HVAC_SET_BLOWER_COEFFICIENT_5,
    HVAC_SET_BLOWER_IDENTIFICATION_0,
    HVAC_SET_BLOWER_IDENTIFICATION_1,
    HVAC_SET_BLOWER_IDENTIFICATION_2,
    HVAC_SET_BLOWER_IDENTIFICATION_3,
    HVAC_SET_BLOWER_IDENTIFICATION_4,
    HVAC_SET_BLOWER_IDENTIFICATION_5,
    HVAC_SET_SPEED_LIMIT,
    HVAC_SET_TORQUE_LIMIT,
    HVAC_SET_AIRFLOW_LIMIT,
    HVAC_SET_POWER_OUTPUT_LIMIT,
    HVAC_SET_DEVICE_TEMPERATURE_LIMIT,
    HVAC_STOP_MOTOR_BY_BRAKING,
    HVAC_RUN_STOP_MOTOR,
    HVAC_SET_DEMAND_RAMP_TIME,
    HVAC_SET_INDUCER_RAMP_RATE,
    HVAC_SET_BLOWER_COEFFICIENT_6,
    HVAC_SET_BLOWER_COEFFICIENT_7,
    HVAC_SET_BLOWER_COEFFICIENT_8,
    HVAC_SET_BLOWER_COEFFICIENT_9,
    HVAC_SET_BLOWER_COEFFICIENT_10,
    HVAC_PUBLISH_PRICE,
)
from .packet import (SetControlCommandRequest, SetControlCommandResponse)


HVAC_PROGRAM_PROFILE_TYPE_NON_PROGRAMMABLE = 0x00
HVAC_PROGRAM_PROFILE_TYPE_7_DAY = 0x02
HVAC_PROGRAM_PROFILE_TYPE_5_2 = 0x03
HVAC_PROGRAM_PROFILE_TYPE_5_1_1 = 0x01

HVAC_PROGRAM_INTERVAL_TYPE_NON_PROGRAMMABLE = 0x03
HAVC_PROGRAM_INTERVAL_TYPE_2_STEP = 0x01
HAVC_PROGRAM_INTERVAL_TYPE_4_STEP = 0x00


HVAC_OPERATING_MODE_OFF = 0x00
HVAC_OPERATING_MODE_COOL = 0x01
HVAC_OPERATING_MODE_AUTO = 0x02
HVAC_OPERATING_MODE_HEAT = 0x03
HVAC_OPERATING_MODE_BACKUP_HEAT = 0x04


# To set the Fan mode to manual you need to specify
# the speed of the fan. Ranging from 0x00 (0%) to 0x64 (100%)
HVAC_FAN_MODE_AUTO = 0xFF
HVAC_FAN_MODE_LOW = 0x14  # 20%
HVAC_FAN_MODE_MEDIUM_LOW = 0x28  # 40%
HVAC_FAN_MODE_MEDIUM = 0x3C  # 60%
HVAC_FAN_MODE_MEDIUM_HIGH = 0x50  # 80%
HVAC_FAN_MODE_HIGH = 0x64  # 100%

_FAN_MODE_AUTO = 0x00
_FAN_MODE_MANUAL = 0x01

HVAC_DISPLAY_CELSIUS = 0x00
HVAC_DISPLAY_FAHRENHEIT = 0x01

HVAC_LOCK_TYPE_FULL = 0x01
HVAC_LOCK_TYPE_PARTIAL = 0x00

HVAC_TEST_MODE_MANUFACTURING = 0x01
HVAC_TEST_MODE_CONTROL = 0x02
HVAC_TEST_MODE_RELIABILITY_PRODUCT = 0x03
HVAC_TEST_MODE_RELIABILITY_SYSTEM = 0x04
HVAC_TEST_MODE_OFF = 0xFF

HVAC_ENABLE = 0x01
HVAC_DISABLE = 0x00


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


class HVAC(object):

    def __init__(self, address, subnet, mac_address, session_id, rs485):
        self.address = address
        self.subnet = subnet
        self.mac_address = mac_address
        self.session_id = session_id
        self._rs485 = rs485

    def _send(self, command, data):
        request = SetControlCommandRequest()
        request.payload_command_code = command
        request.payload_command_data = data

    @property
    def heat_setpoint(self):
        pass

    @heat_setpoint.setter
    def heat_setpoint(self, value):
        self._send(HVAC_HEAT_SET_POINT_TEMPERATURE_MODIFY, bytearray([value]))

    @property
    def cool_setpoint(self):
        pass

    @cool_setpoint.setter
    def cool_setpoint(self, value):
        self._send(HVAC_COOL_SET_POINT_TEMPERATURE_MODIFY, bytearray([value]))

    @property
    def operating_mode(self):
        """
        :return: one of HVAC_OPERATING_MODE_* constants
        """
        pass

    @operating_mode.setter
    def operating_mode(self, value):
        """
        :param value: one of HVAC_OPERATING_MODE_* constants
        :return:
        """

        self._send(HVAC_SYSTEM_SWITCH_MODIFY, bytearray([value]))

    @property
    def hold_temp(self):
        pass

    @hold_temp.setter
    def hold_temp(self, value):
        self._send(HVAC_PERMANENT_SET_POINT_TEMP_HOLD_MODIFY, bytearray([value]))

    @property
    def fan_mode(self):
        pass

    @fan_mode.setter
    def fan_mode(self, value):
        if value == HVAC_FAN_MODE_AUTO:
            value = bytearray([_FAN_MODE_AUTO])
        else:
            if value < 0x00:
                value = 0x00
            elif value > HVAC_FAN_MODE_HIGH:
                value = HVAC_FAN_MODE_HIGH
                value = bytearray([_FAN_MODE_MANUAL, value])

        self._send(HVAC_FAN_KEY_SELECTION, value)


    @property
    def hold_override(self):
        pass

    @hold_override.setter
    def hold_override(self, value):
        """
        :param value: HVAC_ENABLE or HVAC_DISABLE
        :return:
        """
        self._send(HVAC_HOLD_OVERRIDE, bytearray([value]))

    @property
    def beep_enable(self):
        pass

    @beep_enable.setter
    def beep_enable(self, value):
        """
        :param value: HVAC_ENABLE or HVAC_DISABLE
        :return:
        """
        self._send(HVAC_BEEPER_ENABLE, bytearray([value]))

    @property
    def display_scale(self):
        pass

    @display_scale.setter
    def display_scale(self, value):
        """
        :param value:  one of the HVAC_DISPLAY_* constants
        :return:
        """
        self._send(HVAC_FAHRENHEIT_CELSIUS_DISPLAY, bytearray([value]))

    @property
    def comfort_recovery(self):
        pass

    @comfort_recovery.setter
    def comfort_recovery(self, value):
        """
        :param value: HVAC_ENABLE OR HVAC_DISABLE
        :return:
        """
        val = _set_bit(value, 7, True)
        self._send(HVAC_COMFORT_RECOVERY_MODIFY, bytearray([val]))

    @property
    def override_date_time(self):
        pass

    @override_date_time.setter
    def override_date_time(self, value):
        """
        :param value: datetime.datetime
        :return:
        """
        year = value.year - 2000
        month = value.month - 1
        date = value.day
        day = value.weekday
        hour = value.hour
        minute = value.minute

        self._send(HVAC_REAL_TIME_DAY_OVERRIDE, bytearray([year, month, date, day, hour, minute]))

    @property
    def filter_time(self):
        pass

    @filter_time.setter
    def filter_time(self, value):
        if value:
            value_1 = value >> 8 & 0xFF
            value_2 = value & 0xFF
            value = bytearray([0x00, value_1, value_2])
        else:
            value = bytearray([0x01])

        self._send(HVAC_CHANGE_FILTER_TIME_REMAINING, value)

    @property
    def vacation_mode(self):
        pass

    @vacation_mode.setter
    def vacation_mode(self, value):
        """
        :param value: HVAC_ENABLE or HVAC_DISABLE
        :return:
        """
        self._send(HVAC_VACATION_MODE, bytearray([value]))

    @property
    def vacation_mode_heat_setpoint(self):
        pass

    @vacation_mode_heat_setpoint.setter
    def vacation_mode_heat_setpoint(self, value):
        self._send(HVAC_VACATION_MODE, bytearray([self.vacation_mode, value, self.vacation_mode_cool_setpoint]))

    @property
    def vacation_mode_cool_setpoint(self):
        pass

    @vacation_mode_cool_setpoint.setter
    def vacation_mode_cool_setpoint(self, value):
        self._send(HVAC_VACATION_MODE, bytearray([self.vacation_mode, self.vacation_mode_heat_setpoint, value]))

    @property
    def high_alarm_temp(self):
        pass

    @high_alarm_temp.setter
    def high_alarm_temp(self, value):
        self._send(HVAC_HIGH_ALARM_LIMIT_CHANGE, bytearray([value]))

    @property
    def low_alarm_temp(self):
        pass

    @low_alarm_temp.setter
    def low_alarm_temp(self, value):
        self._send(HVAC_LOW_ALARM_LIMIT_CHANGE, bytearray([value]))

    @property
    def high_alarm_outdoor_temp(self):
        pass

    @high_alarm_outdoor_temp.setter
    def high_alarm_outdoor_temp(self, value):
        self._send(HVAC_HIGH_OUTDOOR_ALARM_LIMIT_CHANGE, bytearray([value]))

    @property
    def low_alarm_outdoor_temp(self):
        pass

    @low_alarm_outdoor_temp.setter
    def low_alarm_outdoor_temp(self, value):
        self._send(HVAC_LOW_OUTDOOR_ALARM_LIMIT_CHANGE, bytearray([value]))

    @property
    def display_temp_offset(self):
        pass

    @display_temp_offset.setter
    def display_temp_offset(self, value):
        self._send(HVAC_TEMP_DISPLAY_ADJ_FACTOR_CHANGE, bytearray([value]))

    def clear_compressor_runtime(self):
        self._send(HVAC_CLEAR_COMPRESSOR_RUN_TIME, bytearray())

    def reset_system(self):
        self._send(HVAC_RESET_MICRO, bytearray())

    @property
    def compressor_lockout(self):
        pass

    @compressor_lockout.setter
    def compressor_lockout(self, value):
        """
        :param value: HVAC_ENABLE or HVAC_DISABLE
        :return:
        """
        self._send(HVAC_COMPRESSOR_LOCKOUT, bytearray([value]))

    def release_hold(self):
        self._send(HVAC_HOLD_RELEASE, bytearray())

    @property
    def program_interval_type(self):
        pass

    @program_interval_type.setter
    def program_interval_type(self, value):
        """
        :return: one of HAVC_PROGRAM_INTERVAL_TYPE_* constants
        """
        self._send(HVAC_PROGRAM_INTERVAL_TYPE_MODIFICATION, bytearray([value]))

    @property
    def communications_receiver(self):
        pass

    @communications_receiver.setter
    def communications_receiver(self, value):
        """
        :param value: HVAC_ENABLE or HVAC_DISABLE
        :return:
        """
        self._send(HVAC_COMMUNICATIONS_RECEIVER_ON_OFF, bytearray([value]))

    @property
    def force_phone_number_display(self):
        pass

    @force_phone_number_display.setter
    def force_phone_number_display(self, value):
        """
        :param value: HVAC_ENABLE or HVAC_DISABLE
        :return:
        """
        self._send(HVAC_FORCE_PHONE_NUMBER_DISPLAY, bytearray([value]))

    def restore_factory_daults(self):
        self._send(HVAC_RESTORE_FACTORY_DEFAULTS, bytearray([0x00]))

    @property
    def display_light_continious(self):
        pass

    @display_light_continious.setter
    def display_light_continious(self, value):
        """
        :param value: HVAC_ENABLE or HVAC_DISABLE
        :return:
        """
        self._send(HVAC_CONTINUOUS_DISPLAY_LIGHT, bytearray([value]))

    def set_date_time(self, dt, gmt_offset, dst=False, lock=False):
        control = 0
        gmt_offset *= 4

        control = _set_bit(control, 7, lock)
        control = _set_bit(control, 0, dst)

        dt1 = datetime.datetime(month=1, day=1, year=2000)
        dt -= dt1
        days = dt.days
        seconds = dt.seconds

        days = bytearray([
            days >> 24 & 0xFF,
            days >> 16 & 0xFF,
            days >> 8 & 0xFF,
            days & 0xFF
        ])
        seconds = bytearray([
            seconds >> 24 & 0xFF,
            seconds >> 16 & 0xFF,
            seconds >> 8 & 0xFF,
            seconds & 0xFF
        ])

        payload = bytearray([control, gmt_offset]) + days + seconds

        self._send(HVAC_ADVANCE_REAL_TIME_DAY_OVERRIDE, payload)

    def lock_keypad(self, state, lock_type, password):
        """
        :param state: HVAC_ENABLE or HVAC_DISABLE
        :param lock_type: one of HVAC_LOCK_TYPE_* constants
        :param password: a password between 0 and 65535, the master pasword is always 00000
        :return:
        """

        payload = bytearray([state, lock_type, password])
        self._send(HVAC_KEYPAD_LOCKOUT, payload)


    def test_mode(self, mfg_id, test_code):
        """
        :param mfg_id: the manufacturers id.
        :param test_code: one of HVAC_TEST_MODE_* constants
        :return:
        """

        payload = bytearray([
            mfg_id >> 8 & 0xFF
            mfg_id & 0xFF,
            test_code
        ])
        self._send(HVAC_TEST_MODE, payload)

    def subsystem_installation_test(self, state):
        """
        :param state: HVAC_ENABLE or HVAC_DISABLE
        :return:
        """

        self._send(HVAC_SUBSYSTEM_INSTALLATION_TEST, bytearray([state]))

    def temp_hold_with_duration(self, temp, minutes):
        payload = bytearray([
            temp,
            minutes >> 8 & 0xFF,
            minutes & 0xFF
        ])
        self._send(HVAC_SET_POINT_TEMP_AND_TEMPORARY_HOLD, payload)

    @property
    def comfort_mode(self):
        pass

    @comfort_mode.setter
    def comfort_mode(self, value):
        """
        :param value: HVAC_ENABLE or HVAC_DISABLE
        :return:
        """

        self._send(HVAC_COMFORT_MODE_MODIFICATION, bytearray([value]))

    @property
    def temperature_range(self):
        pass

    @temperature_range.setter
    def temperature_range(self, value):
        """
        :param value: tuple (min temp, max temp)
        :return:
        """

        min_temp, max_temp = value
        self._send(HVAC_LIMITED_HEAT_AND_COOL_RANGE, bytearray([min_temp, max_temp]))
