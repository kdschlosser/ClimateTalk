# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node
from ..mdi import sensors

NODE_TYPE_TEMPERATURE_SENSOR = NodeType(0x27).set_desc('Temperature Sensor')


class TemperatureSensor(Node, sensors.RemoteTemperatureSensorMDI):
    node_type = NODE_TYPE_TEMPERATURE_SENSOR