# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser


# this is only here for the sake of completeness If a user wants to be able to access
# these MDI classes then they will be able to.
# I am going to add a python powered schedule that is going to allow fo a more fine grained control
# these MDI classes only allow for a precision of 15 minutes which is not quite enough. it also
# only allows for 7 days at 4 times a day at most. The scheduling I am going to add
# will be able to be done on a weekly schedule if wanted or they can set specific dates, There
# is going to be no limit to the number of scheduled items. I am also going to have it dump the scheduled
# items to XML so on restart there will be no need to reload them.

import datetime
from ..utils import (
    get_bit as _get_bit,
    set_bit as _set_bit
)

SCHEDULE_FAN_MODE_AUTO = 0x00
SCHEDULE_FAN_MODE_ON = 0x01

SCHEDULE_DAMPER_CLOSE = 0x01
SCHEDULE_DAMPER_OPEN = 0x00


class OptionMixin(bytearray):
    def _get_opt(self, byte_num):
        return int(_get_bit(self[byte_num], 7))

    def _set_opt(self, byte_num, value):
        self[byte_num] = _set_bit(self[byte_num], 7, bool(value))


class FanMode22Mixin(OptionMixin):

    _offset = 0

    @property
    def weekday_fan_mode_1(self):
        return self._get_opt(1)

    @weekday_fan_mode_1.setter
    def weekday_fan_mode_1(self, value):
        self._set_opt(1, value)

    @property
    def weekday_fan_mode_2(self):
        return self._get_opt(3)

    @weekday_fan_mode_2.setter
    def weekday_fan_mode_2(self, value):
        self._set_opt(3, value)

    @property
    def weekend_fan_mode_1(self):
        return self._get_opt(5 + self._offset)

    @weekend_fan_mode_1.setter
    def weekend_fan_mode_1(self, value):
        self._set_opt(5 + self._offset, value)

    @property
    def weekend_fan_mode_2(self):
        return self._get_opt(7 + self._offset)

    @weekend_fan_mode_2.setter
    def weekend_fan_mode_2(self, value):
        self._set_opt(7 + self._offset, value)


class FanMode24Mixin(FanMode22Mixin):
    _offset = 4

    @property
    def weekday_fan_mode_3(self):
        return self._get_opt(5)

    @weekday_fan_mode_3.setter
    def weekday_fan_mode_3(self, value):
        self._set_opt(5, value)

    @property
    def weekday_fan_mode_4(self):
        return self._get_opt(7)

    @weekday_fan_mode_4.setter
    def weekday_fan_mode_4(self, value):
        self._set_opt(7, value)

    @property
    def weekend_fan_mode_3(self):
        return self._get_opt(13)

    @weekend_fan_mode_3.setter
    def weekend_fan_mode_3(self, value):
        self._set_opt(13, value)

    @property
    def weekend_fan_mode_4(self):
        return self._get_opt(15)

    @weekend_fan_mode_4.setter
    def weekend_fan_mode_4(self, value):
        self._set_opt(15, value)


