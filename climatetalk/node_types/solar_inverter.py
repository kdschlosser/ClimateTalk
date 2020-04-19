# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_SOLAR_INVERTER = NodeType(0x24).set_desc('Solar Inverter')


class SolarInverter(Node):
    node_type = NODE_TYPE_SOLAR_INVERTER

