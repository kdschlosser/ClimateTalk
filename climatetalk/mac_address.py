# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

import uuid


class MACAddress(bytearray):

    def __init__(self, *args, **kwargs):
        try:
            bytearray.__init__(self, *args, **kwargs)
        except TypeError:
            bytearray.__init__(self)

    @property
    def value(self):
        return (
            self[1] << 48 |
            self[2] << 40 |
            self[3] << 32 |
            self[4] << 24 |
            self[5] << 16 |
            self[6] << 8 |
            self[7]
        )

    @classmethod
    def create(cls):
        guid = uuid.uuid4()
        mac = guid.int & (1 << 56) - 1
        mac_address = [
            0x00,
            mac >> 48 & 0xFF,
            mac >> 40 & 0xFF,
            mac >> 32 & 0xFF,
            mac >> 24 & 0xFF,
            mac >> 16 & 0xFF,
            mac >> 8 & 0xFF,
            mac & 0xFF
        ]
        return cls(mac_address)

    @property
    def manufacturer_id(self):
        return self[1] << 8 | self[2]

    @property
    def id(self):
        return (
            self[3] << 32 |
            self[4] << 24 |
            self[5] << 16 |
            self[6] << 8 |
            self[7]
        )
