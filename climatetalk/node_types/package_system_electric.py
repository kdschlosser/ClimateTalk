# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_PACKAGE_SYSTEM_ELECTRIC = NodeType(0x08).set_desc('Electric Package System')


class PackageSystemElectric(Node):
    node_type = NODE_TYPE_PACKAGE_SYSTEM_ELECTRIC

