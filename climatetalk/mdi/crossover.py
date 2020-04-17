# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser


from ..utils import (
    get_bit as _get_bit,
    set_bit as _set_bit
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


class CrossoverConfig0MDI(bytearray):
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
    def aux_stages(self):
        """
        :return: 0x0F = variable
        """
        return self[2] << 4 & 0xF

    @property
    def indoor_heat_type(self):
        """
        :return: one of CROSSOVER_HEAT_TYPE_* constants
        """
        return int(_get_bit(self[2], 3))

    @property
    def outdoor_equip_type(self):
        """
        :return: one of CROSSOVER_OUTDOOR_EQUIP_TYPE_* constants
        """
        return int(_get_bit(self[2], 2))

    @property
    def configured_equip_type(self):
        """
        :return: one of CROSSOVER_EQUIP_TYPE_* constants
        """
        return int(_get_bit(self[2], 0))

    @property
    def mode_of_operation(self):
        """
        :return: one of CROSSOVER_OPERATION_TYPE_* constants
        """
        return int(_get_bit(self[2], 0))

    @property
    def humidification(self):
        """
        :return: CROSSOVER_ENABLED or CROSSOVER_DISABLED
        """
        return int(_get_bit(self[3], 1))

    @property
    def dehumidification(self):
        """
        :return: CROSSOVER_ENABLED or CROSSOVER_DISABLED
        """
        return int(_get_bit(self[3], 0))

    @property
    def independent_humidification(self):
        """
        :return: CROSSOVER_ENABLED or CROSSOVER_DISABLED
        """
        return int(_get_bit(self[4], 7))

    @property
    def independent_dehumidification(self):
        """
        :return: CROSSOVER_ENABLED or CROSSOVER_DISABLED
        """
        return int(_get_bit(self[4], 6))

    @property
    def speed_trim(self):
        res = 0
        res = _set_bit(res, 1, _get_bit(self[5], 5))
        res = _set_bit(res, 0, _get_bit(self[5], 4))

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
        res = _set_bit(res, 1, _get_bit(self[5], 3))
        res = _set_bit(res, 0, _get_bit(self[5], 2))

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
        res = _set_bit(res, 1, _get_bit(self[5], 1))
        res = _set_bit(res, 0, _get_bit(self[5], 0))
        if res == 0:
            return 2
        if res == 1:
            return 3
        if res == 2:
            return 4
        if res == 3:
            return 5


class CrossoverConfig1MDI(bytearray):
    id = 1

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
    def aux_stages(self):
        """
        :return: 0x0F = variable
        """
        return self[2] << 4 & 0xF

    @property
    def humidification(self):
        """
        :return: CROSSOVER_CAPABLE or CROSSOVER_NOT_CAPABLE
        """
        return int(_get_bit(self[3], 1))

    @property
    def dehumidification(self):
        """
        :return: CROSSOVER_CAPABLE or CROSSOVER_NOT_CAPABLE
        """
        return int(_get_bit(self[3], 0))

    @property
    def independent_humidification(self):
        """
        :return: CROSSOVER_CAPABLE or CROSSOVER_NOT_CAPABLE
        """
        return int(_get_bit(self[4], 7))

    @property
    def independent_dehumidification(self):
        """
        :return: CROSSOVER_CAPABLE or CROSSOVER_NOT_CAPABLE
        """
        return int(_get_bit(self[4], 6))


CROSSOVER_FAN_STATUS_AUTO = 0x00
CROSSOVER_FAN_STATUS_ALWAYS_ON = 0x01
CROSSOVER_FAN_STATUS_OCCUPIED_ON = 0x02


class CrossoverStatus0MDI(bytearray):
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
    def fan_request_mode(self):
        """
        :return: one of CROSSOVER_FAN_STATUS_* constants
        """
        return self[4]

    @property
    def fan_request_demand(self):
        """
        :return:
        """
        return self[5] * 0.5

    @property
    def fan_request_rate(self):
        """
        :return:
        """
        return self[6]

    @property
    def defrost_request_demand(self):
        """
        :return:
        """
        return self[7] * 0.5

    @property
    def dehumidification_request_demand(self):
        """
        :return:
        """
        return self[8] * 0.5

    @property
    def humidification_request_demand(self):
        """
        :return:
        """
        return self[9] * 0.5


    @property
    def emergency_request_demand(self):
        """
        :return:
        """
        return self[10] * 0.5

    @property
    def aux_request_demand(self):
        """
        :return:
        """
        return self[11] * 0.5

    @property
    def current_indoor_heat_demand(self):
        return self[12] * 0.5

    @property
    def current_outdoor_heat_demand(self):
        return self[13] * 0.5

    @property
    def current_cool_demand(self):
        return self[14] * 0.5

    @property
    def current_fan_demand(self):
        return self[15] * 0.5

    @property
    def current_fan_demand_rate(self):
        return self[16]

    @property
    def current_fan_delay_remaining(self):
        return self[17]

    @property
    def current_humidification_demand(self):
        return self[18] * 0.5

    @property
    def current_dehumidification_demand(self):
        return self[19] * 0.5

    @property
    def emulated_defrost_demand(self):
        return self[20] * 0.5

    @property
    def emulated_fan_demand(self):
        return self[21] * 0.5

    @property
    def emulated_fan_demand_rate(self):
        return self[22]