class FanMode72Mixin(OptionMixin):
    _offset = 0

    @property
    def monday_fan_mode_1(self):
        return self._get_opt(1)

    @monday_fan_mode_1.setter
    def monday_fan_mode_1(self, value):
        self._set_opt(1, value)

    @property
    def monday_fan_mode_2(self):
        return self._get_opt(3)

    @monday_fan_mode_2.setter
    def monday_fan_mode_2(self, value):
        self._set_opt(3, value)

    @property
    def tuesday_fan_mode_1(self):
        return self._get_opt(5 + self._offset)

    @tuesday_fan_mode_1.setter
    def tuesday_fan_mode_1(self, value):
        self._set_opt(5 + self._offset, value)

    @property
    def tuesday_fan_mode_2(self):
        return self._get_opt(7 + self._offset)

    @tuesday_fan_mode_2.setter
    def tuesday_fan_mode_2(self, value):
        self._set_opt(7 + self._offset, value)

    @property
    def wednesday_fan_mode_1(self):
        return self._get_opt(9 + (self._offset * 2))

    @wednesday_fan_mode_1.setter
    def wednesday_fan_mode_1(self, value):
        self._set_opt(9 + (self._offset * 2), value)

    @property
    def wednesday_fan_mode_2(self):
        return self._get_opt(11 + (self._offset * 2))

    @wednesday_fan_mode_2.setter
    def wednesday_fan_mode_2(self, value):
        self._set_opt(11 + (self._offset * 2), value)

    @property
    def thursday_fan_mode_1(self):
        return self._get_opt(13 + (self._offset * 3))

    @thursday_fan_mode_1.setter
    def thursday_fan_mode_1(self, value):
        self._set_opt(13 + (self._offset * 3), value)

    @property
    def thursday_fan_mode_2(self):
        return self._get_opt(15 + (self._offset * 3))

    @thursday_fan_mode_2.setter
    def thursday_fan_mode_2(self, value):
        self._set_opt(15 + (self._offset * 3), value)

    @property
    def friday_fan_mode_1(self):
        return self._get_opt(17 + (self._offset * 4))

    @friday_fan_mode_1.setter
    def friday_fan_mode_1(self, value):
        self._set_opt(17 + (self._offset * 4), value)

    @property
    def friday_fan_mode_2(self):
        return self._get_opt(19 + (self._offset * 4))

    @friday_fan_mode_2.setter
    def friday_fan_mode_2(self, value):
        self._set_opt(19 + (self._offset * 4), value)

    @property
    def saturday_fan_mode_1(self):
        return self._get_opt(21 + (self._offset * 5))

    @saturday_fan_mode_1.setter
    def saturday_fan_mode_1(self, value):
        self._set_opt(21 + (self._offset * 5), value)

    @property
    def saturday_fan_mode_2(self):
        return self._get_opt(23 + (self._offset * 5))

    @saturday_fan_mode_2.setter
    def saturday_fan_mode_2(self, value):
        self._set_opt(23 + (self._offset * 5), value)

    @property
    def sunday_fan_mode_1(self):
        return self._get_opt(25 + (self._offset * 6))

    @sunday_fan_mode_1.setter
    def sunday_fan_mode_1(self, value):
        self._set_opt(25 + (self._offset * 6), value)

    @property
    def sunday_fan_mode_2(self):
        return self._get_opt(27 + (self._offset * 6))

    @sunday_fan_mode_2.setter
    def sunday_fan_mode_2(self, value):
        self._set_opt(27 + (self._offset * 6), value)


class FanMode74Mixin(FanMode72Mixin):
    _offset = 4

    @property
    def monday_fan_mode_3(self):
        return self._get_opt(5)

    @monday_fan_mode_3.setter
    def monday_fan_mode_3(self, value):
        self._set_opt(5, value)

    @property
    def monday_fan_mode_4(self):
        return self._get_opt(7)

    @monday_fan_mode_4.setter
    def monday_fan_mode_4(self, value):
        self._set_opt(7, value)

    @property
    def tuesday_fan_mode_3(self):
        return self._get_opt(13)

    @tuesday_fan_mode_3.setter
    def tuesday_fan_mode_3(self, value):
        self._set_opt(13, value)

    @property
    def tuesday_fan_mode_4(self):
        return self._get_opt(15)

    @tuesday_fan_mode_4.setter
    def tuesday_fan_mode_4(self, value):
        self._set_opt(15, value)

    @property
    def wednesday_fan_mode_3(self):
        return self._get_opt(21)

    @wednesday_fan_mode_3.setter
    def wednesday_fan_mode_3(self, value):
        self._set_opt(21, value)

    @property
    def wednesday_fan_mode_4(self):
        return self._get_opt(23)

    @wednesday_fan_mode_4.setter
    def wednesday_fan_mode_4(self, value):
        self._set_opt(23, value)

    @property
    def thursday_fan_mode_3(self):
        return self._get_opt(29)

    @thursday_fan_mode_3.setter
    def thursday_fan_mode_3(self, value):
        self._set_opt(29, value)

    @property
    def thursday_fan_mode_4(self):
        return self._get_opt(31)

    @thursday_fan_mode_4.setter
    def thursday_fan_mode_4(self, value):
        self._set_opt(31, value)

    @property
    def friday_fan_mode_3(self):
        return self._get_opt(37)

    @friday_fan_mode_3.setter
    def friday_fan_mode_3(self, value):
        self._set_opt(37, value)

    @property
    def friday_fan_mode_4(self):
        return self._get_opt(39)

    @friday_fan_mode_4.setter
    def friday_fan_mode_4(self, value):
        self._set_opt(39, value)

    @property
    def saturday_fan_mode_3(self):
        return self._get_opt(45)

    @saturday_fan_mode_3.setter
    def saturday_fan_mode_3(self, value):
        self._set_opt(45, value)

    @property
    def saturday_fan_mode_4(self):
        return self._get_opt(47)

    @saturday_fan_mode_4.setter
    def saturday_fan_mode_4(self, value):
        self._set_opt(47, value)

    @property
    def sunday_fan_mode_3(self):
        return self._get_opt(53)

    @sunday_fan_mode_3.setter
    def sunday_fan_mode_3(self, value):
        self._set_opt(53, value)

    @property
    def sunday_fan_mode_4(self):
        return self._get_opt(55)

    @sunday_fan_mode_4.setter
    def sunday_fan_mode_4(self, value):
        self._set_opt(55, value)


