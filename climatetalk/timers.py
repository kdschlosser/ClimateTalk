# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

import ctypes
import sys
import threading


# OS-specific low-level timing functions:
if sys.platform.startswith('win'):  # for Windows:
    def micros():
        """return a timestamp in microseconds (us)"""
        tics = ctypes.c_int64()
        freq = ctypes.c_int64()

        # get ticks on the internal ~2MHz QPC clock
        ctypes.windll.Kernel32.QueryPerformanceCounter(ctypes.byref(tics))
        # get the actual freq. of the internal ~2MHz QPC clock
        ctypes.windll.Kernel32.QueryPerformanceFrequency(ctypes.byref(freq))

        t_us = tics.value * 1e6 / freq.value
        return t_us

    def millis():
        """return a timestamp in milliseconds (ms)"""
        tics = ctypes.c_int64()
        freq = ctypes.c_int64()

        # get ticks on the internal ~2MHz QPC clock
        ctypes.windll.Kernel32.QueryPerformanceCounter(ctypes.byref(tics))
        # get the actual freq. of the internal ~2MHz QPC clock
        ctypes.windll.Kernel32.QueryPerformanceFrequency(ctypes.byref(freq))

        t_ms = tics.value * 1e3 / freq.value
        return t_ms

else:  # for Linux:
    import os

    # Constants:
    # see <linux/time.h> here:
    # https://github.com/torvalds/linux/blob/master/include/uapi/linux/time.h
    CLOCK_MONOTONIC_RAW = 4
    # prepare ctype timespec structure of {long, long}

    class timespec(ctypes.Structure):
        _fields_ = [
            ('tv_sec', ctypes.c_long),
            ('tv_nsec', ctypes.c_long)
        ]

    # Configure Python access to the clock_gettime C library, via ctypes:
    # Documentation:
    # -ctypes.CDLL: https://docs.python.org/3.2/library/ctypes.html
    # -librt.so.1 with clock_gettime:
    # https://docs.oracle.com/cd/E36784_01/html/E36873/librt-3lib.html
    # -Linux clock_gettime(): http://linux.die.net/man/3/clock_gettime
    librt = ctypes.CDLL('librt.so.1', use_errno=True)
    clock_gettime = librt.clock_gettime

    # specify input arguments and types to the C clock_gettime() function
    # (int clock_ID, timespec* t)
    clock_gettime.argtypes = [ctypes.c_int, ctypes.POINTER(timespec)]

    def monotonic_time():
        """return a timestamp in seconds (sec)"""
        t = timespec()

        # (Note that clock_gettime() returns 0 for success, or -1 for failure, in
        # which case errno is set appropriately)
        # -see here: http://linux.die.net/man/3/clock_gettime
        if clock_gettime(CLOCK_MONOTONIC_RAW , ctypes.pointer(t)) != 0:
            # if clock_gettime() returns an error
            errno_ = ctypes.get_errno()

            raise OSError(errno_, os.strerror(errno_))

        return t.tv_sec + t.tv_nsec * 1e-9  # sec

    def micros():
        """return a timestamp in microseconds (us)"""
        return monotonic_time() * 1e6  # us

    def millis():
        """eturn a timestamp in milliseconds (ms)"""
        return monotonic_time() * 1e3  # ms


# Other timing functions:
def delay(delay_ms):
    """delay for delay_ms milliseconds (ms)"""
    t_start = millis()
    while millis() - t_start < delay_ms:
        pass  # do nothing

    return


def delay_microseconds(delay_us):
    """delay for delay_us microseconds (us)"""
    t_start = micros()
    while micros() - t_start < delay_us:
        pass  # do nothing

    return


# Classes
class TimerUS(object):
    def __init__(self):
        self.start = 0
        self.reset()

    def reset(self):
        self.start = micros()

    def elapsed(self):
        now = micros()
        return now - self.start


class TimerMS(object):
    def __init__(self):
        self.start = 0
        self.reset()

    def reset(self):
        self.start = millis()

    def elapsed(self):
        now = millis()
        return now - self.start


class BusyTimer(object):

    def __init__(self, timer, threshold, func):
        self.timer = timer
        self.threshold = threshold
        self.func = func
        self._thread = None
        self._event = threading.Event()

    def start(self):
        self._event.set()
        self._thread = threading.Thread(target=self._run)
        self._thread.daemon = True
        self._thread.start()

    def _run(self):
        self._event.clear()
        self.timer.reset()
        while (
            self.timer.elapsed() < self.threshold() and
            not self._event.is_set()
        ):
            pass

        if not self._event.is_set():
            self.func()

    @property
    def is_running(self):
        return self.timer.elapsed() > self.threshold
