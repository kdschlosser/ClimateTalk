# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

import datetime

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


class ZoneTemperatureControllerStatus0MDI(bytearray):
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
        :return: one of ZONE_TEMPERATURE_CONTROLLER_FAN_MODE_* constants
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
        :return: one of ZONE_TEMPERATURE_CONTROLLER_SYSTEM_STATUS_
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
