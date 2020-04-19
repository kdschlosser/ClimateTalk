# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_HUMIDIFIER_STEAM = NodeType(0x11).set_desc('Steam Humidifier')


class HumidifierSteam(Node):
    node_type = NODE_TYPE_HUMIDIFIER_STEAM

