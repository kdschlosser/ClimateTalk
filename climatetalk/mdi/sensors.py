# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from ..utils import (
    get_bit as _get_bit,
    set_bit as _set_bit
)


class OccupancySensor0MDI(bytearray):
    id = 0

    @property
    def critical_fault(self):
        return self[0]

    @property
    def minor_fault(self):
        return self[1]

    @property
    def value(self):
        return bool(self[2])


class TempSensor0MDI(bytearray):
    id = 0

    @property
    def is_installed(self):
        value = self[0] << 8 | self[1]

        return _get_bit(value, 15)

    @property
    def value(self):
        value = 0
        data = self[0] << 8 | self[1]

        value = _set_bit(value, 9, _get_bit(data, 13))
        value = _set_bit(value, 8, _get_bit(data, 12))
        value = _set_bit(value, 7, _get_bit(data, 11))
        value = _set_bit(value, 6, _get_bit(data, 10))
        value = _set_bit(value, 5, _get_bit(data, 9))
        value = _set_bit(value, 4, _get_bit(data, 8))
        value = _set_bit(value, 3, _get_bit(data, 7))
        value = _set_bit(value, 2, _get_bit(data, 6))
        value = _set_bit(value, 1, _get_bit(data, 5))
        value = _set_bit(value, 0, _get_bit(data, 4))

        fractional = 0
        fractional = _set_bit(fractional, 3, _get_bit(data, 3))
        fractional = _set_bit(fractional, 2, _get_bit(data, 2))
        fractional = _set_bit(fractional, 1, _get_bit(data, 1))
        fractional = _set_bit(fractional, 0, _get_bit(data, 0))

        value += (fractional * 16) / 100.0

        if _get_bit(data, 14):
            value = -value

        return value


class TempSensor1MDI(bytearray):
    id = 1

    @property
    def is_installed(self):
        value = self[2] << 8 | self[3]

        return _get_bit(value, 15)

    @property
    def value(self):
        value = 0
        data = self[2] << 8 | self[3]

        value = _set_bit(value, 9, _get_bit(data, 13))
        value = _set_bit(value, 8, _get_bit(data, 12))
        value = _set_bit(value, 7, _get_bit(data, 11))
        value = _set_bit(value, 6, _get_bit(data, 10))
        value = _set_bit(value, 5, _get_bit(data, 9))
        value = _set_bit(value, 4, _get_bit(data, 8))
        value = _set_bit(value, 3, _get_bit(data, 7))
        value = _set_bit(value, 2, _get_bit(data, 6))
        value = _set_bit(value, 1, _get_bit(data, 5))
        value = _set_bit(value, 0, _get_bit(data, 4))

        fractional = 0
        fractional = _set_bit(fractional, 3, _get_bit(data, 3))
        fractional = _set_bit(fractional, 2, _get_bit(data, 2))
        fractional = _set_bit(fractional, 1, _get_bit(data, 1))
        fractional = _set_bit(fractional, 0, _get_bit(data, 0))

        value += (fractional * 16) / 100.0

        if _get_bit(data, 14):
            value = -value

        return value


class HumiditySensor0MDI(bytearray):
    id = 0

    @property
    def is_installed(self):
        value = self[0] << 8 | self[1]

        return _get_bit(value, 15)

    @property
    def value(self):
        value = 0
        data = self[0] << 8 | self[1]

        value = _set_bit(value, 9, _get_bit(data, 13))
        value = _set_bit(value, 8, _get_bit(data, 12))
        value = _set_bit(value, 7, _get_bit(data, 11))
        value = _set_bit(value, 6, _get_bit(data, 10))
        value = _set_bit(value, 5, _get_bit(data, 9))
        value = _set_bit(value, 4, _get_bit(data, 8))
        value = _set_bit(value, 3, _get_bit(data, 7))
        value = _set_bit(value, 2, _get_bit(data, 6))
        value = _set_bit(value, 1, _get_bit(data, 5))
        value = _set_bit(value, 0, _get_bit(data, 4))

        fractional = 0
        fractional = _set_bit(fractional, 3, _get_bit(data, 3))
        fractional = _set_bit(fractional, 2, _get_bit(data, 2))
        fractional = _set_bit(fractional, 1, _get_bit(data, 1))
        fractional = _set_bit(fractional, 0, _get_bit(data, 0))

        value += (fractional * 16) / 100.0

        return value


class SupplyAirTemperatureSensor(TempSensor0MDI):
    id = 0


class ReturnAirTemperatureSensor(TempSensor0MDI):
    id = 0


class OutsideAirTemperatureSensor(TempSensor0MDI):
    id = 0


class RemoteTemperatureSensor(TempSensor0MDI):
    id = 0


class FurnaceReturnAirTempSensorMDI(TempSensor0MDI):
    id = 0


class FurnaceSupplyAirTempSensorMDI(TempSensor1MDI):
    id = 1


class AirHandlerReturnAirTempSensorMDI(TempSensor0MDI):
    id = 0


class AirHandlerFurnaceSupplyAirTempSensorMDI(TempSensor1MDI):
    id = 1


class AirConditionerOutdoorTempSensorMDI(TempSensor0MDI):
    id = 0


class HeatPumpOutdoorTempSensorMDI(TempSensor0MDI):
    id = 0


class CrossoverOutdoorTempSensorMDI(TempSensor0MDI):
    id = 0


class CrossoverReturnAirTempSensorMDI(TempSensor0MDI):
    id = 1


class CrossoverSupplyAirTempSensorMDI(TempSensor0MDI):
    id = 2


class ZoneUserInterfaceLocalTempSensorMDI(TempSensor0MDI):
    id = 0


class ZoneUserInterfaceHumiditySensorMDI(HumiditySensor0MDI):
    id = 1


class ZoneTemperatureControllerLocalTempSensorMDI(TempSensor0MDI):
    id = 0


class ZoneTemperatureControllerHumiditySensorMDI(HumiditySensor0MDI):
    id = 1