class DamperMode22Mixin(OptionMixin):

    _offset = 0

    @property
    def weekday_damper_mode_1(self):
        return self._get_opt(1)

    @weekday_damper_mode_1.setter
    def weekday_damper_mode_1(self, value):
        self._set_opt(1, value)

    @property
    def weekday_damper_mode_2(self):
        return self._get_opt(3)

    @weekday_damper_mode_2.setter
    def weekday_damper_mode_2(self, value):
        self._set_opt(3, value)

    @property
    def weekend_damper_mode_1(self):
        return self._get_opt(5 + self._offset)

    @weekend_damper_mode_1.setter
    def weekend_damper_mode_1(self, value):
        self._set_opt(5 + self._offset, value)

    @property
    def weekend_damper_mode_2(self):
        return self._get_opt(7 + self._offset)

    @weekend_damper_mode_2.setter
    def weekend_damper_mode_2(self, value):
        self._set_opt(7 + self._offset, value)


class DamperMode24Mixin(DamperMode22Mixin):
    _offset = 4

    @property
    def weekday_damper_mode_3(self):
        return self._get_opt(5)

    @weekday_damper_mode_3.setter
    def weekday_damper_mode_3(self, value):
        self._set_opt(5, value)

    @property
    def weekday_damper_mode_4(self):
        return self._get_opt(7)

    @weekday_damper_mode_4.setter
    def weekday_damper_mode_4(self, value):
        self._set_opt(7, value)

    @property
    def weekend_damper_mode_3(self):
        return self._get_opt(13)

    @weekend_damper_mode_3.setter
    def weekend_damper_mode_3(self, value):
        self._set_opt(13, value)

    @property
    def weekend_damper_mode_4(self):
        return self._get_opt(15)

    @weekend_damper_mode_4.setter
    def weekend_damper_mode_4(self, value):
        self._set_opt(15, value)


