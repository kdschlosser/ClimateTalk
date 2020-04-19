# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_DIAGNOSTIC_DEVICE = NodeType(0x1E).set_desc('Diagnostic Device')


class DiagnosticDevice(Node):
    node_type = NODE_TYPE_DIAGNOSTIC_DEVICE

