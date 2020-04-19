# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_PACKAGE_SYSTEM_GAS = NodeType(0x07).set_desc('Gas Package System')


class PackageSystemGas(Node):
    node_type = NODE_TYPE_PACKAGE_SYSTEM_GAS

