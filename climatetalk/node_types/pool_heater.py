# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node
from ..mdi import water_heater

NODE_TYPE_POOL_HEATER = NodeType(0x1B).set_desc('Pool Heater')


class PoolHeater(Node, water_heater.WaterHeaterMDI):
    node_type = NODE_TYPE_POOL_HEATER

