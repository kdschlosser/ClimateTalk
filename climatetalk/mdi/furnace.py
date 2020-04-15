# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser


from ..utils import (
    get_bit as _get_bit,
    set_bit as _set_bit
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


class FurnaceConnfig0MDI(bytearray):

    id = 0

    @property
    def fan_speeds(self):
        """
        :return: 0x0F = variable
        """
        return self[0] << 4 & 0xF

    @property
    def inducer_stages(self):
        """
        :return: 0x0F = variable
        """
        return self[0] & 0xF

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
    def pressure_sensor_type(self):
        """
        :return: one of FURNACE_PRESSURE_SENSOR_TYPE_* constants
        """
        res = 0
        res = _set_bit(res, 1, _get_bit(self[2], 7))
        res = _set_bit(res, 0, _get_bit(self[2], 6))
        return res

    @property
    def ignition_type(self):
        """
        :return: one of FURNACE_IGNITION_TYPE_* constants
        """
        res = 0
        res = _set_bit(res, 1, _get_bit(self[2], 5))
        res = _set_bit(res, 0, _get_bit(self[2], 4))
        return res

    @property
    def fuel_type(self):
        """
        :return: one of FURNACE_FUEL_TYPE_* constants
        """
        res = 0
        res = _set_bit(res, 1, _get_bit(self[2], 3))
        res = _set_bit(res, 0, _get_bit(self[2], 2))
        return res

    @property
    def hvac_operation(self):
        """
        :return: one of FURNACE_OPERATION_TYPE_* constants
        """
        res = 0
        res = _set_bit(res, 1, _get_bit(self[2], 1))
        res = _set_bit(res, 0, _get_bit(self[2], 0))
        return res

    @property
    def cool_humidification_capable(self):
        """
        :return: FURNACE_CAPABLE or FURNACE_NOT_CAPABLE
        """
        return int(_get_bit(self[3], 2))

    @property
    def humidification_capable(self):
        """
        :return: FURNACE_CAPABLE or FURNACE_NOT_CAPABLE
        """
        return int(_get_bit(self[3], 1))

    @property
    def dehumidification_capable(self):
        """
        :return: FURNACE_CAPABLE or FURNACE_NOT_CAPABLE
        """
        return int(_get_bit(self[3], 0))

    @property
    def btu_output(self):
        """
        :return: BTU's
        """
        return self[4] * 1000

    @property
    def circulator_blower_manufacturer_id(self):
        """
        :return: MFG Id
        """
        return self[5]

    @property
    def circulator_blower_size(self):
        """
        :return: one of  FURNACE_CIRCULATOR_BLOWER_SIZE_* constants
        """
        return self[6]

    @property
    def circulator_blower_air_flow(self):
        """
        :return: cfm
        """
        return self[7] << 8 | self[8]


class FurnaceConfig1MDI(bytearray):
    id = 1

    @property
    def cool_cfm_per_ton(self):
        return self[0]

    @property
    def cool_tonnage(self):
        return ((self[1] >> 4) & 0xF) + ((self[1] & 0xF) / 10.0)

    @property
    def heat_cfm(self):
        return self[2] / 10

    @property
    def cool_cfm_trim(self):
        if self[3]:
            return self[3] - 100

        return 0

    @property
    def heat_cfm_adjust(self):
        if self[4]:
            return self[4] - 100

        return 0
