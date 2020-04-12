# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

import threading
import logging
from . import timers
from .packet import Packet

logger = logging.getLogger(__name__)


INTERPACKET_DELAY_THRESHOLD = 100000
INTERCHAR_DELAY_THRESHOLD = 3500

NETWORK_COORDINATOR = 0xFF
BROADCAST = 0x00
CT_ISUM1 = 0xAA  # New Fletcher Seed.
CT_ISUM2 = 0x00

BROADCAST_SUBNET = 0x00


class RS485Com(object):

    def __init__(self, serial):
        self.serial = serial
        self._thread = None
        self._event = threading.Event()
        self._lock = threading.Lock()
        self.packet = bytearray()
        self.inter_char_timer = timers.BusyTimer(
            timers.TimerUS(),
            INTERCHAR_DELAY_THRESHOLD,
            self._queue_packet
        )
        self._recv_queue = []
        self._queue_event = threading.Event()
        self._send_lock = threading.Lock()

    def write(self, packet):
        packet.calc_checksum()
        with self._send_lock:
            packet_timer = timers.TimerUS()
            self.serial.write(packet)
            while packet_timer.elapsed() < INTERPACKET_DELAY_THRESHOLD:
                pass

    def start(self):
        if self._thread is None:
            self._thread = threading.Thread(target=self._run)
            self._thread.daemon = True
            self._thread.start()

    def _queue_packet(self):
        packet = self.packet
        self.packet = bytearray()

        self._recv_queue.append(packet)
        self._queue_event.set()

    def __iter__(self):
        while not self._event.is_set():
            self._queue_event.wait()
            while self._recv_queue:
                yield Packet(self._recv_queue.pop(0))
            self._queue_event.clear()

    def _run(self):
        packet_timer = timers.TimerUS()
        self._queue_event.clear()
        self._event.clear()
        del self._recv_queue[:]

        while not self._event.is_set():
            char = self.serial.recv(1)

            if char:
                if self.inter_char_timer.is_running:
                    self.packet += bytearray(char)
                    packet_timer.reset()
                    self.inter_char_timer.start()

                if packet_timer.elapsed() >= INTERPACKET_DELAY_THRESHOLD:
                    self.packet = bytearray(char)
                    self.inter_char_timer.start()
                    packet_timer.reset()

        self._thread = None

    def stop(self):
        self._event.set()
        self._queue_event.set()
        if self._thread is not None:
            self._thread.join()
