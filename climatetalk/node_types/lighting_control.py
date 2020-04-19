# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_LIGHTING_CONTROL = NodeType(0x1F).set_desc('Lighting Control')


class LightingControl(Node):
    node_type = NODE_TYPE_LIGHTING_CONTROL

