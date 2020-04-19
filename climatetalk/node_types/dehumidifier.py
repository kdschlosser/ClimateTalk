# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_DEHUMIDIFIER = NodeType(0x0D).set_desc('Dehumidifier')


class Dehumidifier(Node):
    node_type = NODE_TYPE_DEHUMIDIFIER