class DamperMode72Mixin(OptionMixin):
    _offset = 0

    @property
    def monday_damper_mode_1(self):
        return self._get_opt(1)

    @monday_damper_mode_1.setter
    def monday_damper_mode_1(self, value):
        self._set_opt(1, value)

    @property
    def monday_damper_mode_2(self):
        return self._get_opt(3)

    @monday_damper_mode_2.setter
    def monday_damper_mode_2(self, value):
        self._set_opt(3, value)

    @property
    def tuesday_damper_mode_1(self):
        return self._get_opt(5 + self._offset)

    @tuesday_damper_mode_1.setter
    def tuesday_damper_mode_1(self, value):
        self._set_opt(5 + self._offset, value)

    @property
    def tuesday_damper_mode_2(self):
        return self._get_opt(7 + self._offset)

    @tuesday_damper_mode_2.setter
    def tuesday_damper_mode_2(self, value):
        self._set_opt(7 + self._offset, value)

    @property
    def wednesday_damper_mode_1(self):
        return self._get_opt(9 + (self._offset * 2))

    @wednesday_damper_mode_1.setter
    def wednesday_damper_mode_1(self, value):
        self._set_opt(9 + (self._offset * 2), value)

    @property
    def wednesday_damper_mode_2(self):
        return self._get_opt(11 + (self._offset * 2))

    @wednesday_damper_mode_2.setter
    def wednesday_damper_mode_2(self, value):
        self._set_opt(11 + (self._offset * 2), value)

    @property
    def thursday_damper_mode_1(self):
        return self._get_opt(13 + (self._offset * 3))

    @thursday_damper_mode_1.setter
    def thursday_damper_mode_1(self, value):
        self._set_opt(13 + (self._offset * 3), value)

    @property
    def thursday_damper_mode_2(self):
        return self._get_opt(15 + (self._offset * 3))

    @thursday_damper_mode_2.setter
    def thursday_damper_mode_2(self, value):
        self._set_opt(15 + (self._offset * 3), value)

    @property
    def friday_damper_mode_1(self):
        return self._get_opt(17 + (self._offset * 4))

    @friday_damper_mode_1.setter
    def friday_damper_mode_1(self, value):
        self._set_opt(17 + (self._offset * 4), value)

    @property
    def friday_damper_mode_2(self):
        return self._get_opt(19 + (self._offset * 4))

    @friday_damper_mode_2.setter
    def friday_damper_mode_2(self, value):
        self._set_opt(19 + (self._offset * 4), value)

    @property
    def saturday_damper_mode_1(self):
        return self._get_opt(21 + (self._offset * 5))

    @saturday_damper_mode_1.setter
    def saturday_damper_mode_1(self, value):
        self._set_opt(21 + (self._offset * 5), value)

    @property
    def saturday_damper_mode_2(self):
        return self._get_opt(23 + (self._offset * 5))

    @saturday_damper_mode_2.setter
    def saturday_damper_mode_2(self, value):
        self._set_opt(23 + (self._offset * 5), value)

    @property
    def sunday_damper_mode_1(self):
        return self._get_opt(25 + (self._offset * 6))

    @sunday_damper_mode_1.setter
    def sunday_damper_mode_1(self, value):
        self._set_opt(25 + (self._offset * 6), value)

    @property
    def sunday_damper_mode_2(self):
        return self._get_opt(27 + (self._offset * 6))

    @sunday_damper_mode_2.setter
    def sunday_damper_mode_2(self, value):
        self._set_opt(27 + (self._offset * 6), value)


class DamperMode74Mixin(DamperMode72Mixin):
    _offset = 4

    @property
    def monday_damper_mode_3(self):
        return self._get_opt(5)

    @monday_damper_mode_3.setter
    def monday_damper_mode_3(self, value):
        self._set_opt(5, value)

    @property
    def monday_damper_mode_4(self):
        return self._get_opt(7)

    @monday_damper_mode_4.setter
    def monday_damper_mode_4(self, value):
        self._set_opt(7, value)

    @property
    def tuesday_damper_mode_3(self):
        return self._get_opt(13)

    @tuesday_damper_mode_3.setter
    def tuesday_damper_mode_3(self, value):
        self._set_opt(13, value)

    @property
    def tuesday_damper_mode_4(self):
        return self._get_opt(15)

    @tuesday_damper_mode_4.setter
    def tuesday_damper_mode_4(self, value):
        self._set_opt(15, value)

    @property
    def wednesday_damper_mode_3(self):
        return self._get_opt(21)

    @wednesday_damper_mode_3.setter
    def wednesday_damper_mode_3(self, value):
        self._set_opt(21, value)

    @property
    def wednesday_damper_mode_4(self):
        return self._get_opt(23)

    @wednesday_damper_mode_4.setter
    def wednesday_damper_mode_4(self, value):
        self._set_opt(23, value)

    @property
    def thursday_damper_mode_3(self):
        return self._get_opt(29)

    @thursday_damper_mode_3.setter
    def thursday_damper_mode_3(self, value):
        self._set_opt(29, value)

    @property
    def thursday_damper_mode_4(self):
        return self._get_opt(31)

    @thursday_damper_mode_4.setter
    def thursday_damper_mode_4(self, value):
        self._set_opt(31, value)

    @property
    def friday_damper_mode_3(self):
        return self._get_opt(37)

    @friday_damper_mode_3.setter
    def friday_damper_mode_3(self, value):
        self._set_opt(37, value)

    @property
    def friday_damper_mode_4(self):
        return self._get_opt(39)

    @friday_damper_mode_4.setter
    def friday_damper_mode_4(self, value):
        self._set_opt(39, value)

    @property
    def saturday_damper_mode_3(self):
        return self._get_opt(45)

    @saturday_damper_mode_3.setter
    def saturday_damper_mode_3(self, value):
        self._set_opt(45, value)

    @property
    def saturday_damper_mode_4(self):
        return self._get_opt(47)

    @saturday_damper_mode_4.setter
    def saturday_damper_mode_4(self, value):
        self._set_opt(47, value)

    @property
    def sunday_damper_mode_3(self):
        return self._get_opt(53)

    @sunday_damper_mode_3.setter
    def sunday_damper_mode_3(self, value):
        self._set_opt(53, value)

    @property
    def sunday_damper_mode_4(self):
        return self._get_opt(55)

    @sunday_damper_mode_4.setter
    def sunday_damper_mode_4(self, value):
        self._set_opt(55, value)


