# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node
from ..mdi import motor

NODE_TYPE_WHOLE_HOUSE_FAN = NodeType(0x23).set_desc('Whole House Fan')


class WholeHouseFan(Node, motor.MotorMDI):
    node_type = NODE_TYPE_WHOLE_HOUSE_FAN

