# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser


class ZoneDamperStatus0MDI(bytearray):
    id = 0

    @property
    def critical_fault(self):

        return self[0]

    @property
    def minor_fault(self):
        return self[1]

    @property
    def request_position(self):
        return self[2] * 0.5

    @property
    def position(self):
        return self[3] * 0.5
