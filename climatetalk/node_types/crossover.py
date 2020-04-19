# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_CROSSOVER = NodeType(0x09).set_desc('Crossover(aka OBBI)')


class Crossover(akaOBBI)(Node):
    node_type = NODE_TYPE_CROSSOVER

