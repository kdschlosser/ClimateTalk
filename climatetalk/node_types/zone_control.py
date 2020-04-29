# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node
from ..mdi import zone_controller
NODE_TYPE_ZONE_CONTROL = NodeType(0x15).set_desc('Zone Control')


class ZoneControl(Node, zone_controller.ZoneControllerMDI):
    node_type = NODE_TYPE_ZONE_CONTROL

