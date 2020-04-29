# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node
from ..mdi import zone_damper

NODE_TYPE_ZONE_DAMPER = NodeType(0x25).set_desc('Zone Damper')


class ZoneDamper(Node, zone_damper.ZoneDamperMDI):
    node_type = NODE_TYPE_ZONE_DAMPER

