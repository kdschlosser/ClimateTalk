# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_CEILING_FAN = NodeType(0x1C).set_desc('Ceiling Fan')


class CeilingFan(Node):
    node_type = NODE_TYPE_CEILING_FAN

