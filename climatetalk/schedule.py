# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

import threading
import datetime


class ScheduleThread(object):

    def __init__(self, scheduled_items):
        self._event = threading.Event()
        self._thread = None
        self._schedule_items = scheduled_items

    def start(self):
        if self._thread is None:
            self._thread = threading.Thread(target=self.run)
            self._thread.daemon = True
            self._thread.start()

    def stop(self):
        self._event.set()
        if self._thread is not None:
            self._thread.join()

    def run(self):
        self._event.clear()

        while not self._event.is_set():
            dt = datetime.datetime.now()

            for schedule in self._schedule_items[:]:
                if schedule >= dt:
                    schedule.run()

            self._event.wait(60.0)


class Schedule(object):

    def __init__(self, network):
        self._network = network
        self._file_path = None

    def load(self, file_path):
        self._file_path = file_path





class ScheduleItem(datetime):

    def set_device(self, device):

    def set_command(self, command, value):

        self._device.