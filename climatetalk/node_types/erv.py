# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_ERV = NodeType(0x0F).set_desc('ERV')


class ERV(Node):
    node_type = NODE_TYPE_ERV

