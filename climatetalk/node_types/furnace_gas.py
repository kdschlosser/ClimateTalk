# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node
from ..mdi import furnace, sensors

NODE_TYPE_GAS_FURNACE = NodeType(0x02).set_desc('Gas Furnace')


class FurnaceGas(Node, furnace.FurnaceMDI):
    node_type = NODE_TYPE_GAS_FURNACE

    @property
    def supply_air_temperature(self):
        return sensors.FurnaceSupplyAirTempSensorMDI(self.address, self.subnet, self.network).value


    @property
    def return_air_temperature(self):
        return sensors.FurnaceReturnAirTempSensorMDI(self.address, self.subnet, self.network).value