class ScheduleBase(bytearray):
    id = 0

    def _get_time(self, byte_num):
        hour = 0
        minute = 0
        data = self[byte_num]

        for i in range(0, 2):
            minute = _set_bit(minute, i, _get_bit(data, i))

        for i in range(3, 7):
            hour = _set_bit(hour, i, _get_bit(data, i))

        if minute == 1:
            minute = 15
        elif minute == 2:
            minute = 30
        elif minute == 3:
            minute = 45

        return datetime.time(hour=hour, minute=minute)

    def _set_time(self, byte_num, data):
        hour = data.hour
        minute = data.minute

        if minute < 15:
            minute = 0
        elif minute < 30:
            minute = 1
        elif minute < 45:
            minute = 2
        else:
            minute = 3

        for i in range(0, 2):
            self[byte_num] = _set_bit(self[byte_num], i, _get_bit(minute, i))

        for i in range(3, 7):
            self[byte_num] = _set_bit(self[byte_num], i, _get_bit(hour, i))

    def _get_temp(self, byte_num):
        temp = 0
        data = self[byte_num]

        for i in range(0, 7):
            temp = _set_bit(temp, i, _get_bit(data, i))

        return temp

    def _set_temp(self, byte_num, value):
        for i in range(0, 7):
            self[byte_num] = _set_bit(self[byte_num], i, _get_bit(value, i))


class Schedule22(ScheduleBase):
    _offset = 0

    @property
    def weekday_time_1(self):
        return self._get_time(0)

    @weekday_time_1.setter
    def weekday_time_1(self, value):
        self._set_time(0, value)

    @property
    def weekday_temp_1(self):
        return self._get_temp(1)

    @weekday_temp_1.setter
    def weekday_temp_1(self, value):
        self._set_temp(1, value)

    @property
    def weekday_time_2(self):
        return self._get_time(2 + self._offset)

    @weekday_time_2.setter
    def weekday_time_2(self, value):
        self._set_time(2 + self._offset, value)

    @property
    def weekday_temp_2(self):
        return self._get_temp(3 + self._offset)

    @weekday_temp_2.setter
    def weekday_temp_2(self, value):
        self._set_temp(3 + self._offset, value)

    @property
    def weekend_time_1(self):
        return self._get_time(4 + self._offset)

    @weekend_time_1.setter
    def weekend_time_1(self, value):
        self._set_time(4 + self._offset, value)

    @property
    def weekend_temp_1(self):
        return self._get_temp(5 + self._offset)

    @weekend_temp_1.setter
    def weekend_temp_1(self, value):
        self._set_temp(5 + self._offset, value)

    @property
    def weekend_time_2(self):
        return self._get_time(6 + self._offset)

    @weekend_time_2.setter
    def weekend_time_2(self, value):
        self._set_time(6 + self._offset, value)

    @property
    def weekend_temp_2(self):
        return self._get_temp(7 + self._offset)

    @weekend_temp_2.setter
    def weekend_temp_2(self, value):
        self._set_temp(7 + self._offset, value)


