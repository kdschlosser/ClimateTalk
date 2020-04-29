# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node
from ..mdi import water_heater

NODE_TYPE_WATER_HEATER_ELECTRIC = NodeType(0x19).set_desc('Electric Water Heater')


class WaterHeaterElectric(Node, water_heater.WaterHeaterMDI):
    node_type = NODE_TYPE_WATER_HEATER_ELECTRIC

