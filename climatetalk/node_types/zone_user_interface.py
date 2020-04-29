# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node
from ..mdi import zone_user_interface, sensors

NODE_TYPE_ZONE_USER_INTERFACE = NodeType(0x16).set_desc('Zone User Interface')


class ZoneUserInterface(Node, zone_user_interface.ZoneUserInterfaceMDI):
    node_type = NODE_TYPE_ZONE_USER_INTERFACE

    @property
    def temperature(self):
        return sensors.ZoneUserInterfaceLocalTempSensorMDI(self.address, self.subnet, self.network).value

    @property
    def humidity(self):
        return sensors.ZoneUserInterfaceHumiditySensorMDI(self.address, self.subnet, self.network).value






