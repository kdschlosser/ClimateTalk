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
    CoolDemand,
    DehumidificationDemand,
)


AC_CAPABLE = 0x01
AC_NOT_CAPABLE = 0x00


AC_OPERATION_TYPE_24_VAC = 0x00
AC_OPERATION_TYPE_SERIAL = 0x01
AC_OPERATION_TYPE_COMBO = 0x02
AC_OPERATION_TYPE_WATER = 0x03

AC_FAN_MOTOR_SIZE_UNKNOWN = 0x00
AC_FAN_MOTOR_SIZE_THIRD_HP = 0x03  # 1/3 HP
AC_FAN_MOTOR_SIZE_HALF_HP = 0x06  # 1/3 HP
AC_FAN_MOTOR_SIZE_THREE_QUARTER_HP = 0x09  # 1/3 HP
AC_FAN_MOTOR_SIZE_ONE_HP = 0x0C  # 1/3 HP
AC_FAN_MOTOR_SIZE_TWO_HP = 0x18  # 1/3 HP


class AirConditionerMDI(object):

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

    _get_mdi_1 = _get_mdi
    _get_mdi_2 = _get_mdi

    @property
    def fan_speeds(self):
        """
        :return: 0x0F = variable
        """
        data = self._get_mdi(0, 0)
        return data[0] << 4 & 0xF

    @property
    def cool_stages(self):
        """
        :return: 0x0F = variable
        """
        data = self._get_mdi(1, 0)
        return data[0] & 0xF

    @property
    def operation_type(self):
        """
        :return: one of HEAT_PUMP_OPERATION_TYPE_* constants
        """
        res = 0
        data = self._get_mdi(2, 0)[0]
        res = _set_bit(res, 1, _get_bit(data, 1))
        res = _set_bit(res, 0, _get_bit(data, 0))
        return res

    @property
    def dehumidification_capable(self):
        """
        :return: AC_CAPABLE or AC_NOT_CAPABLE
        """
        data = self._get_mdi(3, 0)
        return int(_get_bit(data[0], 0))
    
    @property
    def tonnage(self):
        data = self._get_mdi(4, 0)
        return data[0] * 0.5

    @property
    def cool_speed_trim(self):
        data = self._get_mdi_1(0, 0)
        return data[0]

    @property
    def fan_motor_manufacturer_id(self):
        """
        :return: MFG Id
        """
        data = self._get_mdi_2(0, 0)
        return data[0]

    @property
    def fan_motor_size(self):
        """
        :return: one of  AC_FAN_MOTOR_SIZE_* constants
        """
        data = self._get_mdi_2(1, 0)
        return data[0]

    @property
    def fan_air_flow(self):
        """
        :return: cfm
        """
        data = self._get_mdi_2(2, 1)
        return data[0] << 8 | data[1]

    @property
    def critical_fault(self):
        data = self._get_status_mdi(0, 0)
        return data[0]

    @property
    def minor_fault(self):
        data = self._get_status_mdi(1, 0)
        return data[0]

    @property
    def cool_demand(self):
        """
        :return:
        """
        data = self._get_status_mdi(2, 0)
        return data[0] * 0.5

    @cool_demand.setter
    def cool_demand(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = CoolDemand()
        packet.set_command_data(timer, value)
        self._send(packet)

    @property
    def dehumidification_demand(self):
        """
        :return:
        """
        data = self._get_status_mdi(3, 0)
        return data[0] * 0.5

    @dehumidification_demand.setter
    def dehumidification_demand(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = DehumidificationDemand()
        packet.set_command_data(timer, value)
        self._send(packet)

    @property
    def cool_demand_actual(self):
        data = self._get_status_mdi(4, 0)
        return data[0] * 0.5

    @property
    def fan_demand(self):
        """
        :return:
        """
        data = self._get_status_mdi(5, 0)
        return data[0] * 0.5

    @property
    def fan_delay(self):
        """
        :return:
        """
        data = self._get_status_mdi(7, 0)
        return data[0]

    @property
    def dehumidification_demand_actual(self):
        data = self._get_status_mdi(8, 0)
        return data[0] * 0.5
