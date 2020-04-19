# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_WHOLE_HOUSE_FAN = NodeType(0x23).set_desc('Whole House Fan')


class WholeHouseFan(Node):
    node_type = NODE_TYPE_WHOLE_HOUSE_FAN

