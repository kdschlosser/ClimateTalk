# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_BOILER = NodeType(0x17).set_desc('Boiler')


class Boiler(Node):
    node_type = NODE_TYPE_BOILER

