# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_IAQ_ANALYZER = NodeType(0x13).set_desc('IAQ Analyzer')


class IAQAnalyzer(Node):
    node_type = NODE_TYPE_IAQ_ANALYZER

