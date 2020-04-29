# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node
from ..mdi import water_heater

NODE_TYPE_WATER_HEATER_COMMERCIAL = NodeType(0x1A).set_desc('Commercial Water Heater')


class WaterHeaterCommercial(Node, water_heater.WaterHeaterMDI):
    node_type = NODE_TYPE_WATER_HEATER_COMMERCIAL

