# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node
from ..mdi import crossover, sensors

NODE_TYPE_CROSSOVER = NodeType(0x09).set_desc('Crossover')


class Crossover(Node, crossover.CrossoverMDI):
    node_type = NODE_TYPE_CROSSOVER

    @property
    def outdoor_air_temperature(self):
        return sensors.CrossoverOutdoorTempSensorMDI(self.address, self.subnet, self.network).value

    @property
    def return_air_temperature(self):
        return sensors.CrossoverReturnAirTempSensorMDI(self.address, self.subnet, self.network).value

    @property
    def supply_air_temperature(self):
        return sensors.CrossoverSupplyAirTempSensorMDI(self.address, self.subnet, self.network).value
