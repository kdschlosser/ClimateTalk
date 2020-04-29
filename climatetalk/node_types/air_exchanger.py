# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node
from ..mdi import air_handler

NODE_TYPE_AIR_EXCHANGER = NodeType(0x0B).set_desc('Air Exchanger')


class AirExchanger(Node, air_handler.AirHandlerMDI):
    node_type = NODE_TYPE_AIR_EXCHANGER

