# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_WEATHER_DATA_DEVICE = NodeType(0x22).set_desc('Weather Data Device')


class WeatherDataDevice(Node):
    node_type = NODE_TYPE_WEATHER_DATA_DEVICE

