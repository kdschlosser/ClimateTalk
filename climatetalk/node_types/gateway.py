# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_GATEWAY = NodeType(0x1D).set_desc('Gateway')


class Gateway(Node):
    node_type = NODE_TYPE_GATEWAY

