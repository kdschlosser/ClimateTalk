# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser


from ..utils import (
    get_bit as _get_bit,
    set_bit as _set_bit
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


class ZoneControllerConfig0MDI(bytearray):
    id = 0

    @property
    def system_type(self):
        """
        :return: one of ZONE_CONTROLLER_SYSTEM_TYPE_* constants
        """
        return self[0]

    @property
    def heat_stages(self):
        """
        :return: 0x0F = variable
        """
        return self[1] << 4 & 0xF

    @property
    def cool_stages(self):
        """
        :return: 0x0F = variable
        """
        return self[1] & 0xF

    @property
    def balance_point_set_temp(self):
        """
        :return: 0x00 = Off, 0xFF = default
        """
        return self[2]

    @property
    def filter_time(self):
        """
        :return: hours
        """
        return self[3] << 8 | self[4]

    @property
    def uv_lamp_time(self):
        """
        :return: days
            0x0000 = disabled
            0xFFFF = default
        """
        return self[5] << 8 | self[6]

    @property
    def humidifier_pad_time(self):
        """
        :return: hours
            0x0000 = disabled
            0xFFFF = default
        """
        return self[7] << 8 | self[8]

    @property
    def cool_humidification_capable(self):
        """
        :return: ZONE_CONTROLLER_CAPABLE or ZONE_CONTROLLER_NOT_CAPABLE
        """
        return int(_get_bit(self[9], 2))

    @property
    def humidification_capable(self):
        """
        :return: ZONE_CONTROLLER_CAPABLE or ZONE_CONTROLLER_NOT_CAPABLE
        """
        return int(_get_bit(self[9], 1))

    @property
    def dehumidification_capable(self):
        """
        :return: ZONE_CONTROLLER_CAPABLE or ZONE_CONTROLLER_NOT_CAPABLE
        """
        return int(_get_bit(self[9], 0))
    

ZONE_CONTROLLER_FAN_STATUS_AUTO = 0x00
ZONE_CONTROLLER_FAN_STATUS_ALWAYS_ON = 0x01
ZONE_CONTROLLER_FAN_STATUS_OCCUPIED_ON = 0x02


ZONE_CONTROLLER_SYSTEM_STATUS_OFF = 0x00
ZONE_CONTROLLER_SYSTEM_STATUS_COOL = 0x01
ZONE_CONTROLLER_SYSTEM_STATUS_AUTO_COOL = 0x02
ZONE_CONTROLLER_SYSTEM_STATUS_HEAT = 0x03
ZONE_CONTROLLER_SYSTEM_STATUS_AUTO_HEAT = 0x04
ZONE_CONTROLLER_SYSTEM_STATUS_BACKUP = 0x05


class ZoneControllerStatus0MDI(bytearray):
    id = 0

    @property
    def critical_fault(self):

        return self[0]

    @property
    def minor_fault(self):
        return self[1]

    @property
    def heat_request_demand(self):
        """
        :return:
        """
        return self[7] * 0.5

    @property
    def cool_request_demand(self):
        """
        :return:
        """
        return self[9] * 0.5

    @property
    def fan_request_mode(self):
        """
        :return: one of ZONE_CONTROLLER_FAN_STATUS_* constants
        """
        return self[10]

    @property
    def fan_request_demand(self):
        """
        :return:
        """
        return self[11] * 0.5

    @property
    def fan_request_rate(self):
        """
        :return:
        """
        return self[12]

    @property
    def fan_request_delay(self):
        """
        :return:
        """
        return self[13]

    @property
    def emergency_request_demand(self):
        """
        :return:
        """
        return self[14] * 0.5

    @property
    def aux_request_demand(self):
        """
        :return:
        """
        return self[15] * 0.5

    @property
    def humidification_request_demand(self):
        """
        :return:
        """
        return self[16] * 0.5

    @property
    def dehumidification_request_demand(self):
        """
        :return:
        """
        return self[17] * 0.5

    @property
    def operating_status(self):
        """
        :return: one of ZONE_CONTROLLER_SYSTEM_STATUS_
        """
        return self[18]

    @property
    def has_freeze_fault(self):
        return _get_bit(self[19], 7)

    @property
    def has_overheat_fault(self):
        return _get_bit(self[19], 6)
