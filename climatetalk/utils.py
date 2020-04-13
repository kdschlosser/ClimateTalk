# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser


def set_bit(value, bit, flag):
    if flag:
        value |= (1 << bit)
    else:
        value &= ~(1 << bit)

    return value


def get_bit(value, bit):
    return value & (1 << bit) != 0

