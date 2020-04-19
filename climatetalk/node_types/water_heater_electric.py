# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_WATER_HEATER_ELECTRIC = NodeType(0x19).set_desc('Electric Water Heater')


class WaterHeaterElectric(Node):
    node_type = NODE_TYPE_WATER_HEATER_ELECTRIC

