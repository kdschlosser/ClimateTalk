# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_GAS_FURNACE = NodeType(0x02).set_desc('Gas Furnace')




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

from ..commands import (
    AdvanceRealTimeDayOverride,
    AutoPairingRequest1,
    AutoPairingRequest2,
    AuxHeatDemand,
    BackUpHeatDemand,
    BeeperEnable,
    ChangeFilterTimeRemaining,
    ChangeHumidifierPadMaintTimerall,
    ChangeUvLightMaintenanceTimer,
    ClearCompressorRunTime,
    ComfortModeModification,
    ComfortRecoveryModify,
    CommunicationsReceiverOnOff,
    CompressorLockout,
    ContinuousDisplayLight,
    CoolDemand,
    CoolProfileChange,
    CoolSetPointTemperatureModify,
    CustomMessageAreaDisplayData,
    DamperPositionDemand,
    DefrostDemand,
    DehumidificationDemand,
    DehumidificationSetPointModify,
    FahrenheitCelsiusDisplay,
    FanDemand,
    ForcePhoneNumberDisplay,
    HeatDemand,
    HeatProfileChange,
    HeatSetPointTemperatureModify,
    HighAlarmLimitChange,
    HighOutdoorAlarmLimitChange,
    HoldRelease,
    HumDehumConfig,
    HumidificationDemand,
    HumidificationSetPointModify,
    HoldOverride,
    KeypadLockout,
    LimitedHeatAndCoolRange,
    LowAlarmLimitChange,
    LowOutdoorAlarmLimitChange,
    PairingOwnershipRequest1,
    PairingOwnershipRequest2,
    PermanentSetPointTempHoldModify,
    ProgramIntervalTypeModification,
    PublishPrice,
    RealTimeDayOverride,
    ResetMicro,
    RestoreFactoryDefaults,
    ReversingValveConfig,
    RunStopMotor,
    SetAirflowDemand,
    SetAirflowLimit,
    SetBlowerCoefficient1,
    SetBlowerCoefficient10,
    SetBlowerCoefficient2,
    SetBlowerCoefficient3,
    SetBlowerCoefficient4,
    SetBlowerCoefficient5,
    SetBlowerCoefficient6,
    SetBlowerCoefficient7,
    SetBlowerCoefficient8,
    SetBlowerCoefficient9,
    SetBlowerCoefficientBase,
    SetBlowerIdentification0,
    SetBlowerIdentification1,
    SetBlowerIdentification2,
    SetBlowerIdentification3,
    SetBlowerIdentification4,
    SetBlowerIdentification5,
    SetBlowerIdentificationBase,
    SetControlMode,
    SetDemandRampRate,
    SetDemandRampTime,
    SetDeviceTemperatureLimit,
    SetInducerRampRate,
    SetMotorDirection,
    SetMotorPositionDemand,
    SetMotorSpeed,
    SetMotorTorque,
    SetMotorTorquePercent,
    SetPointTempAndTemporaryHold,
    SetPointTempTimeHold,
    SetPowerOutputLimit,
    SetSpeedLimit,
    SetTorqueLimit,
    StopMotorByBraking,
    SubsystemBusyStatus,
    SubsystemInstallationTest,
    ,
    TempDisplayAdjFactorChange,
    TestMode,
    VacationMode,
    WaterHeaterModify,
)


from ..commands import (
SystemSwitchModify,
    HeatSetPointTemperatureModify,
    CoolSetPointTemperatureModify,
    PermanentSetPointTempHoldModify,
    HoldOverride,
    RealTimeDayOverride,
    HeatProfileChange,
    CoolProfileChange,
    FanKeySelection,
    SubsystemInstallationTest,




    RestoreFactoryDefaults,
    TestMode,
    SubsystemBusyStatus,
    DehumidificationDemand,
    HumidificationDemand,
    HeatDemand,
    CoolDemand,
    FanDemand,
    BackUpHeatDemand,
    DefrostDemand,
    AuxHeatDemand
)




