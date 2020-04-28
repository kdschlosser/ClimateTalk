# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser


import datetime
import threading
from ..utils import (
    get_bit as _get_bit,
    set_bit as _set_bit,
    TwosCompliment
)

from ..packet import (
    GetConfigurationRequest,
    GetStatusRequest
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
    BeeperEnable,
    FahrenheitCelsiusDisplay,
    ComfortRecoveryModify,
    ChangeFilterTimeRemaining,
    VacationMode,
    TempDisplayAdjFactorChange,
    CompressorLockout,
    CustomMessageAreaDisplayData,
    SetPointTempAndTemporaryHold,
    ContinuousDisplayLight,
    AdvanceRealTimeDayOverride,
    KeypadLockout,
    SetPointTempTimeHold,
    ComfortModeModification,
    LimitedHeatAndCoolRange,
    ChangeUvLightMaintenanceTimer,
    ChangeHumidifierPadMaintTimerall,
    RestoreFactoryDefaults,
    # ReversingValveConfig,
    # HumDehumConfig,
    HeatDemand,
    AuxHeatDemand,
    BackUpHeatDemand,
    FanDemand,
    CoolDemand,
    DehumidificationDemand,
    HumidificationDemand,
    HumidificationSetPointModify,
    DehumidificationSetPointModify,
    CommunicationsReceiverOnOff,
    ForcePhoneNumberDisplay,
    FAN_DEMAND_MANUAL as _FAN_DEMAND_MANUAL,
    FAN_DEMAND_COOL as _FAN_DEMAND_COOL,
    FAN_DEMAND_HEAT as _FAN_DEMAND_HEAT,
    FAN_DEMAND_AUX_HEAT as _FAN_DEMAND_AUX_HEAT,
    FAN_DEMAND_EMERGENCY_HEAT as _FAN_DEMAND_EMERGENCY_HEAT,
    FAN_DEMAND_DEFROST as _FAN_DEMAND_DEFROST
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


THERMOSTAT_SYSTEM_STATUS_OFF = 0x00
THERMOSTAT_SYSTEM_STATUS_COOL = 0x01
THERMOSTAT_SYSTEM_STATUS_AUTO_COOL = 0x02
THERMOSTAT_SYSTEM_STATUS_HEAT = 0x03
THERMOSTAT_SYSTEM_STATUS_AUTO_HEAT = 0x04
THERMOSTAT_SYSTEM_STATUS_BACKUP = 0x05


THERMOSTAT_CURTAILMENT_STATUS_NONE = 0x00
THERMOSTAT_CURTAILMENT_STATUS_DLC = 0x01
THERMOSTAT_CURTAILMENT_STATUS_TIERED = 0x02
THERMOSTAT_CURTAILMENT_STATUS_RTP_PROTECTION = 0x03
THERMOSTAT_CURTAILMENT_STATUS_RTP = 0x04

THERMOSTAT_FAN_STATUS_AUTO = 0x00
THERMOSTAT_FAN_STATUS_ALWAYS_ON = 0x01
THERMOSTAT_FAN_STATUS_OCCUPIED_ON = 0x02


class ThermostatMDI(object):

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

    @property
    def system_type(self):
        """
        :return: one of THERMOSTAT_SYSTEM_TYPE_* constants
        """
        data = self._get_mdi(0, 0)
        return data[0]

    @property
    def heat_stages(self):
        """
        :return: number of stages, 15 = Variable/Modulating
        """
        data = self._get_mdi(1, 0)
        return data[0] >> 4

    @property
    def cool_stages(self):
        """
        :return: number of stages, 15 = Variable/Modulating
        """
        data = self._get_mdi(1, 0)
        return data[0] & 0xF

    @property
    def balance_point_set_temp(self):
        """
        :return:
            0x00 = Balance Point System is off
            0xFF = Default value indicating that this is not being used
            0x01 - 0x7F =
        """
        data = self._get_mdi(2, 0)
        return data[0]

    @property
    def filter_time(self):
        """
        :return: hours
        """
        data = self._get_mdi(3, 1)
        return data[0] << 8 | data[1]

    @filter_time.setter
    def filter_time(self, value):
        packet = ChangeFilterTimeRemaining()

        if value is True:
            packet.set_command_data(value)

        elif isinstance(value, int):
            packet.set_command_data(False, value)
        else:
            return

        self._send(packet)

    @property
    def temp_adjustment_offset(self):
        data = self._get_mdi(5, 0)
        return TwosCompliment.decode(data[0], 8)

    @temp_adjustment_offset.setter
    def temp_adjustment_offset(self, value):
        packet = TempDisplayAdjFactorChange()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def programmable_hold_time(self):
        """
        :return:
            0x00 = disabled
            0xFFFF = default value
        """
        data = self._get_mdi(6, 1)
        return data[0] << 8 | data[1]

    @property
    def max_temp(self):
        """
        :return: 0xFF = not set/default
        """
        data = self._get_mdi(8, 0)
        return data[0]

    @max_temp.setter
    def max_temp(self, value):
        packet = LimitedHeatAndCoolRange()
        packet.set_command_data(self.min_temp, value)
        self._send(packet)

    @property
    def min_temp(self):
        """
        :return: 0xFF = not set/default
        """
        data = self._get_mdi(9, 0)
        return data[0]

    @min_temp.setter
    def min_temp(self, value):
        packet = LimitedHeatAndCoolRange()
        packet.set_command_data(value, self.max_temp)
        self._send(packet)

    @property
    def emr_state(self):
        """
        :return: THERMOSTAT_ENABLED or THERMOSTAT_DISABLED
        """
        data = self._get_mdi(10, 0)
        return int(_get_bit(data[0], 0))

    @emr_state.setter
    def emr_state(self, value):
        packet = ComfortRecoveryModify()
        data = self._get_mdi(10, 0)
        packet.set_command_data(_get_bit(data[0], 7), value)
        self._send(packet)

    @property
    def keypad_lockout(self):
        """
        :return: one of THERMOSTAT_KEYPAD_LOCKOUT_* constants
        """
        data = self._get_mdi(10, 0)

        if _get_bit(data[0], 6):
            data = self._get_mdi(22, 0)
            if _get_bit(data[0], 2):
                return THERMOSTAT_KEYPAD_LOCKOUT_PARTIAL

            elif _get_bit(data[0], 1):
                return THERMOSTAT_KEYPAD_LOCKOUT_FULL

        return THERMOSTAT_KEYPAD_LOCKOUT_OFF

    def set_keypad_lockout(self, lockout_type, password):
        packet = KeypadLockout()
        packet.set_command_data(lockout_type, password)
        self._send(packet)

    @property
    def scale(self):
        """
        :return: one of THERMOSTAT_SCALE_* constants
        """
        data = self._get_mdi(10, 0)
        return int(_get_bit(data[0], 5))

    @scale.setter
    def scale(self, value):
        packet = FahrenheitCelsiusDisplay()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def fast_second_stage(self):
        """
        :return: THERMOSTAT_ENABLED or THERMOSTAT_DISABLED
        """
        data = self._get_mdi(10, 0)
        return int(_get_bit(data[0], 4))

    @fast_second_stage.setter
    def fast_second_stage(self, value):
        packet = ComfortModeModification()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def continious_display_light(self):
        """
        :return: THERMOSTAT_ENABLED or THERMOSTAT_DISABLED
        """
        data = self._get_mdi(10, 0)
        return int(_get_bit(data[0], 3))

    @continious_display_light.setter
    def continious_display_light(self, value):
        packet = ContinuousDisplayLight()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def compressor_lockout(self):
        """
        :return: THERMOSTAT_ENABLED or THERMOSTAT_DISABLED
        """
        data = self._get_mdi(10, 0)
        return int(_get_bit(data[0], 2))

    @compressor_lockout.setter
    def compressor_lockout(self, value):
        packet = CompressorLockout()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def heat_cycle_rate(self):
        """
        :return: % or one of THERMOSTAT_CYCLE_RATE_* constants
        """
        data = self._get_mdi(20, 0)

        if data[0]:
            return float(data[0]) * 0.5

        data = self._get_mdi(10, 0)
        return int(_get_bit(data[0], 1)) + 254

    @property
    def cool_cycle_rate(self):
        """
        :return: % or one of THERMOSTAT_CYCLE_RATE_* constants
        """
        data = self._get_mdi(21, 0)

        if data[0]:
            return float(data[0]) * 0.5

        data = self._get_mdi(10, 0)
        return int(_get_bit(data[0], 0)) + 254

    @property
    def sensor_d_weight(self):
        """
        :return: one of THERMOSTAT_SENSOR_WEIGHT_* constants
        """
        res = 0
        data = self._get_mdi(11, 0)

        res = _set_bit(res, 1, _get_bit(data[0], 7))
        res = _set_bit(res, 0, _get_bit(data[0], 6))

        return res

    @property
    def sensor_c_weight(self):
        """
        :return: one of THERMOSTAT_SENSOR_WEIGHT_* constants
        """
        res = 0
        data = self._get_mdi(11, 0)

        res = _set_bit(res, 1, _get_bit(data[0], 5))
        res = _set_bit(res, 0, _get_bit(data[0], 4))

        return res

    @property
    def sensor_b_weight(self):
        """
        :return: one of THERMOSTAT_SENSOR_WEIGHT_* constants
        """
        res = 0
        data = self._get_mdi(11, 0)

        res = _set_bit(res, 1, _get_bit(data[0], 3))
        res = _set_bit(res, 0, _get_bit(data[0], 2))

        return res

    @property
    def sensor_a_weight(self):
        """
        :return: one of THERMOSTAT_SENSOR_WEIGHT_* constants
        """
        res = 0
        data = self._get_mdi(11, 0)

        res = _set_bit(res, 1, _get_bit(data[0], 1))
        res = _set_bit(res, 0, _get_bit(data[0], 0))

        return res

    @property
    def sensor_local_weight(self):
        """
        :return: one of THERMOSTAT_SENSOR_WEIGHT_* constants
        """
        res = 0
        data = self._get_mdi(12, 0)

        res = _set_bit(res, 1, _get_bit(data[0], 7))
        res = _set_bit(res, 0, _get_bit(data[0], 6))

        return res

    @property
    def type(self):
        """
        :return: one of THERMOSTAT_TYPE_* constants
        """
        data = self._get_mdi(12, 0)
        return int(_get_bit(data[0], 4))

    @property
    def schedule_profile_type(self):
        """
        :return: one of THERMOSTAT_PROFILE_TYPE_* constants
        """
        res = 0
        data = self._get_mdi(12, 0)

        res = _set_bit(res, 1, _get_bit(data[0], 3))
        res = _set_bit(res, 0, _get_bit(data[0], 2))

        return res

    @schedule_profile_type.setter
    def schedule_profile_type(self, value):
        packet = HeatProfileChange()
        packet.set_command_data(
            self.schedule_interval_type,
            value,
            self.heat_schedule
        )
        self._send(packet)

        packet = CoolProfileChange()
        packet.set_command_data(
            self.schedule_interval_type,
            value,
            self.cool_schedule
        )
        self._send(packet)

    @property
    def cool_schedule(self):
        return None

    @property
    def heat_schedule(self):
        return None

    @property
    def schedule_interval_type(self):
        """
        :return: one of THERMOSTAT_INTERVAL_TYPE_* constants
        """
        res = 0
        data = self._get_mdi(12, 0)

        res = _set_bit(res, 1, _get_bit(data[0], 1))
        res = _set_bit(res, 0, _get_bit(data[0], 0))

        return res

    @schedule_interval_type.setter
    def schedule_interval_type(self, value):
        packet = HeatProfileChange()
        packet.set_command_data(
            value,
            self.schedule_profile_type,
            self.heat_schedule
        )
        self._send(packet)

        packet = CoolProfileChange()
        packet.set_command_data(
            value,
            self.schedule_profile_type,
            self.cool_schedule
        )
        self._send(packet)

    @property
    def air_handler_lockout_temp(self):
        """
        :return: 0xFF = not set/default
        """
        data = self._get_mdi(13, 0)
        return data[0]

    @property
    def uv_lamp_time(self):
        """
        :return: days
            0x0000 = disabled
            0xFFFF = default
        """
        data = self._get_mdi(14, 1)
        return data[0] << 8 | data[1]

    @uv_lamp_time.setter
    def uv_lamp_time(self, value):
        packet = ChangeUvLightMaintenanceTimer()

        if value is False:
            packet.set_command_data(value)
        elif isinstance(value, int):
            packet.set_command_data(False, value)

        self._send(packet)

    @property
    def humidifier_pad_time(self):
        """
        :return: hours
            0x0000 = disabled
            0xFFFF = default
        """
        data = self._get_mdi(16, 1)
        return data[0] << 8 | data[1]

    @humidifier_pad_time.setter
    def humidifier_pad_time(self, value):
        packet = ChangeHumidifierPadMaintTimerall()

        if value is False:
            packet.set_command_data(value)
        elif isinstance(value, int):
            packet.set_command_data(False, value)

        self._send(packet)

    @property
    def aux_heat_stages(self):
        """
        :return: 0x0F = modulating
        """
        data = self._get_mdi(18, 0)

        return data[0] << 4 & 0xF

    @property
    def fan_stages(self):
        """
        :return: 0x0F = modulating
        """
        data = self._get_mdi(18, 0)
        return data[0] & 0xF

    @property
    def aux_heat_cycle_rate(self):
        """
        :return: Default/Unused is 0; Percentage - 0.5% Increments.
        """
        data = self._get_mdi(19, 0)

        return data[0]

    @property
    def ob_mode(self):
        """
        :return: 0 = O Mode/Unavailable;  1 = B Mode
        """
        data = self._get_mdi(22, 0)
        return int(_get_bit(data[0], 6))

    @property
    def beep(self):
        """
        :return: THERMOSTAT_ENABLED or THERMOSTAT_DISABLED
        """
        data = self._get_mdi(22, 0)
        return int(_get_bit(data[0], 5))

    @beep.setter
    def beep(self, value):
        packet = BeeperEnable()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def display_contrast(self):
        data = self._get_mdi(24, 0)

        return data[0]

    @property
    def communication_timeout(self):
        """
        :return: seconds
        """
        data = self._get_mdi(25, 1)

        return data[0] << 8 | data[1]

    def enable_communications_receiver(self, value):
        packet = CommunicationsReceiverOnOff()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def display_phone_number_on_fault(self):
        """
        :return: THERMOSTAT_ENABLED or THERMOSTAT_DISABLED
        """
        data = self._get_mdi(27, 0)
        return int(_get_bit(data[0], 0))

    @display_phone_number_on_fault.setter
    def display_phone_number_on_fault(self, value):
        packet = ForcePhoneNumberDisplay()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def indoor_unit_node_type(self):
        """
        :return: one of node_types.NODE_TYPE_* constants
        """
        data = self._get_mdi(28, 0)
        return data[0]

    @property
    def outdoor_unit_node_type(self):
        """
        :return: one of node_types.NODE_TYPE_* constants
        """
        data = self._get_mdi(29, 0)
        return data[0]

    @property
    def humidification_capable(self):
        """
        :return: THERMOSTAT_CAPABLE or THERMOSTAT_NOT_CAPABLE
        """
        data = self._get_mdi(30, 0)
        return int(_get_bit(data[0], 3))

    @property
    def dehumidification_capable(self):
        """
        :return: THERMOSTAT_CAPABLE or THERMOSTAT_NOT_CAPABLE
        """
        data = self._get_mdi(30, 0)
        return int(_get_bit(data[0], 2))

    @property
    def independent_humidification_capable(self):
        """
        :return: THERMOSTAT_CAPABLE or THERMOSTAT_NOT_CAPABLE
        """
        data = self._get_mdi(30, 0)
        return int(_get_bit(data[0], 1))

    @property
    def independent_dehumidification_capable(self):
        """
        :return: THERMOSTAT_CAPABLE or THERMOSTAT_NOT_CAPABLE
        """
        data = self._get_mdi(30, 0)
        return int(_get_bit(data[0], 0))

    @property
    def allowed_schedule_profiles(self):
        res = []
        data = self._get_mdi(31, 0)

        if _get_bit(data[0], 3):  # 5-2
            res += [THERMOSTAT_PROFILE_TYPE_5_2]
        if _get_bit(data[0], 2):  # 7-day
            res += [THERMOSTAT_PROFILE_TYPE_7_DAY]
        if _get_bit(data[0], 1):  # 5-1-1
            res += [THERMOSTAT_PROFILE_TYPE_5_1_1]
        if _get_bit(data[0], 0):  # Non Programmable
            res += [THERMOSTAT_PROFILE_TYPE_NON_PROGRAMMABLE]

        return res

    @property
    def allowed_schedule_intervals(self):
        res = []
        data = self._get_mdi(32, 0)

        if _get_bit(data[0], 2):  # 2 step
            res += [THERMOSTAT_INTERVAL_TYPE_2_STEP]
        if _get_bit(data[0], 1):  # Non Programmable
            res += [THERMOSTAT_INTERVAL_TYPE_NON_PROGRMMABLE]
        if _get_bit(data[0], 0):  # 4 step
            res += [THERMOSTAT_INTERVAL_TYPE_4_STEP]

        return res

    @property
    def critical_fault(self):
        data = self._get_status_mdi(0, 0)
        return data[0]

    @property
    def minor_fault(self):
        data = self._get_status_mdi(1, 0)
        return data[0]

    @property
    def operating_status(self):
        """
        :return: one of THERMOSTAT_SYSTEM_STATUS_
        """
        data = self._get_status_mdi(2, 0)
        return data[0]

    @operating_status.setter
    def operating_status(self, value):
        packet = SystemSwitchModify()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def curtailment_status(self):
        """
        :return: one of THERMOSTAT_CURTAILMENT_STATUS_* constants
        """
        data = self._get_status_mdi(3, 0)
        return data[0]

    @property
    def humidification_setpoint(self):
        data = self._get_status_mdi(4, 0)
        return data[0]

    @humidification_setpoint.setter
    def humidification_setpoint(self, value):
        packet = HumidificationSetPointModify()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def dehumidification_setpoint(self):
        data = self._get_status_mdi(5, 0)
        return data[0]

    @dehumidification_setpoint.setter
    def dehumidification_setpoint(self, value):
        packet = DehumidificationSetPointModify()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def working_setpoint(self):
        data = self._get_status_mdi(6, 0)
        return data[0]

    @property
    def display_temp(self):
        data = self._get_status_mdi(7, 1)
        value = data[0] << 8 | data[1]

        temp = value << 4 & 0xF
        frac = value & 0xF

        frac /= float(10)
        return temp + frac

    @property
    def heat_setpoint(self):
        data = self._get_status_mdi(9, 0)
        return data[0]

    @heat_setpoint.setter
    def heat_setpoint(self, value):
        packet = HeatSetPointTemperatureModify()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def cool_setpoint(self):
        data = self._get_status_mdi(10, 0)
        return data[0]

    @cool_setpoint.setter
    def cool_setpoint(self, value):
        packet = CoolSetPointTemperatureModify()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def daylight_savings(self):
        """
        :return: THERMOSTAT_ENABLED or THERMOSTAT_DISABLED
        """
        data = self._get_status_mdi(22, 0)
        return int(_get_bit(data[0], 0))

    @daylight_savings.setter
    def daylight_savings(self, value):
        packet = AdvanceRealTimeDayOverride()
        packet.set_command_data(
            bool(self.clock_lockout),
            value,
            self.gmt_offset,
            self.date_time
        )
        self._send(packet)

    @property
    def clock_lockout(self):
        """
        :return: THERMOSTAT_ENABLED or THERMOSTAT_DISABLED
        """
        data = self._get_status_mdi(22, 0)
        return int(_get_bit(data[0], 7))

    @clock_lockout.setter
    def clock_lockout(self, value):
        packet = AdvanceRealTimeDayOverride()
        packet.set_command_data(
            value,
            bool(self.daylight_savings),
            self.gmt_offset,
            self.date_time
        )
        self._send(packet)

    @property
    def gmt_offset(self):
        data = self._get_status_mdi(23, 0)

        return TwosCompliment.decode(data[0] / 4, 8)

    @gmt_offset.setter
    def gmt_offset(self, value):
        packet = AdvanceRealTimeDayOverride()
        packet.set_command_data(
            bool(self.clock_lockout),
            bool(self.daylight_savings),
            value,
            self.date_time
        )
        self._send(packet)

    @property
    def date_time(self):
        weekday = self._get_status_mdi(11, 0)[0]
        year = self._get_status_mdi(25, 0)[0]
        month = self._get_status_mdi(26, 0)[0]
        day = self._get_status_mdi(27, 0)[0]
        hour = self._get_status_mdi(12, 0)[0]
        minute = self._get_status_mdi(13, 0)[0]
        second = self._get_status_mdi(14, 0)[0]

        if 0xFF in (weekday, year, month, day, hour, minute, second):
            return

        year += 2000
        month += 1

        return datetime.datetime(
            month=month,
            day=day,
            year=year,
            hour=hour,
            minute=minute,
            second=second
        )

    @date_time.setter
    def date_time(self, value):
        packet = RealTimeDayOverride()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def programmable_hold(self):
        """
        :return: THERMOSTAT_ENBLED or THERMOSTAT_DISABLED
        """
        data = self._get_status_mdi(15, 0)
        return int(_get_bit(data[0], 3))

    @property
    def startup_hold(self):
        """
        :return: THERMOSTAT_ENBLED or THERMOSTAT_DISABLED
        """
        data = self._get_status_mdi(15, 0)
        return int(_get_bit(data[0], 2))

    @property
    def temporary_hold(self):
        """
        :return: THERMOSTAT_ENBLED or THERMOSTAT_DISABLED
        """
        data = self._get_status_mdi(15, 0)
        return int(_get_bit(data[0], 1))

    @temporary_hold.setter
    def temporary_hold(self, value):
        packet = SetPointTempAndTemporaryHold()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def permanent_hold(self):
        """
        :return: THERMOSTAT_ENBLED or THERMOSTAT_DISABLED
        """
        data = self._get_status_mdi(15, 0)
        return int(_get_bit(data[0], 0))

    @permanent_hold.setter
    def permanent_hold(self, value):
        packet = PermanentSetPointTempHoldModify()
        packet.set_command_data(value)
        self._send(packet)

    def hold_override(self):
        packet = HoldOverride()
        packet.set_command_data(THERMOSTAT_DISABLED)
        self._send(packet)

    @property
    def temporary_hold_remaining(self):
        """
        :return: minutes
        """
        data = self._get_status_mdi(16, 1)
        return data[0] << 8 | data[1]

    @temporary_hold_remaining.setter
    def temporary_hold_remaining(self, value):
        packet = SetPointTempTimeHold()
        packet.set_command_data(self.working_setpoint, value)
        self._send(packet)

    @property
    def dehumidification_demand(self):
        """
        :return:
        """
        data = self._get_status_mdi(18, 0)
        return data[0] * 0.5

    @dehumidification_demand.setter
    def dehumidification_demand(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = DehumidificationDemand()
        packet.set_command_data(timer, value)
        self._send(packet)

    @property
    def humidification_demand(self):
        """
        :return:
        """
        data = self._get_status_mdi(19, 0)
        return data[0] * 0.5

    @humidification_demand.setter
    def humidification_demand(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = HumidificationDemand()
        packet.set_command_data(timer, value)
        self._send(packet)

    @property
    def heat_demand(self):
        """
        :return:
        """
        data = self._get_status_mdi(20, 0)
        return data[0] * 0.5

    @heat_demand.setter
    def heat_demand(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = HeatDemand()
        packet.set_command_data(timer, value)
        self._send(packet)

    @property
    def cool_demand(self):
        """
        :return:
        """
        data = self._get_status_mdi(21, 0)
        return data[0] * 0.5

    @cool_demand.setter
    def cool_demand(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = CoolDemand()
        packet.set_command_data(timer, value)
        self._send(packet)

    @property
    def fan_demand(self):
        """
        :return:
        """
        data = self._get_status_mdi(22, 0)
        return data[0] * 0.5

    def fan_demand_manual(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = FanDemand()
        packet.set_command_data(timer, _FAN_DEMAND_MANUAL, value)
        self._send(packet)

    fan_demand_manual = property(fset=fan_demand_manual)

    def fan_demand_cool(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = FanDemand()
        packet.set_command_data(timer, _FAN_DEMAND_COOL, value)
        self._send(packet)

    fan_demand_cool = property(fset=fan_demand_cool)

    def fan_demand_heat(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = FanDemand()
        packet.set_command_data(timer, _FAN_DEMAND_HEAT, value)
        self._send(packet)

    fan_demand_heat = property(fset=fan_demand_heat)

    def fan_demand_aux_heat(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = FanDemand()
        packet.set_command_data(timer, _FAN_DEMAND_AUX_HEAT, value)
        self._send(packet)

    fan_demand_aux_heat = property(fset=fan_demand_aux_heat)

    def fan_demand_emergency_heat(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = FanDemand()
        packet.set_command_data(timer, _FAN_DEMAND_EMERGENCY_HEAT, value)
        self._send(packet)

    fan_demand_emergency_heat = property(fset=fan_demand_emergency_heat)

    def fan_demand_defrost(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = FanDemand()
        packet.set_command_data(timer, _FAN_DEMAND_DEFROST, value)
        self._send(packet)

    fan_demand_defrost = property(fset=fan_demand_defrost)

    @property
    def emergency_heat_demand(self):
        """
        :return:
        """
        data = self._get_status_mdi(23, 0)
        return data[0] * 0.5

    @emergency_heat_demand.setter
    def emergency_heat_demand(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = BackUpHeatDemand()
        packet.set_command_data(timer, value)
        self._send(packet)

    @property
    def aux_heat_demand(self):
        """
        :return:
        """
        data = self._get_status_mdi(24, 0)
        return data[0] * 0.5

    @aux_heat_demand.setter
    def aux_heat_demand(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = AuxHeatDemand()
        packet.set_command_data(timer, value)
        self._send(packet)

    @property
    def relative_humidity(self):
        """
        :return:
        """
        data = self._get_status_mdi(28, 0)
        return data[0]

    @property
    def vacation_mode(self):
        """
        :return: THERMOSTAT_ENABLED or THERMOSTAT_DISABLED
        """
        data = self._get_status_mdi(29, 0)
        return int(data[0])

    @vacation_mode.setter
    def vacation_mode(self, value):
        packet = VacationMode()
        packet.set_command_data(value)
        self._send(packet)

    def vacation_mode_setpoints(self, heat_setpoint, cool_setpoint):
        packet = VacationMode()
        packet.set_command_data(self.vacation_mode, heat_setpoint, cool_setpoint)
        self._send(packet)

    @property
    def fan_mode_setting(self):
        """
        :return: one of THERMOSTAT_FAN_STATUS_* constants
        """
        data = self._get_status_mdi(30, 0)
        return data[0]

    @fan_mode_setting.setter
    def fan_mode_setting(self, value):
        packet = FanKeySelection()
        packet.set_command_data(value)
        self._send(packet)

    def restore_factory_defaults(self):
        packet = RestoreFactoryDefaults()
        packet.set_command_data()
        self._send(packet)

    THERMOSTAT_SUBSYSTEM_INSTALLATION_TEST_START = 0x01
    THERMOSTAT_SUBSYSTEM_INSTALLATION_TEST_STOP = 0x00

    def subsystem_installation_test(self, state):
        """
        :param state: one of THERMOSTAT_SUBSYSTEM_INSTALLATION_TEST_* constants
        :return:
        """
        packet = SubsystemInstallationTest()
        packet.set_command_data(state)
        self._send(packet)

    def set_display_text(
        self,
        area_id,
        duration,
        blink,
        reverse,
        text_id,
        text
    ):
        """
        :param area_id: 0 - 7
        :param duration: 0.0 - 7.5
        :param blink: True/False
        :param reverse: True/False
        :param text_id: 0 - 7
        :param text:
        :return:
        """
        packet = CustomMessageAreaDisplayData()
        packet.set_command_data(
            area_id,
            duration,
            blink,
            reverse,
            text_id,
            text
        )
        self._send(packet)

    # ReversingValveConfig,
    # HumDehumConfig
