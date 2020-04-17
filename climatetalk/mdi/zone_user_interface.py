# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

import datetime
from ..utils import (
    get_bit as _get_bit,
    set_bit as _set_bit
)


ZONE_USER_INTERFACE_CAPABLE = 0x01
ZONE_USER_INTERFACE_NOT_CAPABLE = 0x00

ZONE_USER_INTERFACE_SYSTEM_TYPE_UNKNOWN = 0x00
ZONE_USER_INTERFACE_SYSTEM_TYPE_CONVENTIONAL = 0x01
ZONE_USER_INTERFACE_SYSTEM_TYPE_HEAT_PUMP = 0x02
ZONE_USER_INTERFACE_SYSTEM_TYPE_DUAL_FUEL = 0x03
ZONE_USER_INTERFACE_SYSTEM_TYPE_COOLING = 0x04
ZONE_USER_INTERFACE_SYSTEM_TYPE_GAS_HEAT = 0x05
ZONE_USER_INTERFACE_SYSTEM_TYPE_ELECTRIC_HEAT = 0x06
ZONE_USER_INTERFACE_SYSTEM_TYPE_ELECTRIC_ONLY = 0x07
ZONE_USER_INTERFACE_SYSTEM_TYPE_FAN_ONLY = 0x08
ZONE_USER_INTERFACE_SYSTEM_TYPE_GEOTHERMAL_HEAT_PUMP = 0x09
ZONE_USER_INTERFACE_SYSTEM_TYPE_GEOTHERMAL_DUAL_FUEL = 0x0A
ZONE_USER_INTERFACE_SYSTEM_TYPE_BOILER = 0x0B
ZONE_USER_INTERFACE_SYSTEM_TYPE_BOILER_HEAT_PUMP = 0x0C
ZONE_USER_INTERFACE_SYSTEM_TYPE_DEFAULT = 0x7F
ZONE_USER_INTERFACE_SYSTEM_TYPE_OTHER = 0xFF


ZONE_USER_INTERFACE_PROFILE_TYPE_NON_PROGRAMMABLE = 0x00
ZONE_USER_INTERFACE_PROFILE_TYPE_7_DAY = 0x01
ZONE_USER_INTERFACE_PROFILE_TYPE_5_1_1 = 0x02
ZONE_USER_INTERFACE_PROFILE_TYPE_5_2 = 0x03

ZONE_USER_INTERFACE_INTERVAL_TYPE_NON_PROGRMMABLE = 0x00
ZONE_USER_INTERFACE_INTERVAL_TYPE_2_STEP = 0x01
ZONE_USER_INTERFACE_INTERVAL_TYPE_4_STEP = 0x02


class ZoneUserInterfaceConfig0MDI(bytearray):
    id = 0

    @property
    def schedule_profile_type(self):
        """
        :return: one of ZONE_USER_INTERFACEPROFILE_TYPE_* constants
        """
        res = 0
        res = _set_bit(res, 1, _get_bit(self[0], 3))
        res = _set_bit(res, 0, _get_bit(self[0], 2))

        return res

    @property
    def schedule_interval_type(self):
        """
        :return: one of ZONE_USER_INTERFACEINTERVAL_TYPE_* constants
        """
        res = 0
        res = _set_bit(res, 1, _get_bit(self[0], 1))
        res = _set_bit(res, 0, _get_bit(self[0], 0))

        return res

    @property
    def allowed_schedule_profiles(self):
        res = []
        if _get_bit(self[31], 3):  # 5-2
            res += [ZONE_USER_INTERFACE_PROFILE_TYPE_5_2]
        if _get_bit(self[31], 2):  # 7-day
            res += [ZONE_USER_INTERFACE_PROFILE_TYPE_7_DAY]
        if _get_bit(self[31], 1):  # 5-1-1
            res += [ZONE_USER_INTERFACE_PROFILE_TYPE_5_1_1]
        if _get_bit(self[31], 0):  # Non Programmable
            res += [ZONE_USER_INTERFACE_PROFILE_TYPE_NON_PROGRAMMABLE]

        return res

    @property
    def allowed_schedule_intervals(self):
        res = []
        if _get_bit(self[32], 2):  # 2 step
            res += [ZONE_USER_INTERFACE_INTERVAL_TYPE_2_STEP]
        if _get_bit(self[32], 1):  # Non Programmable
            res += [ZONE_USER_INTERFACE_INTERVAL_TYPE_NON_PROGRMMABLE]
        if _get_bit(self[32], 0):  # 4 step
            res += [ZONE_USER_INTERFACE_INTERVAL_TYPE_4_STEP]

        return res

    @property
    def system_type(self):
        """
        :return: one of ZONE_USER_INTERFACE_SYSTEM_TYPE_* constants
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
        :return: ZONE_USER_INTERFACECAPABLE or ZONE_USER_INTERFACENOT_CAPABLE
        """
        return int(_get_bit(self[9], 2))

    @property
    def humidification_capable(self):
        """
        :return: ZONE_USER_INTERFACECAPABLE or ZONE_USER_INTERFACENOT_CAPABLE
        """
        return int(_get_bit(self[9], 1))

    @property
    def dehumidification_capable(self):
        """
        :return: ZONE_USER_INTERFACECAPABLE or ZONE_USER_INTERFACENOT_CAPABLE
        """
        return int(_get_bit(self[9], 0))
    