class Schedule24(Schedule22):
    _offset = 4

    @property
    def weekday_time_3(self):
        return self._get_time(4)

    @weekday_time_3.setter
    def weekday_time_3(self, value):
        self._set_time(4, value)

    @property
    def weekday_temp_3(self):
        return self._get_temp(5)

    @weekday_temp_3.setter
    def weekday_temp_3(self, value):
        self._set_temp(5, value)

    @property
    def weekday_time_4(self):
        return self._get_time(6)

    @weekday_time_4.setter
    def weekday_time_4(self, value):
        self._set_time(6, value)

    @property
    def weekday_temp_4(self):
        return self._get_temp(7)

    @weekday_temp_4.setter
    def weekday_temp_4(self, value):
        self._set_temp(7, value)
        
    @property
    def weekend_time_3(self):
        return self._get_time(12)

    @weekend_time_3.setter
    def weekend_time_3(self, value):
        self._set_time(12, value)

    @property
    def weekend_temp_3(self):
        return self._get_temp(13)

    @weekend_temp_3.setter
    def weekend_temp_3(self, value):
        self._set_temp(13, value)

    @property
    def weekend_time_4(self):
        return self._get_time(14)

    @weekend_time_4.setter
    def weekend_time_4(self, value):
        self._set_time(14, value)

    @property
    def weekend_temp_4(self):
        return self._get_temp(15)

    @weekend_temp_4.setter
    def weekend_temp_4(self, value):
        self._set_temp(15, value)


