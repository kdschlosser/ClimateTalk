# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

import datetime


class GetIdentificationMDI(bytearray):
    id = None

    @property
    def manufacturer_id(self):
        return self[1] << 8 | self[0]

    @property
    def version(self):
        return self[2] >> 4 & 0xF

    @property
    def revision(self):
        return self[2] & 0xF

    @property
    def _packet_offset(self):
        offset = 4
        for i in range(self[3] + 1):
            offset += len(self._get_string(offset)) + 1
            offset += len(self._get_string(offset)) + 1

        offset += len(self._get_string(offset)) + 1
        return offset

    @property
    def software_versions(self):
        offset = 4
        versions = []
        for i in range(self[3] + 1):
            version = [self._get_string(offset)]
            if version:
                versions += [version]

            offset += len(version) + 1
            offset += len(self._get_string(offset)) + 1

        return versions

    def _get_string(self, offset):
        data = self[offset]
        value = ''
        while data != 0x00:
            value += chr(data)
            offset += 1
            data = self[offset]

        return value

    @property
    def software_revisions(self):
        offset = 4
        revisions = []
        for i in range(self[3] + 1):
            data = self._get_string(offset)
            offset += len(data) + 1
            revision = self._get_string(offset)

            if revision:
                revisions += [revision]

            offset += len(revision) + 1

        return revisions

    @property
    def serial_number(self):
        offset = 4
        for i in range(self[3] + 1):
            offset += len(self._get_string(offset)) + 1
            offset += len(self._get_string(offset)) + 1

        return self._get_string(offset)

    def _get_date(self, offset):
        month = self[offset]
        day = self[offset + 1]
        year = self[offset + 2]

        if 0xFF in (month, day, year):
            return

        return datetime.datetime(month=month, day=day, year=year)

    @property
    def build_date(self):
        offset = self._packet_offset

        return self._get_date(offset + 1)

    @property
    def test_date(self):
        offset = self._packet_offset
        return self._get_date(offset + 4)

    @property
    def install_date(self):
        offset = self._packet_offset
        return self._get_date(offset + 7)

    @property
    def address(self):
        offset = self._packet_offset + 10

        return self._get_string(offset)

    @property
    def zipcode(self):
        offset = self._packet_offset + 10
        offset += len(self.address) + 1

        return self._get_string(offset)

    @property
    def manufacturer(self):
        offset = self._packet_offset + 10
        offset += len(self.address) + 1
        offset += len(self.zipcode) + 1

        return self._get_string(offset)

    @property
    def control_name(self):
        offset = self._packet_offset + 10
        offset += len(self.address) + 1
        offset += len(self.zipcode) + 1
        offset += len(self.manufacturer) + 1

        return self._get_string(offset)

    @property
    def model(self):
        offset = self._packet_offset + 10
        offset += len(self.address) + 1
        offset += len(self.zipcode) + 1
        offset += len(self.manufacturer) + 1
        offset += len(self.control_name) + 1

        return self._get_string(offset)

    @property
    def model_version(self):
        offset = self._packet_offset + 10
        offset += len(self.address) + 1
        offset += len(self.zipcode) + 1
        offset += len(self.manufacturer) + 1
        offset += len(self.control_name) + 1
        offset += len(self.model) + 1

        return self._get_string(offset)

    @property
    def model_revision(self):
        offset = self._packet_offset + 10
        offset += len(self.address) + 1
        offset += len(self.zipcode) + 1
        offset += len(self.manufacturer) + 1
        offset += len(self.control_name) + 1
        offset += len(self.model) + 1
        offset += len(self.model_version) + 1

        return self._get_string(offset)


class SetIdentificationDataMDI(bytearray):
    def _set_string(self, null_count, value):
        offset = 9

        for _ in range(null_count):
            data = self[offset]
            while data != 0x00:
                offset += 1
                data = self[offset]

        offset += 1
        while self[offset] != 0x00:
            self.pop(offset)

        for i in range(len(value) - 1, -1, -1):
            self.insert(offset, value[i])

    def _get_string(self, null_count):
        offset = 9

        for _ in range(null_count):
            data = self[offset]
            while data != 0x00:
                offset += 1
                data = self[offset]

        offset += 1
        data = self[offset]
        value = ''
        while data != 0x00:
            value += chr(data)
            offset += 1
            data = self[offset]

        return value

    def _set_date(self, offset, value):
        self[offset] = value.month
        self[offset + 1] = value.day
        self[offset + 2] = value.year

    def _get_date(self, offset):
        month = self[offset]
        day = self[offset + 1]
        year = self[offset + 2]

        if 0xFF in (month, day, year):
            return

        return datetime.datetime(month=month, day=day, year=year)

    @property
    def build_date(self):
        return self._get_date(0)

    @build_date.setter
    def build_date(self, value):
        self._set_date(0, value)

    @property
    def test_date(self):
        return self._get_date(3)

    @test_date.setter
    def test_date(self, value):
        self._set_date(3, value)

    @property
    def install_date(self):
        return self._get_date(6)

    @install_date.setter
    def install_date(self, value):
        self._set_date(6, value)

    @property
    def address(self):
        return self._get_string(0)

    @address.setter
    def address(self, value):
        self._set_string(0, value)

    @property
    def zipcode(self):
        return self._get_string(1)

    @zipcode.setter
    def zipcode(self, value):
        self._set_string(1, value)

    @property
    def manufacturer(self):
        return self._get_string(2)

    @manufacturer.setter
    def manufacturer(self, value):
        self._set_string(2, value)

    @property
    def control_name(self):
        return self._get_string(3)

    @control_name.setter
    def control_name(self, value):
        self._set_string(3, value)

    @property
    def model(self):
        return self._get_string(4)

    @model.setter
    def model(self, value):
        self._set_string(4, value)

    @property
    def model_version(self):
        return self._get_string(5)

    @model_version.setter
    def model_version(self, value):
        self._set_string(5, value)

    @property
    def model_revision(self):
        return self._get_string(6)

    @model_revision.setter
    def model_revision(self, value):
        self._set_string(6, value)


