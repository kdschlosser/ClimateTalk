# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

import threading
from ..utils import (
    TwosCompliment,
    get_bit as _get_bit,
    set_bit as _set_bit
)

from ..packet import (
    DirectMemoryAccessReadRequest,
    DirectMemoryAccessReadResponseMotor,
    DMA_READ_MDI_TYPE_CONFIGURATION,
    DMA_READ_MDI_TYPE_STATUS,
    DMA_READ_MDI_TYPE_SENSOR,
    DMA_READ_MDI_TYPE_IDENTIFICATION
)

from ..commands import (
    SetMotorSpeed,
    SetMotorTorque,
    SetAirflowDemand,
    SetControlMode,
    SetDemandRampRate,
    SetMotorDirection,
    SetMotorTorquePercent,
    SetMotorPositionDemand,
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
    SetBlowerIdentification0,
    SetBlowerIdentification1,
    SetBlowerIdentification2,
    SetBlowerIdentification3,
    SetBlowerIdentification4,
    SetBlowerIdentification5,
    SetSpeedLimit,
    SetTorqueLimit,
    SetAirflowLimit,
    SetPowerOutputLimit,
    SetDeviceTemperatureLimit,
    StopMotorByBraking,
    RunStopMotor,
    SetDemandRampTime,
    SetInducerRampRate
)


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
    FanKeySelection,
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
    SetPointTempAndTemporaryHold,
    SetPointTempTimeHold,
    SubsystemBusyStatus,
    SubsystemInstallationTest,
    SystemSwitchModify,
    TempDisplayAdjFactorChange,
    TestMode,
    VacationMode,
    WaterHeaterModify,
)

MOTOR_CONTROL_MODE_SPEED = 0x00
MOTOR_CONTROL_MODE_TORQUE = 0x01
MOTOR_CONTROL_MODE_AIRFLOW = 0x02

MOTOR_DIRECTION_CLOCKWISE = 0x01
MOTOR_DIRECTION_COUNTER_CLOCKWISE = 0x00


