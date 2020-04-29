# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

import datetime
import threading
from ..utils import (
    get_bit as _get_bit,
    set_bit as _set_bit
)

from ..packet import (
    GetConfigurationRequest,
    GetStatusRequest
)

from ..commands import (
    FanKeySelection,
    DefrostDemand,
    HeatDemand,
    AuxHeatDemand,
    BackUpHeatDemand,
    FanDemand,
    CoolDemand,
    DehumidificationDemand,
    HumidificationDemand,
    FAN_DEMAND_MANUAL as _FAN_DEMAND_MANUAL,
    FAN_DEMAND_COOL as _FAN_DEMAND_COOL,
    FAN_DEMAND_HEAT as _FAN_DEMAND_HEAT,
    FAN_DEMAND_AUX_HEAT as _FAN_DEMAND_AUX_HEAT,
    FAN_DEMAND_EMERGENCY_HEAT as _FAN_DEMAND_EMERGENCY_HEAT,
    FAN_DEMAND_DEFROST as _FAN_DEMAND_DEFROST
)


CROSSOVER_CAPABLE = 0x01
CROSSOVER_NOT_CAPABLE = 0x00

CROSSOVER_ENABLED = 0x01
CROSSOVER_DISABLED = 0x00

CROSSOVER_OPERATION_TYPE_24_VAC = 0x00
CROSSOVER_OPERATION_TYPE_MINI_TSTAT = 0x01

CROSSOVER_FAN_MOTOR_SIZE_UNKNOWN = 0x00
CROSSOVER_FAN_MOTOR_SIZE_THIRD_HP = 0x03  # 1/3 HP
CROSSOVER_FAN_MOTOR_SIZE_HALF_HP = 0x06  # 1/3 HP
CROSSOVER_FAN_MOTOR_SIZE_THREE_QUARTER_HP = 0x09  # 1/3 HP
CROSSOVER_FAN_MOTOR_SIZE_ONE_HP = 0x0C  # 1/3 HP
CROSSOVER_FAN_MOTOR_SIZE_TWO_HP = 0x18  # 1/3 HP


CROSSOVER_HEAT_TYPE_GAS = 0x00
CROSSOVER_HEAT_TYPE_ELECTRIC = 0x01

CROSSOVER_OUTDOOR_EQUIP_AC = 0x00
CROSSOVER_OUTDOOR_EQUIP_HEAT_PUMP = 0x01
CROSSOVER_EQUIP_TYPE_INDOOR = 0x00
CROSSOVER_EQUIP_TYPE_OUTDOOR = 0x01

CROSSOVER_FAN_STATUS_AUTO = 0x00
CROSSOVER_FAN_STATUS_ALWAYS_ON = 0x01
CROSSOVER_FAN_STATUS_OCCUPIED_ON = 0x02


