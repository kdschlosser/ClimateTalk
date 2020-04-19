# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_ELECTRONIC_AIR_CLEANER = NodeType(0x0E).set_desc('Electronic Air Cleaner')


class ElectronicAirCleaner(Node):
    node_type = NODE_TYPE_ELECTRONIC_AIR_CLEANER