class MotorConfig0MDI(object):

    def __init__(self, network, address, subnet, mac_address, session_id):
        self.network = network
        self.address = address
        self.subnet = subnet
        self.mac_address = mac_address
        self.session_id = session_id

    def _send(self, packet):
        packet.destination = self.address
        packet.subnet = self.subnet

    def _get_ident_mdi(self, byte_num, num_bytes):
        return self._get_mdi(DMA_READ_MDI_TYPE_IDENTIFICATION, byte_num, num_bytes)

    def _get_status_mdi(self, byte_num, num_bytes):
        return self._get_mdi(DMA_READ_MDI_TYPE_STATUS, byte_num, num_bytes)

    def _get_sensor_mdi(self, byte_num, num_bytes):
        return self._get_mdi(DMA_READ_MDI_TYPE_SENSOR, byte_num, num_bytes)

    def _get_mdi(self, mdi_type, byte_num, num_bytes):
        packet = DirectMemoryAccessReadRequest()
        packet.destination = self.address
        packet.subnet = self.subnet
        packet.packet_number = 0x00
        packet.payload_mdi = mdi_type
        packet.payload_packet_number = 0x00
        packet.payload_start_byte = byte_num
        packet.payload_byte_count = num_bytes

        event = threading.Event()

        data = bytearray()

        def callback(response):
            data.extend(response.payload_data)
            DirectMemoryAccessReadResponseMotor.message_type.disconnect(self.address, self.subnet)
            event.set()

        DirectMemoryAccessReadResponseMotor.message_type.connect(self.address, self.subnet, callback)

        self.network.send(packet)
        event.wait()
        return data

    @property
    def speed(self):
        data = self._get_status_mdi(0, 1)
        return (data[1] << 8 | data[0]) * 4

    @speed.setter
    def speed(self, value):
        packet = SetMotorSpeed()
        packet.set_command_data(value / 4)
        self._send(packet)

    @property
    def torque(self):
        data = self._get_status_mdi(2, 1)
        return (data[1] << 8 | data[0]) * 2048

    @torque.setter
    def torque(self, value):
        packet = SetMotorTorque()
        packet.set_command_data(value / 2048)
        self._send(packet)

    @property
    def cfm(self):
        data = self._get_status_mdi(4, 1)
        return (data[1] << 8 | data[0]) * 4

    @cfm.setter
    def cfm(self, value):
        packet = SetAirflowDemand()
        packet.set_command_data(value / 4)
        self._send(packet)

    @property
    def control_mode(self):
        """
        :return: one of MOTOR_CONTROL_MODE_* constants
        """
        data = self._get_status_mdi(8, 0)
        return data[0]

    @control_mode.setter
    def control_mode(self, value):
        packet = SetControlMode()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def demand(self):
        data = self._get_status_mdi(9, 1)

        value = data[1] << 8 | data[0]

        mode = self.control_mode
        if mode == MOTOR_CONTROL_MODE_TORQUE:
            return value * 2048

        return value * 4

    @property
    def direction(self):
        """
        :return: one of MOTOR_DIRECTION_* constants
        """
        data = self._get_status_mdi(11, 0)
        return data[0]

    @direction.setter
    def direction(self, value):
        packet = SetMotorDirection()
        packet.set_command_data(value)
        self._send(packet)


    @property
    def demand_ramp_rate(self):
        """
        :return: time in seconds from 0 to 100%
        """
        data = self._get_status_mdi(11, 0)
        return data[0]

    @demand_ramp_rate.setter
    def demand_ramp_rate(self, value):
        packet = SetDemandRampRate()
        packet.set_command_data(value)
        self._send(packet)


    SetDemandRampTime,
    SetMotorPositionDemand,

    def stop_motor(self, braking):
        RunStopMotor
        StopMotorByBraking

    def run_motor(self, ramp_time, demand):
        mode = self.control_mode
        self.control_mode = mode

        if mode == MOTOR_CONTROL_MODE_AIRFLOW:
            self.blower_coefficient1 = self.blower_coefficient1
            self.blower_coefficient2 = self.blower_coefficient2
            self.blower_coefficient3 = self.blower_coefficient3
            self.blower_coefficient4 = self.blower_coefficient4
            self.blower_coefficient5 = self.blower_coefficient5

        else:
            self.direction = self.direction
            if mode == MOTOR_CONTROL_MODE_TORQUE:
                demand = int(round(demand / 100.0)) * 65535
                packet = SetMotorTorquePercent()
                packet.set_command_data(demand)
                self._send(packet)
            else:
                self.speed = demand

        packet = RunStopMotor()
        packet.set_command_data(0x01)
        self._send(packet)


    @property
    def inducer_ramp_rate(self):
        pass

    @inducer_ramp_rate.setter
    def inducer_ramp_rate(self, value):
        packet = SetInducerRampRate()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def speed_limit(self):
        data = self._get_status_mdi(14, 1)
        return (data[1] << 8 | data[0]) * 4

    @speed_limit.setter
    def speed_limit(self, value):
        packet = SetSpeedLimit()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def torque_limit(self):
        data = self._get_status_mdi(16, 1)
        return (data[1] << 8 | data[0]) * 2048

    @torque_limit.setter
    def torque_limit(self, value):
        packet = SetTorqueLimit()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def airflow_limit(self):
        data = self._get_status_mdi(18, 1)
        return (data[1] << 8 | data[0]) * 4

    @airflow_limit.setter
    def airflow_limit(self, value):
        packet = SetAirflowLimit()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def shaft_power_out_limit(self):
        data = self._get_status_mdi(20, 1)
        return (data[1] << 8 | data[0]) * 2

    @shaft_power_out_limit.setter
    def shaft_power_out_limit(self, value):
        packet = SetPowerOutputLimit()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def power_in_limit(self):
        data = self._get_status_mdi(22, 1)
        return (data[1] << 8 | data[0]) * 2

    @property
    def motor_temp_limit(self):
        data = self._get_status_mdi(24, 1)
        return TwosCompliment.decode(data[1] << 8 | data[0], 16) / 128

    @property
    def device_temp_limit(self):
        data = self._get_status_mdi(26, 1)
        return TwosCompliment.decode(data[1] << 8 | data[0], 16) / 128

    @device_temp_limit.setter
    def device_temp_limit(self, value):
        packet = SetDeviceTemperatureLimit()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def control_status(self):
        data = self._get_status_mdi(30, 1)
        control = data[0]
        control2 = data[1]

        res = dict(
            starting_routine=_get_bit(control, 0),
            demand_slew=_get_bit(control, 1),
            run_normal=_get_bit(control, 2),
            run_power_limit=_get_bit(control, 3),
            run_temp_limit=_get_bit(control, 4),
            lost_rotor_trip=_get_bit(control, 5),
            current_trip=_get_bit(control, 6),
            over_voltage=_get_bit(control, 7),
            under_voltage=_get_bit(control2, 0),
            over_temp=_get_bit(control2, 1),
            incomplete_parameters=_get_bit(control2, 2),
            undesired_parameters=_get_bit(control2, 7)
        )
        return res

    @property
    def dc_bus_voltage(self):
        data = self._get_sensor_mdi(0, 1)
        return (data[1] << 8 | data[0]) * 64

    @property
    def ac_voltage(self):
        data = self._get_sensor_mdi(2, 1)
        return (data[1] << 8 | data[0]) * 64

    @property
    def phase_a_current(self):
        data = self._get_sensor_mdi(4, 1)
        return (data[1] << 8 | data[0]) * 2048

    @property
    def phase_b_current(self):
        data = self._get_sensor_mdi(6, 1)
        return (data[1] << 8 | data[0]) * 2048

    @property
    def phase_c_current(self):
        data = self._get_sensor_mdi(8, 1)
        return (data[1] << 8 | data[0]) * 2048

    @property
    def motor_temp(self):
        data = self._get_sensor_mdi(14, 1)
        return TwosCompliment.decode(data[1] << 8 | data[0], 16) / 128

    @property
    def ambient_temp(self):
        data = self._get_sensor_mdi(16, 1)
        return TwosCompliment.decode(data[1] << 8 | data[0], 16) / 128

    @property
    def software_version(self):
        data = self._get_ident_mdi(0, 3)
        return ''.join(chr(item) for item in data)

    @property
    def control_version(self):
        data = self._get_ident_mdi(4, 0)
        return chr(data[0])

    @property
    def serial_number(self):
        data = self._get_ident_mdi(5, 5)
        return ''.join(chr(item) for item in data)

    @property
    def protocol_version(self):
        data = self._get_ident_mdi(12, 0)
        return chr(data[0])

    @property
    def manufacturer_id(self):
        data = self._get_ident_mdi(13, 0)
        return data[0]

    @property
    def eeprom_version(self):
        data = self._get_ident_mdi(14, 1)
        return data[1] << 8 | data[0]

    @property
    def oem_id(self):
        data = self._get_ident_mdi(16, 0)
        return data[0]

    @property
    def power_level(self):
        data = self._get_ident_mdi(17, 0)
        return data[0]

    @property
    def blower_coefficient1(self):
        data = self._get_ident_mdi(18, 1)
        return data[1] << 8 | data[0]

    @blower_coefficient1.setter
    def blower_coefficient1(self, value):
        packet = SetBlowerCoefficient1()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def blower_coefficient2(self):
        data = self._get_ident_mdi(20, 1)
        return data[1] << 8 | data[0]

    @blower_coefficient2.setter
    def blower_coefficient2(self, value):
        packet = SetBlowerCoefficient2()
        packet.set_command_data(value)
        self._send(packet)
    @property
    def blower_coefficient3(self):
        data = self._get_ident_mdi(22, 1)
        return data[1] << 8 | data[0]

    @blower_coefficient3.setter
    def blower_coefficient3(self, value):
        packet = SetBlowerCoefficient3()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def blower_coefficient4(self):
        data = self._get_ident_mdi(24, 1)
        return data[1] << 8 | data[0]

    @blower_coefficient4.setter
    def blower_coefficient4(self, value):
        packet = SetBlowerCoefficient4()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def blower_coefficient5(self):
        data = self._get_ident_mdi(26, 1)
        return data[1] << 8 | data[0]

    @blower_coefficient5.setter
    def blower_coefficient5(self, value):
        packet = SetBlowerCoefficient5()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def blower_coefficient6(self):
        data = self._get_ident_mdi(40, 1)
        return data[1] << 8 | data[0]

    @blower_coefficient6.setter
    def blower_coefficient6(self, value):
        packet = SetBlowerCoefficient6()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def blower_coefficient7(self):
        data = self._get_ident_mdi(42, 1)
        return data[1] << 8 | data[0]

    @blower_coefficient7.setter
    def blower_coefficient7(self, value):
        packet = SetBlowerCoefficient7()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def blower_coefficient8(self):
        data = self._get_ident_mdi(44, 1)
        return data[1] << 8 | data[0]

    @blower_coefficient8.setter
    def blower_coefficient8(self, value):
        packet = SetBlowerCoefficient8()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def blower_coefficient9(self):
        data = self._get_ident_mdi(46, 1)
        return data[1] << 8 | data[0]

    @blower_coefficient9.setter
    def blower_coefficient9(self, value):
        packet = SetBlowerCoefficient9()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def blower_coefficient10(self):
        data = self._get_ident_mdi(486, 1)
        return data[1] << 8 | data[0]

    @blower_coefficient10.setter
    def blower_coefficient10(self, value):
        packet = SetBlowerCoefficient10()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def blower_identification0(self):
        data = self._get_ident_mdi(28, 1)
        return data[1] << 8 | data[0]

    @blower_identification0.setter
    def blower_identification0(self, value):
        packet = SetBlowerIdentification0()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def blower_identification1(self):
        data = self._get_ident_mdi(30, 1)
        return data[1] << 8 | data[0]

    @blower_identification1.setter
    def blower_identification1(self, value):
        packet = SetBlowerIdentification1()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def blower_identification2(self):
        data = self._get_ident_mdi(32, 1)
        return data[1] << 8 | data[0]

    @blower_identification2.setter
    def blower_identification2(self, value):
        packet = SetBlowerIdentification2()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def blower_identification3(self):
        data = self._get_ident_mdi(34, 1)
        return data[1] << 8 | data[0]

    @blower_identification3.setter
    def blower_identification3(self, value):
        packet = SetBlowerIdentification3()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def blower_identification4(self):
        data = self._get_ident_mdi(36, 1)
        return data[1] << 8 | data[0]

    @blower_identification4.setter
    def blower_identification4(self, value):
        packet = SetBlowerIdentification4()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def blower_identification5(self):
        data = self._get_ident_mdi(38, 1)
        return data[1] << 8 | data[0]

    @blower_identification5.setter
    def blower_identification5(self, value):
        packet = SetBlowerIdentification5()
        packet.set_command_data(value)
        self._send(packet)