ZONE_USER_INTERFACE_SYSTEM_STATUS_OFF = 0x00
ZONE_USER_INTERFACE_SYSTEM_STATUS_COOL = 0x01
ZONE_USER_INTERFACE_SYSTEM_STATUS_AUTO_COOL = 0x02
ZONE_USER_INTERFACE_SYSTEM_STATUS_HEAT = 0x03
ZONE_USER_INTERFACE_SYSTEM_STATUS_AUTO_HEAT = 0x04
ZONE_USER_INTERFACE_SYSTEM_STATUS_BACKUP = 0x05


ZONE_USER_INTERFACE_CURTAILMENT_STATUS_NONE = 0x00
ZONE_USER_INTERFACE_CURTAILMENT_STATUS_DLC = 0x01
ZONE_USER_INTERFACE_CURTAILMENT_STATUS_TIERED = 0x02
ZONE_USER_INTERFACE_CURTAILMENT_STATUS_RTP_PROTECTION = 0x03
ZONE_USER_INTERFACE_CURTAILMENT_STATUS_RTP = 0x04

ZONE_USER_INTERFACE_FAN_STATUS_AUTO = 0x00
ZONE_USER_INTERFACE_FAN_STATUS_ALWAYS_ON = 0x01
ZONE_USER_INTERFACE_FAN_STATUS_OCCUPIED_ON = 0x02

ZONE_USER_INTERFACE_FAN_MODE_MANUAL = 0x00
ZONE_USER_INTERFACE_FAN_MODE_AUTO = 0x01


class ThermostatStatus0MDI(bytearray):
    id = 0

    @property
    def critical_fault(self):

        return self[0]

    @property
    def minor_fault(self):
        return self[1]

    @property
    def setpoint(self):
        return self[2]

    @property
    def heat_setpoint(self):
        return self[3]

    @property
    def cool_setpoint(self):
        return self[4]

    @property
    def humidification_setpoint(self):
        return self[5]

    @property
    def dehumidification(self):
        return self[6]

    @property
    def heat_request_demand(self):
        return self[7] * 0.5

    @property
    def cool_request_demand(self):
        return self[9] * 0.5

    @property
    def fan_request_mode(self):
        """
        :return: one of ZONE_USER_INTERFACE_FAN_MODE_* constants
        """
        return self[10]

    @property
    def fan_request_demand(self):
        return self[11] * 0.5

    @property
    def fan_request_rate(self):
        return self[12]

    @property
    def fan_request_delay(self):
        return self[13]

    @property
    def emergency_heat_request_demand(self):
        """
        :return:
        """
        return self[14] * 0.5

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
        :return: one of ZONE_USER_INTERFACE_SYSTEM_STATUS_
        """
        return self[18]

    @property
    def date_time(self):
        weekday = self[19]
        year = self[23]
        month = self[24]
        day = self[25]
        hour = self[20]
        minute = self[21]
        second = self[22]

        if 0xFF in (weekday, year, month, day, hour, minute, second):
            return

        return datetime.datetime(
            month=month,
            day=day,
            year=year,
            hour=hour,
            minute=minute,
            second=second
        )