class Schedule72(ScheduleBase):
    _offset = 0

    @property
    def monday_temp_1(self):
        return self._get_temp(1)

    @monday_temp_1.setter
    def monday_temp_1(self, value):
        self._set_temp(1, value)

    @property
    def monday_temp_2(self):
        return self._get_temp(3)

    @monday_temp_2.setter
    def monday_temp_2(self, value):
        self._set_temp(3, value)

    @property
    def tuesday_temp_1(self):
        return self._get_temp(5 + self._offset)

    @tuesday_temp_1.setter
    def tuesday_temp_1(self, value):
        self._set_temp(5 + self._offset, value)

    @property
    def tuesday_temp_2(self):
        return self._get_temp(7 + self._offset)

    @tuesday_temp_2.setter
    def tuesday_temp_2(self, value):
        self._set_temp(7 + self._offset, value)

    @property
    def wednesday_temp_1(self):
        return self._get_temp(9 + (self._offset * 2))

    @wednesday_temp_1.setter
    def wednesday_temp_1(self, value):
        self._set_temp(9 + (self._offset * 2), value)

    @property
    def wednesday_temp_2(self):
        return self._get_temp(11 + (self._offset * 2))

    @wednesday_temp_2.setter
    def wednesday_temp_2(self, value):
        self._set_temp(11 + (self._offset * 2), value)

    @property
    def thursday_temp_1(self):
        return self._get_temp(13 + (self._offset * 3))

    @thursday_temp_1.setter
    def thursday_temp_1(self, value):
        self._set_temp(13 + (self._offset * 3), value)

    @property
    def thursday_temp_2(self):
        return self._get_temp(15 + (self._offset * 3))

    @thursday_temp_2.setter
    def thursday_temp_2(self, value):
        self._set_temp(15 + (self._offset * 3), value)

    @property
    def friday_temp_1(self):
        return self._get_temp(17 + (self._offset * 4))

    @friday_temp_1.setter
    def friday_temp_1(self, value):
        self._set_temp(17 + (self._offset * 4), value)

    @property
    def friday_temp_2(self):
        return self._get_temp(19 + (self._offset * 4))

    @friday_temp_2.setter
    def friday_temp_2(self, value):
        self._set_temp(19 + (self._offset * 4), value)

    @property
    def saturday_temp_1(self):
        return self._get_temp(21 + (self._offset * 5))

    @saturday_temp_1.setter
    def saturday_temp_1(self, value):
        self._set_temp(21 + (self._offset * 5), value)

    @property
    def saturday_temp_2(self):
        return self._get_temp(23 + (self._offset * 5))

    @saturday_temp_2.setter
    def saturday_temp_2(self, value):
        self._set_temp(23 + (self._offset * 5), value)

    @property
    def sunday_temp_1(self):
        return self._get_temp(25 + (self._offset * 6))

    @sunday_temp_1.setter
    def sunday_temp_1(self, value):
        self._set_temp(25 + (self._offset * 6), value)

    @property
    def sunday_temp_2(self):
        return self._get_temp(27 + (self._offset * 6))

    @sunday_temp_2.setter
    def sunday_temp_2(self, value):
        self._set_temp(27 + (self._offset * 6), value)
    
    @property
    def monday_time_1(self):
        return self._get_time(1)

    @monday_time_1.setter
    def monday_time_1(self, value):
        self._set_time(1, value)

    @property
    def monday_time_2(self):
        return self._get_time(3)

    @monday_time_2.setter
    def monday_time_2(self, value):
        self._set_time(3, value)

    @property
    def tuesday_time_1(self):
        return self._get_time(5 + self._offset)

    @tuesday_time_1.setter
    def tuesday_time_1(self, value):
        self._set_time(5 + self._offset, value)

    @property
    def tuesday_time_2(self):
        return self._get_time(7 + self._offset)

    @tuesday_time_2.setter
    def tuesday_time_2(self, value):
        self._set_time(7 + self._offset, value)

    @property
    def wednesday_time_1(self):
        return self._get_time(9 + (self._offset * 2))

    @wednesday_time_1.setter
    def wednesday_time_1(self, value):
        self._set_time(9 + (self._offset * 2), value)

    @property
    def wednesday_time_2(self):
        return self._get_time(11 + (self._offset * 2))

    @wednesday_time_2.setter
    def wednesday_time_2(self, value):
        self._set_time(11 + (self._offset * 2), value)

    @property
    def thursday_time_1(self):
        return self._get_time(13 + (self._offset * 3))

    @thursday_time_1.setter
    def thursday_time_1(self, value):
        self._set_time(13 + (self._offset * 3), value)

    @property
    def thursday_time_2(self):
        return self._get_time(15 + (self._offset * 3))

    @thursday_time_2.setter
    def thursday_time_2(self, value):
        self._set_time(15 + (self._offset * 3), value)

    @property
    def friday_time_1(self):
        return self._get_time(17 + (self._offset * 4))

    @friday_time_1.setter
    def friday_time_1(self, value):
        self._set_time(17 + (self._offset * 4), value)

    @property
    def friday_time_2(self):
        return self._get_time(19 + (self._offset * 4))

    @friday_time_2.setter
    def friday_time_2(self, value):
        self._set_time(19 + (self._offset * 4), value)

    @property
    def saturday_time_1(self):
        return self._get_time(21 + (self._offset * 5))

    @saturday_time_1.setter
    def saturday_time_1(self, value):
        self._set_time(21 + (self._offset * 5), value)

    @property
    def saturday_time_2(self):
        return self._get_time(23 + (self._offset * 5))

    @saturday_time_2.setter
    def saturday_time_2(self, value):
        self._set_time(23 + (self._offset * 5), value)

    @property
    def sunday_time_1(self):
        return self._get_time(25 + (self._offset * 6))

    @sunday_time_1.setter
    def sunday_time_1(self, value):
        self._set_time(25 + (self._offset * 6), value)

    @property
    def sunday_time_2(self):
        return self._get_time(27 + (self._offset * 6))

    @sunday_time_2.setter
    def sunday_time_2(self, value):
        self._set_time(27 + (self._offset * 6), value)


