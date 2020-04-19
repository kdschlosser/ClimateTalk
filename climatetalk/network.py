# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

import socket
import threading

from . import rs485






class Network(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        self.rs485 = rs485.RS485(self)
        self.rs485.start()
        self._read_event = threading.Event()
        self._read_thread = threading.Thread(target=self._read_loop)
        self._read_thread.daemon = True
        self._read_thread.start()

    def recv(self):
        pass

    def send(self):
        pass

    def _read_loop(self):
        # this will actually loop forever or until the program is stopped.
        # a packet is always returned.
        for packet in self.rs485:
            packet.message_type.send(packet)

    def write(self, packet):
        self.rs485.write(packet)

    def stop(self):
        self.rs485.stop()