class FurnaceGas(Node):
    node_type = NODE_TYPE_GAS_FURNACE

    def _send(self, packet):
        request.payload_command_code = command
        request.payload_command_data = data

    @property
    def heat_setpoint(self):
        pass

    @heat_setpoint.setter
    def heat_setpoint(self, value):
        packet = HeatSetPointTemperatureModify()
        packet.set_command_data(value)

        self._send(packet)

    @property
    def cool_setpoint(self):
        pass

    @cool_setpoint.setter
    def cool_setpoint(self, value):
        packet = CoolSetPointTemperatureModify()
        packet.set_command_data(value)

        self._send(packet)

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
        SetControlMode

    @property
    def hold_temp(self):
        pass

    @hold_temp.setter
    def hold_temp(self, value):
        PermanentSetPointTempHoldModify

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

        FanKeySelection

    @property
    def hold_override(self):
        pass

    @hold_override.setter
    def hold_override(self, value):
        """
        :param value: HVAC_ENABLE or HVAC_DISABLE
        :return:
        """
        HoldOverride

    @property
    def beep_enable(self):
        pass

    @beep_enable.setter
    def beep_enable(self, value):
        """
        :param value: HVAC_ENABLE or HVAC_DISABLE
        :return:
        """
        BeeperEnable

    @property
    def display_scale(self):
        pass

    @display_scale.setter
    def display_scale(self, value):
        """
        :param value:  one of the HVAC_DISPLAY_* constants
        :return:
        """
        FahrenheitCelsiusDisplay

    @property
    def comfort_recovery(self):
        pass

    @comfort_recovery.setter
    def comfort_recovery(self, value):
        """
        :param value: HVAC_ENABLE OR HVAC_DISABLE
        :return:
        """
        ComfortRecoveryModify
        val = _set_bit(value, 7, True)

    @property
    def override_date_time(self):
        pass

    @override_date_time.setter
    def override_date_time(self, value):
        """
        :param value: datetime.datetime
        :return:
        """
        RealTimeDayOverride

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

        ChangeFilterTimeRemaining

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
        VacationMode

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
        HighAlarmLimitChange
        self._send(HVAC_HIGH_ALARM_LIMIT_CHANGE, bytearray([value]))

    @property
    def low_alarm_temp(self):
        pass

    @low_alarm_temp.setter
    def low_alarm_temp(self, value):
        LowAlarmLimitChange
        self._send(HVAC_LOW_ALARM_LIMIT_CHANGE, bytearray([value]))

    @property
    def high_alarm_outdoor_temp(self):
        pass

    @high_alarm_outdoor_temp.setter
    def high_alarm_outdoor_temp(self, value):
        HighOutdoorAlarmLimitChange


        self._send(HVAC_HIGH_OUTDOOR_ALARM_LIMIT_CHANGE, bytearray([value]))

    @property
    def low_alarm_outdoor_temp(self):
        pass

    @low_alarm_outdoor_temp.setter
    def low_alarm_outdoor_temp(self, value):
        LowOutdoorAlarmLimitChange
        self._send(HVAC_LOW_OUTDOOR_ALARM_LIMIT_CHANGE, bytearray([value]))

    @property
    def display_temp_offset(self):
        pass

    @display_temp_offset.setter
    def display_temp_offset(self, value):
        TempDisplayAdjFactorChange
        self._send(HVAC_TEMP_DISPLAY_ADJ_FACTOR_CHANGE, bytearray([value]))

    def clear_compressor_runtime(self):
        ClearCompressorRunTime

        self._send(HVAC_CLEAR_COMPRESSOR_RUN_TIME, bytearray())

    def reset_system(self):
        ResetMicro
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
        CompressorLockout
        self._send(HVAC_COMPRESSOR_LOCKOUT, bytearray([value]))

    def release_hold(self):
        HoldRelease
        self._send(HVAC_HOLD_RELEASE, bytearray())

    @property
    def program_interval_type(self):
        pass

    @program_interval_type.setter
    def program_interval_type(self, value):
        """
        :return: one of HAVC_PROGRAM_INTERVAL_TYPE_* constants
        """
        ProgramIntervalTypeModification
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
        CommunicationsReceiverOnOff
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
        ForcePhoneNumberDisplay
        self._send(HVAC_FORCE_PHONE_NUMBER_DISPLAY, bytearray([value]))

    def restore_factory_daults(self):
        RestoreFactoryDefaults
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
        ContinuousDisplayLight
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
        AdvanceRealTimeDayOverride
        self._send(HVAC_ADVANCE_REAL_TIME_DAY_OVERRIDE, payload)

    def lock_keypad(self, state, lock_type, password):
        """
        :param state: HVAC_ENABLE or HVAC_DISABLE
        :param lock_type: one of HVAC_LOCK_TYPE_* constants
        :param password: a password between 0 and 65535, the master pasword is always 00000
        :return:
        """
        KeypadLockout
        payload = bytearray([state, lock_type, password])
        self._send(HVAC_KEYPAD_LOCKOUT, payload)


    def test_mode(self, mfg_id, test_code):
        """
        :param mfg_id: the manufacturers id.
        :param test_code: one of HVAC_TEST_MODE_* constants
        :return:
        """
        TestMode
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
        SubsystemInstallationTest
        self._send(HVAC_SUBSYSTEM_INSTALLATION_TEST, bytearray([state]))

    def temp_hold_with_duration(self, temp, minutes):
        payload = bytearray([
            temp,
            minutes >> 8 & 0xFF,
            minutes & 0xFF
        ])
        SetPointTempAndTemporaryHold
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
        ComfortModeModification
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
        LimitedHeatAndCoolRange
        min_temp, max_temp = value
        self._send(HVAC_LIMITED_HEAT_AND_COOL_RANGE, bytearray([min_temp, max_temp]))


