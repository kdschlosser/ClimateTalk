# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser


from ..utils import (
    get_bit as _get_bit,
    set_bit as _set_bit
)

HEAT_PUMP_CAPABLE = 0x01
HEAT_PUMP_NOT_CAPABLE = 0x00


HEAT_PUMP_OPERATION_TYPE_24_VAC = 0x00
HEAT_PUMP_OPERATION_TYPE_SERIAL = 0x01
HEAT_PUMP_OPERATION_TYPE_COMBO = 0x02
HEAT_PUMP_OPERATION_TYPE_WATER = 0x03

HEAT_PUMP_FAN_MOTOR_SIZE_UNKNOWN = 0x00
HEAT_PUMP_FAN_MOTOR_SIZE_THIRD_HP = 0x03  # 1/3 HP
HEAT_PUMP_FAN_MOTOR_SIZE_HALF_HP = 0x06  # 1/3 HP
HEAT_PUMP_FAN_MOTOR_SIZE_THREE_QUARTER_HP = 0x09  # 1/3 HP
HEAT_PUMP_FAN_MOTOR_SIZE_ONE_HP = 0x0C  # 1/3 HP
HEAT_PUMP_FAN_MOTOR_SIZE_TWO_HP = 0x18  # 1/3 HP


class HeatPumpConfig0MDI(bytearray):
    id = 0

    @property
    def fan_speeds(self):
        """
        :return: 0x0F = variable
        """
        return self[0] << 4 & 0xF

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
    def hvac_operation(self):
        """
        :return: one of HEAT_PUMP_OPERATION_TYPE_* constants
        """
        res = 0
        res = _set_bit(res, 1, _get_bit(self[2], 1))
        res = _set_bit(res, 0, _get_bit(self[2], 0))
        return res

    @property
    def dehumidification_capable(self):
        """
        :return: HEAT_PUMP_CAPABLE or HEAT_PUMP_NOT_CAPABLE
        """
        return int(_get_bit(self[3], 0))
    
    @property
    def tonnage(self):
        return self[4] * 0.5


class HeatPumpConfig1MDI(bytearray):
    id = 1

    @property
    def cool_speed_trim(self):
        return self[0]

    @property
    def heat_speed_trim(self):
        return self[1]


class HeatPumpConfig2MDI(bytearray):
    id = 2

    @property
    def fan_motor_manufacturer_id(self):
        """
        :return: MFG Id
        """
        return self[0]

    @property
    def fan_motor_size(self):
        """
        :return: one of  HEAT_PUMP_FAN_MOTOR_SIZE_* constants
        """
        return self[1]

    @property
    def fan_air_flow(self):
        """
        :return: cfm
        """
        return self[2] << 8 | self[3]


class HeatPumpStatus0MDI(bytearray):
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
        return self[2] * 0.5

    @property
    def cool_request_demand(self):
        """
        :return:
        """
        return self[3] * 0.5

    @property
    def dehumidification_request_demand(self):
        """
        :return:
        """
        return self[4] * 0.5

    @property
    def current_heat_demand(self):
        return self[5] * 0.5

    @property
    def current_cool_demand(self):
        return self[6] * 0.5

    @property
    def defrost_request_demand(self):
        """
        :return:
        """
        return self[7] * 0.5

    @property
    def fan_request_demand(self):
        """
        :return:
        """
        return self[8] * 0.5

    @property
    def fan_request_rate(self):
        """
        :return:
        """
        return self[9]

    @property
    def fan_request_delay(self):
        """
        :return:
        """
        return self[10]

    @property
    def current_dehumidification_demand(self):
        return self[11] * 0.5


