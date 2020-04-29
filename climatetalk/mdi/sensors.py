# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

import threading

from ..packet import GetSensorDataRequest, GetSensorDataResponse
from ..utils import (
    get_bit as _get_bit,
    set_bit as _set_bit
)


class SensorBase(object):
    mdi_id = 0

    def __init__(self, address, subnet, network):
        self.address = address
        self.subnet = subnet
        self.network = network

    @property
    def _sensor_data(self):
        packet = GetSensorDataRequest()
        packet.destination = self.address
        packet.subnet = self.subnet
        packet.packet_number = 0x00

        event = threading.Event()

        data = bytearray()

        def callback(response):
            for sensor_data in response:
                if sensor_data.id == self.mdi_id:
                    data.append(sensor_data.data[0] << 8 | sensor_data.data[0])
                    break

            GetSensorDataResponse.message_type.disconnect(
                self.address,
                self.subnet
            )
            event.set()

        GetSensorDataResponse.message_type.connect(
            self.address,
            self.subnet,
            callback
        )

        self.network.send(packet)
        event.wait()
        return data

    @property
    def is_installed(self):
        return _get_bit(self._sensor_data, 15)

    @property
    def value(self):
        value = 0
        data = self._sensor_data

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


class HumiditySensorMDI(SensorBase):
    mdi_id = 0


class SupplyAirTemperatureSensorMDI(SensorBase):
    mdi_id = 0


class ReturnAirTemperatureSensorMDI(SensorBase):
    mdi_id = 0


class OutsideAirTemperatureSensorMDI(SensorBase):
    mdi_id = 0


class FurnaceReturnAirTempSensorMDI(SensorBase):
    mdi_id = 0


class FurnaceSupplyAirTempSensorMDI(SensorBase):
    mdi_id = 1


class AirHandlerReturnAirTempSensorMDI(SensorBase):
    mdi_id = 0


class AirHandlerSupplyAirTempSensorMDI(SensorBase):
    mdi_id = 1


class AirConditionerOutdoorTempSensorMDI(SensorBase):
    mdi_id = 0


class HeatPumpOutdoorTempSensorMDI(SensorBase):
    mdi_id = 0


class CrossoverOutdoorTempSensorMDI(SensorBase):
    mdi_id = 0


class CrossoverReturnAirTempSensorMDI(SensorBase):
    mdi_id = 1


class CrossoverSupplyAirTempSensorMDI(SensorBase):
    mdi_id = 2


class ZoneUserInterfaceLocalTempSensorMDI(SensorBase):
    mdi_id = 0


class ZoneUserInterfaceHumiditySensorMDI(SensorBase):
    mdi_id = 1


class ZoneTemperatureControllerLocalTempSensorMDI(SensorBase):
    mdi_id = 0


class ZoneTemperatureControllerHumiditySensorMDI(SensorBase):
    mdi_id = 1
