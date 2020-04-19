# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node

NODE_TYPE_MEDIA_AIR_CLEANER = NodeType(0x14).set_desc('Media Air Cleaner')


class MediaAirCleaner(Node):
    node_type = NODE_TYPE_MEDIA_AIR_CLEANER

