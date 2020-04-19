# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_UV_LIGHT = NodeType(0x21).set_desc('UV Light')


class UVLight(Node):
    node_type = NODE_TYPE_UV_LIGHT

