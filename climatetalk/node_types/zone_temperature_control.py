# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node
from ..mdi import zone_temperature_controller, sensors

NODE_TYPE_ZONE_TEMPERATURE_CONTROL = NodeType(0x26).set_desc('Zone Temperature Control')


class ZoneTemperatureControl(Node, zone_temperature_controller.ZoneTemperatureControllerMDI):
    node_type = NODE_TYPE_ZONE_TEMPERATURE_CONTROL

    @property
    def temperature(self):
        return sensors.ZoneTemperatureControllerLocalTempSensorMDI(self.address, self.subnet, self.network).value

    @property
    def humidity(self):
        return sensors.ZoneTemperatureControllerHumiditySensorMDI(self.address, self.subnet, self.network).value
