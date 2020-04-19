# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

import threading


class Signal(object):

    def __init__(self):
        self._callbacks = {}

    def send(self, signal, packet):
        address = packet.address
        subnet = packet.subnet

        try:
            self._callbacks[signal][(address, subnet)](packet)
        except KeyError:
            pass

    def connect(self, signal, address, subnet, callback):
        if signal not in self._callbacks:
            self._callbacks[signal] = {}

        self._callbacks[signal][(address, subnet)] = callback

    def disconnect(self, signal, address, subnet):
        try:
            del self._callbacks[signal][(address, subnet)]
        except KeyError:
            pass


_signal = Signal()


def connect(signal, address, subnet, callback):
    _signal.connect(signal, address, subnet, callback)


def disconnect(signal, address, subnet):
    _signal.disconnect(signal, address, subnet)


def send(signal, packet):
    _signal.send(signal, packet)
