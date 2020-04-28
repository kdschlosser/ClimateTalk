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
    HeatDemand,
    AuxHeatDemand,
    BackUpHeatDemand,
    FanDemand,
    ChangeFilterTimeRemaining,
    ChangeUvLightMaintenanceTimer,
    ChangeHumidifierPadMaintTimerall,
    CoolDemand,
    SystemSwitchModify,
    DehumidificationDemand,
    HumidificationDemand,
    FAN_DEMAND_MANUAL as _FAN_DEMAND_MANUAL,
    FAN_DEMAND_COOL as _FAN_DEMAND_COOL,
    FAN_DEMAND_HEAT as _FAN_DEMAND_HEAT,
    FAN_DEMAND_AUX_HEAT as _FAN_DEMAND_AUX_HEAT,
    FAN_DEMAND_EMERGENCY_HEAT as _FAN_DEMAND_EMERGENCY_HEAT,
    FAN_DEMAND_DEFROST as _FAN_DEMAND_DEFROST
)


ZONE_CONTROLLER_CAPABLE = 0x01
ZONE_CONTROLLER_NOT_CAPABLE = 0x00

ZONE_CONTROLLER_SYSTEM_TYPE_UNKNOWN = 0x00
ZONE_CONTROLLER_SYSTEM_TYPE_CONVENTIONAL = 0x01
ZONE_CONTROLLER_SYSTEM_TYPE_HEAT_PUMP = 0x02
ZONE_CONTROLLER_SYSTEM_TYPE_DUAL_FUEL = 0x03
ZONE_CONTROLLER_SYSTEM_TYPE_COOLING = 0x04
ZONE_CONTROLLER_SYSTEM_TYPE_GAS_HEAT = 0x05
ZONE_CONTROLLER_SYSTEM_TYPE_ELECTRIC_HEAT = 0x06
ZONE_CONTROLLER_SYSTEM_TYPE_ELECTRIC_ONLY = 0x07
ZONE_CONTROLLER_SYSTEM_TYPE_FAN_ONLY = 0x08
ZONE_CONTROLLER_SYSTEM_TYPE_GEOTHERMAL_HEAT_PUMP = 0x09
ZONE_CONTROLLER_SYSTEM_TYPE_GEOTHERMAL_DUAL_FUEL = 0x0A
ZONE_CONTROLLER_SYSTEM_TYPE_BOILER = 0x0B
ZONE_CONTROLLER_SYSTEM_TYPE_BOILER_HEAT_PUMP = 0x0C
ZONE_CONTROLLER_SYSTEM_TYPE_DEFAULT = 0x7F
ZONE_CONTROLLER_SYSTEM_TYPE_OTHER = 0xFF

ZONE_CONTROLLER_FAN_STATUS_AUTO = 0x00
ZONE_CONTROLLER_FAN_STATUS_ALWAYS_ON = 0x01
ZONE_CONTROLLER_FAN_STATUS_OCCUPIED_ON = 0x02

ZONE_CONTROLLER_SYSTEM_STATUS_OFF = 0x00
ZONE_CONTROLLER_SYSTEM_STATUS_COOL = 0x01
ZONE_CONTROLLER_SYSTEM_STATUS_AUTO_COOL = 0x02
ZONE_CONTROLLER_SYSTEM_STATUS_HEAT = 0x03
ZONE_CONTROLLER_SYSTEM_STATUS_AUTO_HEAT = 0x04
ZONE_CONTROLLER_SYSTEM_STATUS_BACKUP = 0x05


class ZoneControllerMDI(object):
    
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
        :return: one of ZONE_CONTROLLER_SYSTEM_TYPE_* constants
        """
        data = self._get_mdi(0, 0)
        return data[0]

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
    def balance_point_set_temp(self):
        """
        :return: 0x00 = Off, 0xFF = default
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
    def uv_lamp_time(self):
        """
        :return: days
            0x0000 = disabled
            0xFFFF = default
        """
        data = self._get_mdi(5, 1)
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
        data = self._get_mdi(7, 1)
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
    def cool_humidification_capable(self):
        """
        :return: ZONE_CONTROLLER_CAPABLE or ZONE_CONTROLLER_NOT_CAPABLE
        """
        data = self._get_mdi(9, 0)
        return int(_get_bit(data[0], 2))

    @property
    def humidification_capable(self):
        """
        :return: ZONE_CONTROLLER_CAPABLE or ZONE_CONTROLLER_NOT_CAPABLE
        """
        data = self._get_mdi(9, 0)
        return int(_get_bit(data[0], 1))

    @property
    def dehumidification_capable(self):
        """
        :return: ZONE_CONTROLLER_CAPABLE or ZONE_CONTROLLER_NOT_CAPABLE
        """
        data = self._get_mdi(9, 0)
        return int(_get_bit(data[0], 0))

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
        data = self._get_status_mdi(7, 0)
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
        data = self._get_status_mdi(9, 0)
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
        :return: one of ZONE_CONTROLLER_FAN_STATUS_* constants
        """
        data = self._get_status_mdi(10, 0)
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
        data = self._get_status_mdi(11, 0)
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
        data = self._get_mdi(12, 0)
        return data[0]
    
    @property
    def fan_delay(self):
        """
        :return:
        """
        data = self._get_mdi(13, 0)
        return data[0]

    @property
    def emergency_heat_demand(self):
        """
        :return:
        """
        data = self._get_status_mdi(14, 0)
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
        data = self._get_status_mdi(15, 0)
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
        data = self._get_status_mdi(16, 0)
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
        data = self._get_status_mdi(17, 0)
        return data[0] * 0.5

    @dehumidification_demand.setter
    def dehumidification_demand(self, value):
        timer = datetime.time(minute=1, second=0)
        packet = DehumidificationDemand()
        packet.set_command_data(timer, value)
        self._send(packet)
    
    @property
    def operating_status(self):
        """
        :return: one of ZONE_CONTROLLER_SYSTEM_STATUS_
        """
        data = self._get_status_mdi(18, 0)
        return data[0]

    @operating_status.setter
    def operating_status(self, value):
        packet = SystemSwitchModify()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def has_freeze_fault(self):
        data = self._get_mdi(19, 0)
        return int(_get_bit(data[0], 7))
    
    @property
    def has_overheat_fault(self):
        data = self._get_mdi(19, 0)
        return int(_get_bit(data[0], 6))
