# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node
from ..mdi import furnace

NODE_TYPE_ELECTRIC_FURNACE = NodeType(0x06).set_desc('Electric Furnace')


class FurnaceElectric(Node, furnace.FurnaceMDI):
    node_type = NODE_TYPE_ELECTRIC_FURNACE