class Schedule74(Schedule72):
    _offset = 4
    
    @property
    def monday_time_3(self):
        return self._get_time(5)

    @monday_time_3.setter
    def monday_time_3(self, value):
        self._set_time(5, value)

    @property
    def monday_time_4(self):
        return self._get_time(7)

    @monday_time_4.setter
    def monday_time_4(self, value):
        self._set_time(7, value)

    @property
    def tuesday_time_3(self):
        return self._get_time(13)

    @tuesday_time_3.setter
    def tuesday_time_3(self, value):
        self._set_time(13, value)

    @property
    def tuesday_time_4(self):
        return self._get_time(15)

    @tuesday_time_4.setter
    def tuesday_time_4(self, value):
        self._set_time(15, value)

    @property
    def wednesday_time_3(self):
        return self._get_time(21)

    @wednesday_time_3.setter
    def wednesday_time_3(self, value):
        self._set_time(21, value)

    @property
    def wednesday_time_4(self):
        return self._get_time(23)

    @wednesday_time_4.setter
    def wednesday_time_4(self, value):
        self._set_time(23, value)

    @property
    def thursday_time_3(self):
        return self._get_time(29)

    @thursday_time_3.setter
    def thursday_time_3(self, value):
        self._set_time(29, value)

    @property
    def thursday_time_4(self):
        return self._get_time(31)

    @thursday_time_4.setter
    def thursday_time_4(self, value):
        self._set_time(31, value)

    @property
    def friday_time_3(self):
        return self._get_time(37)

    @friday_time_3.setter
    def friday_time_3(self, value):
        self._set_time(37, value)

    @property
    def friday_time_4(self):
        return self._get_time(39)

    @friday_time_4.setter
    def friday_time_4(self, value):
        self._set_time(39, value)

    @property
    def saturday_time_3(self):
        return self._get_time(45)

    @saturday_time_3.setter
    def saturday_time_3(self, value):
        self._set_time(45, value)

    @property
    def saturday_time_4(self):
        return self._get_time(47)

    @saturday_time_4.setter
    def saturday_time_4(self, value):
        self._set_time(47, value)

    @property
    def sunday_time_3(self):
        return self._get_time(53)

    @sunday_time_3.setter
    def sunday_time_3(self, value):
        self._set_time(53, value)

    @property
    def sunday_time_4(self):
        return self._get_time(55)

    @sunday_time_4.setter
    def sunday_time_4(self, value):
        self._set_time(55, value)

    @property
    def monday_temp_3(self):
        return self._get_temp(5)

    @monday_temp_3.setter
    def monday_temp_3(self, value):
        self._set_temp(5, value)

    @property
    def monday_temp_4(self):
        return self._get_temp(7)

    @monday_temp_4.setter
    def monday_temp_4(self, value):
        self._set_temp(7, value)

    @property
    def tuesday_temp_3(self):
        return self._get_temp(13)

    @tuesday_temp_3.setter
    def tuesday_temp_3(self, value):
        self._set_temp(13, value)

    @property
    def tuesday_temp_4(self):
        return self._get_temp(15)

    @tuesday_temp_4.setter
    def tuesday_temp_4(self, value):
        self._set_temp(15, value)

    @property
    def wednesday_temp_3(self):
        return self._get_temp(21)

    @wednesday_temp_3.setter
    def wednesday_temp_3(self, value):
        self._set_temp(21, value)

    @property
    def wednesday_temp_4(self):
        return self._get_temp(23)

    @wednesday_temp_4.setter
    def wednesday_temp_4(self, value):
        self._set_temp(23, value)

    @property
    def thursday_temp_3(self):
        return self._get_temp(29)

    @thursday_temp_3.setter
    def thursday_temp_3(self, value):
        self._set_temp(29, value)

    @property
    def thursday_temp_4(self):
        return self._get_temp(31)

    @thursday_temp_4.setter
    def thursday_temp_4(self, value):
        self._set_temp(31, value)

    @property
    def friday_temp_3(self):
        return self._get_temp(37)

    @friday_temp_3.setter
    def friday_temp_3(self, value):
        self._set_temp(37, value)

    @property
    def friday_temp_4(self):
        return self._get_temp(39)

    @friday_temp_4.setter
    def friday_temp_4(self, value):
        self._set_temp(39, value)

    @property
    def saturday_temp_3(self):
        return self._get_temp(45)

    @saturday_temp_3.setter
    def saturday_temp_3(self, value):
        self._set_temp(45, value)

    @property
    def saturday_temp_4(self):
        return self._get_temp(47)

    @saturday_temp_4.setter
    def saturday_temp_4(self, value):
        self._set_temp(47, value)

    @property
    def sunday_temp_3(self):
        return self._get_temp(53)

    @sunday_temp_3.setter
    def sunday_temp_3(self, value):
        self._set_temp(53, value)

    @property
    def sunday_temp_4(self):
        return self._get_temp(55)

    @sunday_temp_4.setter
    def sunday_temp_4(self, value):
        self._set_temp(55, value)
