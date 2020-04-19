# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_SECONDARY_COMPRESSOR = NodeType(0x0A).set_desc('Secondary Compressor')


class SecondaryCompressor(Node):
    node_type = NODE_TYPE_SECONDARY_COMPRESSOR

