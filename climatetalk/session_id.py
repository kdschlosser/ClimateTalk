# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

import uuid


class SessionId(bytearray):

    @classmethod
    def create(cls):
        guid = uuid.uuid4()
        sess = guid.int & (1 << 64) - 1
        sess_id = [
            sess >> 56 & 0xFF,
            sess >> 48 & 0xFF,
            sess >> 40 & 0xFF,
            sess >> 32 & 0xFF,
            sess >> 24 & 0xFF,
            sess >> 16 & 0xFF,
            sess >> 8 & 0xFF,
            sess & 0xFF
        ]

        return cls(sess_id)

    def __init__(self, *args, **kwargs):
        try:
            bytearray.__init__(self, *args, **kwargs)
        except TypeError:
            bytearray.__init__(self)

    @property
    def value(self):
        return (
            self[0] << 56 |
            self[1] << 48 |
            self[2] << 40 |
            self[3] << 32 |
            self[4] << 24 |
            self[5] << 16 |
            self[6] << 8 |
            self[7]
        )
