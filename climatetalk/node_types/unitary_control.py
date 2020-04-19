# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_UNITARY_CONTROL = NodeType(0x0C).set_desc('Unitary Control')


class UnitaryControl(Node):
    node_type = NODE_TYPE_UNITARY_CONTROL

