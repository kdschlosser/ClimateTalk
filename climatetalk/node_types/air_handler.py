# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node
from ..mdi import air_handler, sensors

NODE_TYPE_AIR_HANDLER = NodeType(0x03).set_desc('Air Handler')


class AirHandler(Node, air_handler.AirHandlerMDI):
    node_type = NODE_TYPE_AIR_HANDLER

    @property
    def supply_air_temperature(self):
        return sensors.AirHandlerSupplyAirTempSensorMDI(self.address, self.subnet, self.network).value

    @property
    def return_air_temperature(self):
        return sensors.AirHandlerReturnAirTempSensorMDI(self.address, self.subnet, self.network).value

