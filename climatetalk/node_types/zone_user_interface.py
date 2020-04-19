# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_ZONE_USER_INTERFACE = NodeType(0x16).set_desc('Zone User Interface')


class ZoneUserInterface(Node):
    node_type = NODE_TYPE_ZONE_USER_INTERFACE

