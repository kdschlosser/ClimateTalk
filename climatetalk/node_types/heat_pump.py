# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node
from ..mdi import heat_pump, sensors

NODE_TYPE_HEAT_PUMP = NodeType(0x05).set_desc('Heat Pump')


class HeatPump(Node, heat_pump.HeatPumpMDI):
    node_type = NODE_TYPE_HEAT_PUMP

    @property
    def outdoor_temperature(self):
        return sensors.HeatPumpOutdoorTempSensorMDI(self.address, self.subnet, self.network).value
