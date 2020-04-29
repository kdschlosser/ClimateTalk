# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node
from ..mdi import thermostat, sensors

NODE_TYPE_THERMOSTAT = NodeType(0x01).set_desc('Thermostat')


class Thermostat(Node, thermostat.ThermostatMDI):
    node_type = NODE_TYPE_THERMOSTAT

    @property
    def supply_air_temperature(self):
        return sensors.SupplyAirTempSensorMDI(self.address, self.subnet, self.network).value


    @property
    def return_air_temperature(self):
        sensors.ReturnAirTempSensorMDI