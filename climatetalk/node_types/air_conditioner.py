# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_AIR_CONDITIONER = NodeType(0x04).set_desc('Air Conditioner')


class AirConditioner(Node):
    node_type = NODE_TYPE_AIR_CONDITIONER

