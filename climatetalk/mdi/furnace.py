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

FURNACE_PRESSURE_SENSOR_TYPE_SENSORLESS = 0x00
FURNACE_PRESSURE_SENSOR_TYPE_PS = 0x01
FURNACE_PRESSURE_SENSOR_TYPE_TRANSDUCER = 0x02

FURNACE_IGNITION_TYPE_SPARK = 0x00
FURNACE_IGNITION_TYPE_SILICON_CARBIDE = 0x01
FURNACE_IGNITION_TYPE_SILICON_NITRIDE = 0x02

FURNACE_FUEL_TYPE_PROPANE = 0x00
FURNACE_FUEL_TYPE_NATURAL_GAS = 0x01

FURNACE_OPERATION_TYPE_24_VAC = 0x00
FURNACE_OPERATION_TYPE_SERIAL = 0x01
FURNACE_OPERATION_TYPE_COMBO = 0x02
FURNACE_OPERATION_TYPE_WATER = 0x03

FURNACE_CAPABLE = 0x01
FURNACE_NOT_CAPABLE = 0x00

FURNACE_CIRCULATOR_BLOWER_SIZE_UNKNOWN = 0x00
FURNACE_CIRCULATOR_BLOWER_SIZE_THIRD_HP = 0x03  # 1/3 HP
FURNACE_CIRCULATOR_BLOWER_SIZE_HALF_HP = 0x06  # 1/3 HP
FURNACE_CIRCULATOR_BLOWER_SIZE_THREE_QUARTER_HP = 0x09  # 1/3 HP
FURNACE_CIRCULATOR_BLOWER_SIZE_ONE_HP = 0x0C  # 1/3 HP
FURNACE_CIRCULATOR_BLOWER_SIZE_TWO_HP = 0x18  # 1/3 HP


FURNACE_FAN_STATUS_AUTO = 0x00
FURNACE_FAN_STATUS_ALWAYS_ON = 0x01
FURNACE_FAN_STATUS_OCCUPIED_ON = 0x02


