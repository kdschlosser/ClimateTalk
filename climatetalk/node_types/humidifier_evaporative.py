# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_HUMIDIFIER_EVAPORATIVE = NodeType(0x10).set_desc('Evaporative Humidifier')


class HumidifierEvaporative(Node):
    node_type = NODE_TYPE_HUMIDIFIER_EVAPORATIVE

