# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_ZONE_CONTROL = NodeType(0x15).set_desc('Zone Control')


class ZoneControl(Node):
    node_type = NODE_TYPE_ZONE_CONTROL

