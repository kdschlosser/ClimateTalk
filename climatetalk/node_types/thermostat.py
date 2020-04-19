# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_THERMOSTAT = NodeType(0x01).set_desc('Thermostat')


class Thermostat(Node):
    node_type = NODE_TYPE_THERMOSTAT

