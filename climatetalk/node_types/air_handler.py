# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_AIR_HANDLER = NodeType(0x03).set_desc('Air Handler')


class AirHandler(Node):
    node_type = NODE_TYPE_AIR_HANDLER

