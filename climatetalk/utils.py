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


class TwosCompliment(object):

    @staticmethod
    def encode(value, num_bits):
        if value < 0:
            value = (1 << num_bits) + value
        elif value & (1 << (num_bits - 1)) != 0:
            # If sign bit is set.
            # compute negative value.
            value = value - (1 << num_bits)

        return value

    @staticmethod
    def decode(value, num_bits):
        return value - (1 << num_bits)