class FurnaceMDI(object):

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
    def inducer_stages(self):
        """
        :return: 0x0F = variable
        """
        data = self._get_mdi(0, 0)
        return data[0] & 0xF

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
    def pressure_sensor_type(self):
        """
        :return: one of FURNACE_PRESSURE_SENSOR_TYPE_* constants
        """
        res = 0
        data = self._get_mdi(2, 0)[0]
        res = _set_bit(res, 1, _get_bit(data, 7))
        res = _set_bit(res, 0, _get_bit(data, 6))
        return res

    @property
    def ignition_type(self):
        """
        :return: one of FURNACE_IGNITION_TYPE_* constants
        """
        res = 0
        data = self._get_mdi(2, 0)[0]
        res = _set_bit(res, 1, _get_bit(data, 5))
        res = _set_bit(res, 0, _get_bit(data, 4))
        return res

    @property
    def fuel_type(self):
        """
        :return: one of FURNACE_FUEL_TYPE_* constants
        """
        res = 0
        data = self._get_mdi(2, 0)[0]
        res = _set_bit(res, 1, _get_bit(data, 3))
        res = _set_bit(res, 0, _get_bit(data, 2))
        return res

    @property
    def operation_type(self):
        """
        :return: one of FURNACE_OPERATION_TYPE_* constants
        """
        res = 0
        data = self._get_mdi(2, 0)[0]
        res = _set_bit(res, 1, _get_bit(data, 1))
        res = _set_bit(res, 0, _get_bit(data, 0))
        return res

    @property
    def cool_humidification_capable(self):
        """
        :return: FURNACE_CAPABLE or FURNACE_NOT_CAPABLE
        """
        data = self._get_mdi(3, 0)
        return int(_get_bit(data[0], 2))

    @property
    def humidification_capable(self):
        """
        :return: FURNACE_CAPABLE or FURNACE_NOT_CAPABLE
        """
        data = self._get_mdi(3, 0)
        return int(_get_bit(data[0], 1))

    @property
    def dehumidification_capable(self):
        """
        :return: FURNACE_CAPABLE or FURNACE_NOT_CAPABLE
        """
        data = self._get_mdi(3, 0)
        return int(_get_bit(data[0], 0))

    @property
    def btu_output(self):
        """
        :return: BTU's
        """
        data = self._get_mdi(4, 0)
        return data[0] * 1000

    @property
    def circulator_blower_manufacturer_id(self):
        """
        :return: MFG Id
        """
        data = self._get_mdi(5, 0)
        return data[0]

    @property
    def circulator_blower_size(self):
        """
        :return: one of  FURNACE_CIRCULATOR_BLOWER_SIZE_* constants
        """
        data = self._get_mdi(6, 0)
        return data[0]

    @property
    def circulator_blower_air_flow(self):
        """
        :return: cfm
        """
        data = self._get_mdi(7, 1)
        return data[0] << 8 | data[1]

    @property
    def cool_cfm_per_ton(self):
        data = self._get_mdi_1(0, 0)
        return data[0]

    @property
    def cool_tonnage(self):
        data = self._get_mdi_1(1, 0)

        return ((data[0] >> 4) & 0xF) + ((data[0] & 0xF) / 10.0)

    @property
    def heat_cfm(self):
        data = self._get_mdi_1(2, 0)
        return data[0] / 10

    @property
    def cool_cfm_trim(self):
        data = self._get_mdi_1(3, 0)[0]

        if data:
            return data - 100

        return 0

    @property
    def heat_cfm_adjust(self):
        data = self._get_mdi_1(4, 0)[0]

        if data:
            return data - 100

        return 0

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
        :return: one of THERMOSTAT_FAN_STATUS_* constants
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
    def fan_delay(self):
        """
        :return:
        """
        data = self._get_status_mdi(7, 0)
        return data[0]

    @property
    def defrost_demand(self):
        """
        :return:
        """
        data = self._get_status_mdi(8, 0)
        return data[0] * 0.5

    @defrost_demand.setter
    def defrost_demand(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = DefrostDemand()
        packet.set_command_data(timer, value)
        self._send(packet)

    @property
    def emergency_heat_demand(self):
        """
        :return:
        """
        data = self._get_status_mdi(9, 0)
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
        data = self._get_status_mdi(10, 0)
        return data[0] * 0.5

    @aux_heat_demand.setter
    def aux_heat_demand(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = AuxHeatDemand()
        packet.set_command_data(timer, value)
        self._send(packet)

    @property
    def humidification_demand(self):
        """
        :return:
        """
        data = self._get_status_mdi(11, 0)
        return data[0] * 0.5

    @humidification_demand.setter
    def humidification_demand(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = HumidificationDemand()
        packet.set_command_data(timer, value)
        self._send(packet)

    @property
    def dehumidification_demand(self):
        """
        :return:
        """
        data = self._get_status_mdi(12, 0)
        return data[0] * 0.5

    @dehumidification_demand.setter
    def dehumidification_demand(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = DehumidificationDemand()
        packet.set_command_data(timer, value)
        self._send(packet)

    @property
    def air_flow(self):
        data = self._get_status_mdi(13, 1)
        return data[0] << 8 | data[1]

    @property
    def heat_demand_actual(self):
        data = self._get_status_mdi(15, 0)
        return data[0] * 0.5

    @property
    def cool_demand_actual(self):
        data = self._get_status_mdi(16, 0)
        return data[0] * 0.5

    @property
    def fan_demand_actual(self):
        data = self._get_status_mdi(17, 0)
        return data[0] * 0.5

    @property
    def fan_rate_actual(self):
        data = self._get_status_mdi(18, 0)
        return data[0]

    @property
    def fan_delay_remaining(self):
        data = self._get_status_mdi(19, 0)
        return data[0]

    @property
    def humidification_demand_actual(self):
        data = self._get_status_mdi(20, 0)
        return data[0] * 0.5

    @property
    def dehumidification_demand_actual(self):
        data = self._get_status_mdi(21, 0)
        return data[0] * 0.5