class CrossoverMDI(object):
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
    def fan_speeds(self):
        """
        :return: 0x0F = variable
        """
        data = self._get_mdi(0, 0)
        return data[0] << 4 & 0xF

    @property
    def heat_stages(self):
        """
        :return: 0x0F = variable
        """
        data = self._get_mdi(1, 0)
        return data[0] << 4 & 0xF

    @property
    def cool_stages(self):
        """
        :return: 0x0F = variable
        """
        data = self._get_mdi(1, 0)
        return data[0] & 0xF

    @property
    def aux_stages(self):
        """
        :return: 0x0F = variable
        """
        data = self._get_mdi(2, 0)
        return data[0] << 4 & 0xF

    @property
    def indoor_heat_type(self):
        """
        :return: one of CROSSOVER_HEAT_TYPE_* constants
        """
        data = self._get_mdi(2, 0)
        return int(_get_bit(data[0], 3))

    @property
    def outdoor_equip_type(self):
        """
        :return: one of CROSSOVER_OUTDOOR_EQUIP_TYPE_* constants
        """
        data = self._get_mdi(2, 0)
        return int(_get_bit(data[0], 2))

    @property
    def configured_equip_type(self):
        """
        :return: one of CROSSOVER_EQUIP_TYPE_* constants
        """
        data = self._get_mdi(2, 0)
        return int(_get_bit(data[0], 1))

    @property
    def mode_of_operation(self):
        """
        :return: one of CROSSOVER_OPERATION_TYPE_* constants
        """
        data = self._get_mdi(2, 0)
        return int(_get_bit(data[0], 0))

    @property
    def humidification(self):
        """
        :return: CROSSOVER_ENABLED or CROSSOVER_DISABLED
        """
        data = self._get_mdi(3, 0)
        return int(_get_bit(data[0], 1))

    @property
    def dehumidification(self):
        """
        :return: CROSSOVER_ENABLED or CROSSOVER_DISABLED
        """
        data = self._get_mdi(3, 0)
        return int(_get_bit(data[0], 0))

    @property
    def independent_humidification(self):
        """
        :return: CROSSOVER_ENABLED or CROSSOVER_DISABLED
        """
        data = self._get_mdi(4, 0)
        return int(_get_bit(data[0], 7))

    @property
    def independent_dehumidification(self):
        """
        :return: CROSSOVER_ENABLED or CROSSOVER_DISABLED
        """
        data = self._get_mdi(4, 0)
        return int(_get_bit(data[0], 6))

    @property
    def speed_trim(self):
        res = 0
        data = self._get_mdi(5, 0)[0]
        res = _set_bit(res, 1, _get_bit(data, 5))
        res = _set_bit(res, 0, _get_bit(data, 4))

        if res == 0:
            return 0xFF
        if res == 1:
            return -10
        if res == 2:
            return 10
        if res == 3:
            return 0

    @property
    def air_flow(self):
        res = 0
        data = self._get_mdi(5, 0)[0]
        res = _set_bit(res, 1, _get_bit(data, 3))
        res = _set_bit(res, 0, _get_bit(data, 2))

        if res == 0:
            return 350
        if res == 1:
            return 375
        if res == 2:
            return 400
        if res == 3:
            return 400

    @property
    def tonnage(self):
        res = 0
        data = self._get_mdi(5, 0)[0]
        res = _set_bit(res, 1, _get_bit(data, 1))
        res = _set_bit(res, 0, _get_bit(data, 0))
        if res == 0:
            return 2
        if res == 1:
            return 3
        if res == 2:
            return 4
        if res == 3:
            return 5

    @property
    def critical_fault(self):
        data = self._get_status_mdi(0, 0)
        return data[0]

    @property
    def minor_fault(self):
        data = self._get_status_mdi(1, 0)
        return data[0]

    @property
    def heat_demand(self):
        """
        :return:
        """
        data = self._get_status_mdi(2, 0)
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
        data = self._get_status_mdi(3, 0)
        return data[0] * 0.5

    @cool_demand.setter
    def cool_demand(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = CoolDemand()
        packet.set_command_data(timer, value)
        self._send(packet)

    @property
    def fan_mode_setting(self):
        """
        :return: one of CROSSOVER_FAN_STATUS_* constants
        """
        data = self._get_status_mdi(4, 0)
        return data[0]

    @fan_mode_setting.setter
    def fan_mode_setting(self, value):
        packet = FanKeySelection()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def fan_demand(self):
        """
        :return:
        """
        data = self._get_status_mdi(5, 0)
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
    def fan_rate(self):
        """
        :return:
        """
        data = self._get_status_mdi(6, 0)
        return data[0]

    @property
    def defrost_demand(self):
        """
        :return:
        """
        data = self._get_status_mdi(7, 0)
        return data[0] * 0.5

    @defrost_demand.setter
    def defrost_demand(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = DefrostDemand()
        packet.set_command_data(timer, value)
        self._send(packet)

    @property
    def dehumidification_demand(self):
        """
        :return:
        """
        data = self._get_status_mdi(8, 0)
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
        data = self._get_status_mdi(9, 0)
        return data[0] * 0.5

    @humidification_demand.setter
    def humidification_demand(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = HumidificationDemand()
        packet.set_command_data(timer, value)
        self._send(packet)

    @property
    def emergency_heat_demand(self):
        """
        :return:
        """
        data = self._get_status_mdi(10, 0)
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
        data = self._get_status_mdi(11, 0)
        return data[0] * 0.5

    @aux_heat_demand.setter
    def aux_heat_demand(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = AuxHeatDemand()
        packet.set_command_data(timer, value)
        self._send(packet)

    @property
    def outdoor_heat_demand_actual(self):
        data = self._get_status_mdi(12, 0)
        return data[0] * 0.5

    @property
    def heat_demand_actual(self):
        data = self._get_status_mdi(13, 0)
        return data[0] * 0.5

    @property
    def cool_demand_actual(self):
        data = self._get_status_mdi(14, 0)
        return data[0] * 0.5

    @property
    def fan_demand_actual(self):
        data = self._get_status_mdi(15, 0)
        return data[0] * 0.5

    @property
    def fan_rate_actual(self):
        data = self._get_status_mdi(16, 0)
        return data[0]

    @property
    def fan_delay_remaining(self):
        data = self._get_status_mdi(17, 0)
        return data[0]

    @property
    def humidification_demand_actual(self):
        data = self._get_status_mdi(18, 0)
        return data[0] * 0.5

    @property
    def dehumidification_demand_actual(self):
        data = self._get_status_mdi(19, 0)
        return data[0] * 0.5

    @property
    def emulated_defrost_demand(self):
        data = self._get_status_mdi(20, 0)
        return data[0] * 0.5

    @property
    def emulated_fan_demand(self):
        data = self._get_status_mdi(21, 0)
        return data[0] * 0.5

    @property
    def emulated_fan_rate(self):
        data = self._get_status_mdi(22, 0)
        return data[0]
