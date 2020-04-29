# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node
from ..mdi import sensors

NODE_TYPE_OCCUPANCY_SENSOR = NodeType(0x28).set_desc('Occupancy Sensor')


class OccupancySensor(Node, sensors.OccupancySensorMDI):
    node_type = NODE_TYPE_OCCUPANCY_SENSOR




