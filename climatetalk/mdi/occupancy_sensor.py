# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

import threading
from ..packet import GetSensorDataRequest, GetSensorDataResponse


class OccupancySensorMDI(object):

    def __init__(self, network, address, subnet, mac_address, session_id):
        self.network = network
        self.address = address
        self.subnet = subnet
        self.mac_address = mac_address
        self.session_id = session_id

    def _get_status_mdi(self, byte_num, num_bytes):
        num_bytes += 1

        packet = GetSensorDataRequest()
        packet.destination = self.address
        packet.subnet = self.subnet
        packet.packet_number = 0x00

        event = threading.Event()

        data = bytearray()

        def callback(response):
            data.extend(
                response.payload_data[byte_num:byte_num + num_bytes]
            )
            GetSensorDataResponse.message_type.disconnect(
                self.address,
                self.subnet
            )
            event.set()

        GetSensorDataResponse.message_type.connect(
            self.address,
            self.subnet,
            callback
        )

        self.network.send(packet)
        event.wait()
        return data

    @property
    def critical_fault(self):
        data = self._get_status_mdi(0, 0)
        return data[0]

    @property
    def minor_fault(self):
        data = self._get_status_mdi(1, 0)

        return data[0]

    @property
    def is_occupied(self):
        data = self._get_status_mdi(2, 0)
        return bool(data[0])
