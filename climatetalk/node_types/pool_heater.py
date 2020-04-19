# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_POOL_HEATER = NodeType(0x1B).set_desc('Pool Heater')


class PoolHeater(Node):
    node_type = NODE_TYPE_POOL_HEATER

