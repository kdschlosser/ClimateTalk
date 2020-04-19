# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_WATER_HEATER_GAS = NodeType(0x18).set_desc('Gas Water Heater')


class WaterHeaterGas(Node):
    node_type = NODE_TYPE_WATER_HEATER_GAS

