# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_SECURITY_SYSTEM = NodeType(0x20).set_desc('Security System')


class SecuritySystem(Node):
    node_type = NODE_TYPE_SECURITY_SYSTEM

