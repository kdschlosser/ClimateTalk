# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node
from ..mdi import air_conditioner, sensors

NODE_TYPE_AIR_CONDITIONER = NodeType(0x04).set_desc('Air Conditioner')


class AirConditioner(Node, air_conditioner.AirConditionerMDI):
    node_type = NODE_TYPE_AIR_CONDITIONER

    @property
    def outdoor_temperature(self):
        return sensors.AirConditionerOutdoorTempSensorMDI(self.address, self.subnet, self.network).value

