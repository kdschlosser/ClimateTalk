# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_HEAT_PUMP = NodeType(0x05).set_desc('Heat Pump')


class HeatPump(Node):
    node_type = NODE_TYPE_HEAT_PUMP

