# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_HRV = NodeType(0x12).set_desc('HRV')


class HRV(Node):
    node_type = NODE_TYPE_HRV

