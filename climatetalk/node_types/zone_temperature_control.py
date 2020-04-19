# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_ZONE_TEMPERATURE_CONTROL = NodeType(0x26).set_desc('Zone Temperature Control')


class ZoneTemperatureControl(Node):
    node_type = NODE_TYPE_ZONE_TEMPERATURE_CONTROL

