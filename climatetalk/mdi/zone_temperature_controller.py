# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

import datetime
import threading
from ..utils import (
    get_bit as _get_bit,
    TwosCompliment
)

from ..packet import (
    GetConfigurationRequest,
    GetStatusRequest
)

from ..commands import (
    FanKeySelection,
    HeatDemand,
    BackUpHeatDemand,
    FanDemand,
    CoolDemand,
    SystemSwitchModify,
    RealTimeDayOverride,
    AdvanceRealTimeDayOverride,
    HeatSetPointTemperatureModify,
    CoolSetPointTemperatureModify,
    HumidificationSetPointModify,
    DehumidificationSetPointModify,
    DehumidificationDemand,
    HumidificationDemand,
    FAN_DEMAND_MANUAL as _FAN_DEMAND_MANUAL,
    FAN_DEMAND_COOL as _FAN_DEMAND_COOL,
    FAN_DEMAND_HEAT as _FAN_DEMAND_HEAT,
    FAN_DEMAND_AUX_HEAT as _FAN_DEMAND_AUX_HEAT,
    FAN_DEMAND_EMERGENCY_HEAT as _FAN_DEMAND_EMERGENCY_HEAT,
    FAN_DEMAND_DEFROST as _FAN_DEMAND_DEFROST
)


ZONE_TEMPERATURE_CONTROLLER_SYSTEM_STATUS_OFF = 0x00
ZONE_TEMPERATURE_CONTROLLER_SYSTEM_STATUS_COOL = 0x01
ZONE_TEMPERATURE_CONTROLLER_SYSTEM_STATUS_AUTO_COOL = 0x02
ZONE_TEMPERATURE_CONTROLLER_SYSTEM_STATUS_HEAT = 0x03
ZONE_TEMPERATURE_CONTROLLER_SYSTEM_STATUS_AUTO_HEAT = 0x04
ZONE_TEMPERATURE_CONTROLLER_SYSTEM_STATUS_BACKUP = 0x05


ZONE_TEMPERATURE_CONTROLLER_CURTAILMENT_STATUS_NONE = 0x00
ZONE_TEMPERATURE_CONTROLLER_CURTAILMENT_STATUS_DLC = 0x01
ZONE_TEMPERATURE_CONTROLLER_CURTAILMENT_STATUS_TIERED = 0x02
ZONE_TEMPERATURE_CONTROLLER_CURTAILMENT_STATUS_RTP_PROTECTION = 0x03
ZONE_TEMPERATURE_CONTROLLER_CURTAILMENT_STATUS_RTP = 0x04

ZONE_TEMPERATURE_CONTROLLER_FAN_STATUS_AUTO = 0x00
ZONE_TEMPERATURE_CONTROLLER_FAN_STATUS_ALWAYS_ON = 0x01
ZONE_TEMPERATURE_CONTROLLER_FAN_STATUS_OCCUPIED_ON = 0x02

ZONE_TEMPERATURE_CONTROLLER_FAN_MODE_MANUAL = 0x00
ZONE_TEMPERATURE_CONTROLLER_FAN_MODE_AUTO = 0x01


class ZoneTemperatureControllerMDI(object):

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

    @property
    def critical_fault(self):
        data = self._get_status_mdi(0, 0)
        return data[0]

    @property
    def minor_fault(self):
        data = self._get_status_mdi(1, 0)
        return data[0]

    @property
    def working_setpoint(self):
        data = self._get_status_mdi(2, 0)
        return data[0]

    @property
    def heat_setpoint(self):
        data = self._get_status_mdi(3, 0)
        return data[0]

    @heat_setpoint.setter
    def heat_setpoint(self, value):
        packet = HeatSetPointTemperatureModify()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def cool_setpoint(self):
        data = self._get_status_mdi(4, 0)
        return data[0]

    @cool_setpoint.setter
    def cool_setpoint(self, value):
        packet = CoolSetPointTemperatureModify()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def humidification_setpoint(self):
        data = self._get_status_mdi(5, 0)
        return data[0]

    @humidification_setpoint.setter
    def humidification_setpoint(self, value):
        packet = HumidificationSetPointModify()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def dehumidification_setpoint(self):
        data = self._get_status_mdi(6, 0)
        return data[0]

    @dehumidification_setpoint.setter
    def dehumidification_setpoint(self, value):
        packet = DehumidificationSetPointModify()
        packet.set_command_data(value)
        self._send(packet)

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
        :return: one of THERMOSTAT_FAN_STATUS_* constants
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
        data = self._get_status_mdi(12, 0)
        return data[0]

    @property
    def fan_delay(self):
        """
        :return:
        """
        data = self._get_status_mdi(13, 0)
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
        :return: one of ZONE_USER_INTERFACE_SYSTEM_STATUS_
        """
        data = self._get_status_mdi(18, 0)
        return data[0]

    @operating_status.setter
    def operating_status(self, value):
        packet = SystemSwitchModify()
        packet.set_command_data(value)
        self._send(packet)

    @property
    def daylight_savings(self):
        """
        :return: ZONE_USER_INTERFACE_ENABLED or ZONE_USER_INTERFACE_DISABLED
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
        :return: ZONE_USER_INTERFACE_ENABLED or ZONE_USER_INTERFACE_DISABLED
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
        weekday = self._get_status_mdi(19, 0)[0]
        year = self._get_status_mdi(23, 0)[0]
        month = self._get_status_mdi(24, 0)[0]
        day = self._get_status_mdi(25, 0)[0]
        hour = self._get_status_mdi(20, 0)[0]
        minute = self._get_status_mdi(21, 0)[0]
        second = self._get_status_mdi(22, 0)[0]

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
