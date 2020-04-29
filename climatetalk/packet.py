# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

import six
from .message_types import *
from . import mac_address
from . import session_id
from .utils import get_bit as _get_bit, set_bit as _set_bit


CT_ISUM1 = 0xAA  # New Fletcher Seed.
CT_ISUM2 = 0x00

ACK = 0x06
NAK = 0x15

SEND_METHOD_NON_ROUTED = 0x00
SEND_METHOD_ROUTED_PRIORITY_CONTROL_COMMAND = 0x01
SEND_METHOD_ROUTED_PRIORITY_NODE_TYPE = 0x02
SEND_METHOD_ROUTED_SOCKET = 0x03


class PacketNumber(int):
    @property
    def data_flow(self):
        return _get_bit(self, 7)

    @data_flow.setter
    def data_flow(self, value):
        _set_bit(self, 7, bool(value))


class PacketMeta(type):

    def __call__(cls, *args, **kwargs):
        if cls != Packet:
            return super(PacketMeta, cls).__call__(*args, **kwargs)

        data = args[0]

        for cl in PACKET_CLASSES:
            # noinspection PyProtectedMember
            if cl.message_type == data[7]:
                break

        else:
            return super(PacketMeta, cls).__call__(*args, **kwargs)

        namespace = dict(
            _packet_number=data[8],
            _payload_length=data[9],
            _payload_data=data[11:-2]
        )
        cl = type('DynamicPacket', (cl,), namespace)
        instance = cl(*args, **kwargs)
        return instance


# Packet breakdown

# byte num
# Destination Address byte 0
# Source Address      byte 1
# Subnet              byte 2
# Send Method         byte 3
# Send Parameter 1    byte 4
# Send Parameter 2    byte 5
# Source Node Type    byte 6
# Message Type        byte 7
# Packet Number       byte 8
# Packet Length       byte 9
# Packet Payload      bytes 10-250
# Message Checksum 1  byte -2
# Message Checksum 2  byte -1


@six.add_metaclass(PacketMeta)
class Packet(bytearray):
    message_type = 0x00
    _packet_number = PacketNumber(0x00)
    _payload_length = 0x00
    _payload_data = bytearray()

    def __init__(self, *args, **kwargs):
        try:
            bytearray.__init__(self, *args, **kwargs)
        except TypeError:
            bytearray.__init__(self)

        if not len(self):

            self.extend(bytearray(0x00 for _ in range(self._payload_length + 12)))
            self[7] = self.message_type
            self[8] = self._packet_number
            self[9] = self._payload_length

            for i, item in enumerate(self._payload_data):
                self[i + 10] = item

    @property
    def destination(self):
        return self[0]

    @destination.setter
    def destination(self, value):
        if len(self):
            self[0] = value
        else:
            self.append(value)

    @property
    def source(self):
        return self[1]

    @source.setter
    def source(self, value):
        if len(self) > 1:
            self[1] = value
        else:
            self.append(value)

    @property
    def subnet(self):
        return self[2]

    @subnet.setter
    def subnet(self, value):
        if len(self) > 2:
            self[2] = value
        else:
            self.append(value)

    @property
    def send_method(self):
        return self[3]

    @send_method.setter
    def send_method(self, value):
        if len(self) > 3:
            self[3] = value
        else:
            self.append(value)

    @property
    def send_parameters(self):
        return self[4] << 8 | self[5]

    @send_parameters.setter
    def send_parameters(self, value):
        byte1 = value >> 8 & 0xFF
        byte2 = value & 0xFF

        if len(self) > 5:
            self[4] = byte1
            self[5] = byte2
        else:
            self.append(byte1)
            self.append(byte2)

    @property
    def source_node_type(self):
        return self[6]

    @source_node_type.setter
    def source_node_type(self, value):
        if len(self) > 6:
            self[6] = value
        else:
            self.append(value)

    @property
    def message_type(self):
        return self[7]  # byte 7

    @message_type.setter
    def message_type(self, value):
        if len(self) > 7:
            self[7] = value
        else:
            self.append(value)

    @property
    def packet_number(self):
        return self[8]  # byte 8

    @packet_number.setter
    def packet_number(self, value):
        if len(self) > 8:
            self[8] = value
        else:
            self.append(value)

    @property
    def packet_length(self):
        return self[9]  # byte 9

    @packet_length.setter
    def packet_length(self, value):
        if len(self) > 9:
            self[9] = value
        else:
            self.append(value)

    @property
    def packet_payload(self):
        return self[10:-2]

    @packet_payload.setter
    def packet_payload(self, value):
        if len(self) > 10:
            del self[10:]
            self.extend(bytearray(value))
        else:
            self.extend(bytearray(value))

        self.append(CT_ISUM1)
        self.append(CT_ISUM2)

    def calc_checksum(self):
        sum1 = 0
        sum2 = 0

        for i in range(len(self)[:-2]):
            sum1 += self[i]
            sum2 += sum1

        check1 = (sum1 + sum2) % 0xFF
        check2 = (sum1 + check1) % 0xFF

        if self[-2] == CT_ISUM1:
            self[len(self) - 2] = check1
            self[len(self) - 1] = check2

        return check1, check2

    @property
    def is_valid(self):
        check1, check2 = self.cacl_checksum()
        data1, data2 = self[-2:]

        return check1 == data1 and check2 == data2


class GetConfigurationRequest(Packet):
    message_type = GET_CONFIGURATION
    _payload_length = 0
    _payload_data = bytearray()


class GetConfigurationResponse(Packet):
    message_type = GET_CONFIGURATION_RESPONSE

    @property
    def db_id_tag(self):
        return self[10]

    @db_id_tag.setter
    def db_id_tag(self, value):
        while len(self) < 11:
            self.append(0x00)

        self[10] = value

    @property
    def db_length(self):
        return self[11]

    @db_length.setter
    def db_length(self, value):
        while len(self) < 12:
            self.append(0x00)

        self[11] = value

    @property
    def payload_data(self):
        return self[12:-2]

    @payload_data.setter
    def payload_data(self, value):

        while len(self) < 11 + len(value):
            self.append(0x00)

        for i, item in enumerate(value):
            self[12 + i] = item


class GetStatusRequest(Packet):
    message_type = GET_STATUS
    _payload_length = 0
    _payload_data = bytearray()


class GetStatusResponse(Packet):
    message_type = GET_STATUS_RESPONSE

    @property
    def payload_data(self):
        return self[11:-2]

    @payload_data.setter
    def payload_data(self, value):

        while len(self) < 10 + len(value):
            self.append(0x00)

        for i, item in enumerate(value):
            self[10 + i] = item


class SetControlCommandRequest(Packet):
    message_type = SET_CONTROL_COMMAND

    @property
    def payload_command_code(self):
        return self[10] | self[11] << 8
    
    @payload_command_code.setter
    def payload_command_code(self, value):
        while len(self) < 12:
            self.append(0x00)

        self[10] = value & 0xFF
        self[11] = value >> 8 & 0xFF


class SetControlCommandResponse(SetControlCommandRequest):
    message_type = SET_CONTROL_COMMAND_RESPONSE


class SetDisplayMessageRequest(Packet):
    message_type = SET_DISPLAY_MESSAGE

    @property
    def payload_node_type(self):
        return self[10]

    @payload_node_type.setter
    def payload_node_type(self, value):
        while len(self) < 11:
            self.append(0x00)
        self[10] = value

    @property
    def payload_message_length(self):
        # 0-30
        return self[11]

    @payload_message_length.setter
    def payload_message_length(self, value):
        while len(self) < 12:
            self.append(0x00)

        self[11] = value

    @property
    def payload_message(self):
        return self[14:-2]

    @payload_message.setter
    def payload_message(self, value):
        while len(self) < len(value) + 12:
            self.append(0x00)

        for i, item in enumerate(value):
            self[12 + i] = item

        self.payload_message_length = len(value)


class SetDisplayMessageResponse(Packet):
    message_type = SET_DISPLAY_MESSAGE_RESPONSE
    _payload_length = 2
    _payload_data = bytearray(b'\xAC\x06')

    @property
    def result(self):
        return self[12]

    @result.setter
    def result(self, value):
        # ACK or NAK
        self[12] = value


class SetDisgnosticsRequest(Packet):
    message_type = SET_DISGNOSTICS

    @property
    def payload_node_type(self):
        return self[10]

    @payload_node_type.setter
    def payload_node_type(self, value):
        while len(self) < 11:
            self.append(0x00)
        self[10] = value

    @property
    def payload_major_code(self):
        return self[11]

    @payload_major_code.setter
    def payload_major_code(self, value):
        while len(self) < 12:
            self.append(0x00)
        self[11] = value

    @property
    def payload_minor_code(self):
        return self[12]

    @payload_minor_code.setter
    def payload_minor_code(self, value):
        while len(self) < 13:
            self.append(0x00)
        self[12] = value

    @property
    def payload_message_length(self):
        # 0-15
        return self[13]

    @payload_message_length.setter
    def payload_message_length(self, value):
        while len(self) < 14:
            self.append(0x00)

        self[13] = value

    @property
    def payload_fault_message(self):
        return self[14:-2]

    @payload_fault_message.setter
    def payload_fault_message(self, value):
        while len(self) < len(value) + 14:
            self.append(0x00)

        for i, item in enumerate(value):
            self[14 + i] = item

        self.payload_message_length = len(value)


class SetDisgnosticsResponse(Packet):
    message_type = SET_DISGNOSTICS_RESPONSE
    _payload_length = 2
    _payload_data = bytearray(b'\xAC\x06')

    @property
    def result(self):
        return self[12]

    @result.setter
    def result(self, value):
        # ACK or NAK
        self[12] = value


class GetDiagnosticsRequest(Packet):
    message_type = GET_DIAGNOSTICS
    _payload_length = 2
    _payload_data = bytearray(b'\x00\x00')

    @property
    def payload_fault_type(self):
        return self[10]

    @payload_fault_type.setter
    def payload_fault_type(self, value):
        self[10] = value

    @property
    def payload_fault_index(self):
        return self[11]

    @payload_fault_index.setter
    def payload_fault_index(self, value):
        self[11] = value


class GetDiagnosticsResponse(Packet):
    message_type = GET_DIAGNOSTICS_RESPONSE

    def __iter__(self):
        fault = bytearray()
        for char in self[11:-2]:
            if char == 0x00:
                yield fault
                fault = bytearray()
            else:
                fault.append(char)


class GetSensorDataRequest(Packet):
    message_type = GET_SENSOR_DATA
    _payload_length = 0
    _payload_data = bytearray()


class GetSensorDataResponse(Packet):
    message_type = GET_SENSOR_DATA_RESPONSE

    class SensorData(object):

        def __init__(self, id, data):
            self.id = id
            self.data = data

    def __iter__(self):
        data = self.payload_data
        while data:
            db_id = data[0]
            db_len = data[1]
            db_data = data[2:db_len]
            data = data[:db_len + 2]
            yield self.SensorData(db_id, db_data)

    @property
    def payload_data(self):
        return self[11:-2]

    @payload_data.setter
    def payload_data(self, value):
        while len(self) < 11 + len(value):
            self.append(0x00)

        for i, item in enumerate(value):
            self[10 + i] = item


class SetIdentificationDataRequest(Packet):
    message_type = SET_IDENTIFICATION

    @property
    def payload_data(self):
        return self[11:-2]

    @payload_data.setter
    def payload_data(self, value):
        while len(self) < 11 + len(value):
            self.append(0x00)

        for i, item in enumerate(value):
            self[10 + i] = item


class SetIdentificationDataResponse(Packet):
    message_type = SET_IDENTIFICATION_RESPONSE
    _payload_length = 2
    _payload_data = bytearray(b'\xAC\x06')

    @property
    def payload_result(self):
        # ACK or NAK
        return self[11]

    @payload_result.setter
    def payload_result(self, value):
        self[11] = value


class GetIdentificationDataRequest(Packet):
    message_type = GET_IDENTIFICATION
    _payload_length = 0
    _payload_data = bytearray()


class GetIdentificationDataResponse(Packet):
    message_type = GET_IDENTIFICATION_RESPONSE

    @property
    def payload_data(self):
        return self[11:-2]

    @payload_data.setter
    def payload_data(self, value):
        while len(self) < 11 + len(value):
            self.append(0x00)

        for i, item in enumerate(value):
            self[10 + i] = item


class SetApplicationSharedDataToNetworkRequest(Packet):
    message_type = SET_APPLICATION_SHARED_DATA_TO_NETWORK

    @property
    def payload_sector_node_type(self):
        return self[10]

    @payload_sector_node_type.setter
    def payload_sector_node_type(self, value):
        while len(self) < 11:
            self.append(0x00)

        self[10] = value

    @property
    def payload_shared_data_length(self):
        return self[11]

    @payload_shared_data_length.setter
    def payload_shared_data_length(self, value):
        while len(self) < 12:
            self.append(0x00)

        self[11] = value

    @property
    def payload_control_id(self):
        return self[12] >> 8 | self[13]

    @payload_control_id.setter
    def payload_control_id(self, value):
        while len(self) < 14:
            self.append(0x00)

        self[12] = value << 8 & 0xFF
        self[13] = value & 0xFF

    @property
    def payload_manufacturer_id(self):
        return self[14] >> 8 | self[15]

    @payload_manufacturer_id.setter
    def payload_manufacturer_id(self, value):
        while len(self) < 16:
            self.append(0x00)

        self[14] = value << 8 & 0xFF
        self[15] = value & 0xFF

    @property
    def payload_app_node_type(self):
        return self[16]

    @payload_app_node_type.setter
    def payload_app_node_type(self, value):
        while len(self) < 17:
            self.append(0x00)

        self[16] = value

    @property
    def payload_application_data(self):
        return self[17:-2]

    @payload_application_data.setter
    def payload_application_data(self, value):
        while len(self) < 18 + len(value):
            self.append(0x00)

        for i, item in enumerate(value):
            self[17 + i] = item

        self.payload_shared_data_length = len(value)


class SetApplicationSharedDataToNetworkResponse(SetApplicationSharedDataToNetworkRequest):
    message_type = SET_APPLICATION_SHARED_DATA_TO_NETWORK_RESPONSE


class GetApplicationSharedDataToNetworkRequest(Packet):
    message_type = GET_APPLICATION_SHARED_DATA_TO_NETWORK
    _payload_length = 1
    _payload_data = bytearray(b'\x00')

    @property
    def payload_sector_node_type(self):
        return self[10]

    @payload_sector_node_type.setter
    def payload_sector_node_type(self, value):
        self[10] = value


class GetApplicationSharedDataToNetworkResponse(GetApplicationSharedDataToNetworkRequest):
    message_type = GET_APPLICATION_SHARED_DATA_TO_NETWORK_RESPONSE

    @property
    def payload_shared_data_length(self):
        return self[11]

    @payload_shared_data_length.setter
    def payload_shared_data_length(self, value):
        while len(self) < 12:
            self.append(0x00)

        self[11] = value

    @property
    def payload_control_id(self):
        return self[12] >> 8 | self[13]

    @payload_control_id.setter
    def payload_control_id(self, value):
        while len(self) < 14:
            self.append(0x00)

        self[12] = value << 8 & 0xFF
        self[13] = value & 0xFF

    @property
    def payload_manufacturer_id(self):
        return self[14] >> 8 | self[15]

    @payload_manufacturer_id.setter
    def payload_manufacturer_id(self, value):
        while len(self) < 16:
            self.append(0x00)

        self[14] = value << 8 & 0xFF
        self[15] = value & 0xFF

    @property
    def payload_app_node_type(self):
        return self[16]

    @payload_app_node_type.setter
    def payload_app_node_type(self, value):
        while len(self) < 17:
            self.append(0x00)

        self[16] = value

    @property
    def payload_application_data(self):
        return self[17:-2]

    @payload_application_data.setter
    def payload_application_data(self, value):
        while len(self) < 18 + len(value):
            self.append(0x00)

        for i, item in enumerate(value):
            self[17 + i] = item

        self.payload_shared_data_length = len(value)


class SetManufacturerDeviceDataRequest(Packet):
    message_type = SET_MANUFACTURER_DEVICE_DATA

    @property
    def payload_manufacturer_device_data(self):
        return self[11:-2]

    @payload_manufacturer_device_data.setter
    def payload_manufacturer_device_data(self, value):
        while len(self) < 11 + len(value):
            self.append(0x00)

        for i, item in enumerate(value):
            self[10 + i] = item


class SetManufacturerDeviceDataResponse(SetManufacturerDeviceDataRequest):
    message_type = SET_MANUFACTURER_DEVICE_DATA_RESPONSE


class GetManufacturerDeviceDataRequest(Packet):
    message_type = GET_MANUFACTURER_DEVICE_DATA
    _payload_length = 0
    _payload_data = bytearray()


class GetManufacturerDeviceDataResponse(Packet):
    message_type = GET_MANUFACTURER_DEVICE_DATA_RESPONSE

    @property
    def payload_manufacturer_device_data(self):
        return self[11:-2]

    @payload_manufacturer_device_data.setter
    def payload_manufacturer_device_data(self, value):
        while len(self) < 11 + len(value):
            self.append(0x00)

        for i, item in enumerate(value):
            self[10 + i] = item


class SetNetworkNodeListRequest(Packet):
    message_type = SET_NETWORK_NODE_LIST

    @property
    def payload_coordinator_type(self):
        return self[10]

    @payload_coordinator_type.setter
    def payload_coordinator_type(self, value):
        while len(self) < 11:
            self.append(0x00)

        self[10] = value

    def get_node_type(self, index):
        return self[10 + index]

    def set_node_type(self, index, value):
        while len(self) < 10 + index:
            self.append(0x00)

        self[10 + index] = value


class SetNetworkNodeListResponse(SetNetworkNodeListRequest):
    message_type = SET_NETWORK_NODE_LIST_RESPONSE


# byte num
# Destination Address byte 0
# Source Address      byte 1
# Subnet              byte 2
# Send Method         byte 3
# Send Parameter 1    byte 4
# Send Parameter 2    byte 5
# Source Node Type    byte 6
# Message Type        byte 7
# Packet Number       byte 8
# Packet Length       byte 9
# Packet Payload      bytes 10-250
# Message Checksum 1  byte -2
# Message Checksum 2  byte -1


DMA_READ_MDI_TYPE_CONFIGURATION = 0x01
DMA_READ_MDI_TYPE_STATUS = 0x02
DMA_READ_MDI_TYPE_SENSOR = 0x03
DMA_READ_MDI_TYPE_IDENTIFICATION = 0x0E


class DirectMemoryAccessReadRequest(Packet):
    """
    MDI values (byte 1 of the payload)
    Configuration: 0x01
    Status: 0x02
    Sensor: 0x07
    Identification 0x0E

    example motor command

    Destination Address             byte 0    [25]
    Source Address                  byte 1    [3]
    Subnet                          byte 2    [2]
    Send Method                     byte 3    [0]
    Send Parameter 1                byte 4    [0]
    Send Parameter 2                byte 5    [0]
    Source Node Type                byte 6    [0x01] thermostat
    Message Type                    byte 7    [0x1D] DIRECT_MEMORY_ACCESS_READ
    Packet Number                   byte 8    [0x00]
    Packet Length                   byte 9    [4]
    Packet Payload MDI              byte 10   [0x02] Configuration
    Packet Payload null             byte 11   [0x00] Always 0x00
    Packet Payload MDI start byte   byte 12   [30]
    Packet Payload byte count       byte 13   [2]
    Message Checksum 1              byte 14
    Message Checksum 2              byte 15
    """
    message_type = DIRECT_MEMORY_ACCESS_READ
    _payload_length = 4
    _payload_data = bytearray(b'\x00' * 4)

    @property
    def payload_mdi(self):
        return self[10]

    @payload_mdi.setter
    def payload_mdi(self, value):
        self[10] = value

    @property
    def payload_packet_number(self):
        # should always be 0x00
        return self[11]

    @payload_packet_number.setter
    def payload_packet_number(self, value):
        self[11] = value

    @property
    def payload_start_byte(self):
        return self[12]

    @payload_start_byte.setter
    def payload_start_byte(self, value):
        self[12] = value

    @property
    def payload_byte_count(self):
        return self[13]

    @payload_byte_count.setter
    def payload_byte_count(self, value):
        self[13] = value


class DirectMemoryAccessReadResponse(Packet):
    message_type = DIRECT_MEMORY_ACCESS_READ_RESPONSE

    @property
    def payload_data(self):
        return self[11:-2]

    @payload_data.setter
    def payload_data(self, value):
        while len(self) < 11 + len(value):
            self.append(0x00)

        for i, item in enumerate(value):
            self[i + 10] = item


class DirectMemoryAccessReadResponseMotor(DirectMemoryAccessReadResponse):
    message_type = DIRECT_MEMORY_ACCESS_READ_RESPONSE_MOTOR

    @property
    def payload_data(self):
        return self[13:-2]


class SetManufacturerGenericDataRequest(Packet):
    message_type = SET_MANUFACTURER_GENERIC_DATA

    @property
    def payload_manufacturer_id(self):
        return self[10] >> 8 | self[11]

    @payload_manufacturer_id.setter
    def payload_manufacturer_id(self, value):
        while len(self) < 13:
            self.append(0x00)

        self[10] = value << 8 & 0xFF
        self[11] = value & 0xFF

    @property
    def payload_data(self):
        return self[13:-2]

    @payload_data.setter
    def payload_data(self, value):
        while len(self) < len(value) + 13:
            self.append(0x00)

        for i, item in enumerate(value):
            self[i + 12] = item


class SetManufacturerGenericDataResponse(SetManufacturerGenericDataRequest):
    message_type = SET_MANUFACTURER_GENERIC_DATA_RESPONSE


class GetManufacturerGenericDataRequest(Packet):
    message_type = GET_MANUFACTURER_GENERIC_DATA

    @property
    def payload_manufacturer_id(self):
        return self[10] >> 8 | self[11]

    @payload_manufacturer_id.setter
    def payload_manufacturer_id(self, value):
        while len(self) < 13:
            self.append(0x00)

        self[10] = value << 8 & 0xFF
        self[11] = value & 0xFF

    @property
    def payload_data(self):
        return self[13:-2]

    @payload_data.setter
    def payload_data(self, value):
        while len(self) < len(value) + 13:
            self.append(0x00)

        for i, item in enumerate(value):
            self[i + 12] = item


class GetManufacturerGenericDataResponse(GetManufacturerGenericDataRequest):
    message_type = GET_MANUFACTURER_GENERIC_DATA_RESPONSE


class GetManufacturerGenericDataResponseMotor(GetManufacturerGenericDataRequest):
    message_type = GET_MANUFACTURER_GENERIC_DATA_RESPONSE_MOTOR


class GetUserMenuRequest(Packet):
    message_type = GET_USER_MENU
    # payload_len = 6 + n
    # bytes 13 and 14 = 0x00

    @property
    def payload_menu_file(self):
        # should always be 0x01
        return self[10]

    @payload_menu_file.setter
    def payload_menu_file(self, value):
        while len(self) < 11:
            self.append(0x00)

        self[10] = value

    @property
    def payload_main_menu(self):
        # 0x00 - 0x0A
        return self[11]

    @payload_main_menu.setter
    def payload_main_menu(self, value):
        while len(self) < 12:
            self.append(0x00)

        self[11] = value

    @property
    def payload_sub_level(self):
        # 0x00 - 0x0A
        return self[12]

    @payload_sub_level.setter
    def payload_sub_level(self, value):
        while len(self) < 13:
            self.append(0x00)

        self[12] = value

    @property
    def payload_maximum_return_size(self):
        return self[15]

    @payload_maximum_return_size.setter
    def payload_maximum_return_size(self, value):
        while len(self) < 16:
            self.append(0x00)
        self[15] = value


class GetUserMenuResponse(GetUserMenuRequest):
    message_type = GET_USER_MENU_RESPONSE

    @property
    def payload_menu_data(self):
        return self[16:self.payload_maximum_return_size]

    @payload_menu_data.setter
    def payload_menu_data(self, value):
        while len(self) < len(value) + 17:
            self.append(0x00)

        for i, item in enumerate(value):
            self[i + 16] = item

        self.payload_maximum_return_size = len(value)


class SetUserMenuRequest(Packet):
    message_type = SET_USER_MENU
    _payload_length = 7
    _payload_data = bytearray(b'\x00' * 7)
    _payload_data[3] = 0x55
    _payload_data[6] = 0xAA

    @property
    def payload_menu_file(self):
        return self[10]

    @payload_menu_file.setter
    def payload_menu_file(self, value):
        self[10] = value

    @property
    def payload_main_menu(self):
        return self[11]

    @payload_main_menu.setter
    def payload_main_menu(self, value):
        self[11] = value

    @property
    def payload_sub_level(self):
        return self[12]

    @payload_sub_level.setter
    def payload_sub_level(self, value):
        self[12] = value

    @property
    def payload_file_security_code_1(self):
        return self[13]

    @payload_file_security_code_1.setter
    def payload_file_security_code_1(self, value):
        self[13] = value

    @property
    def payload_update_value(self):
        return self[14] >> 8 | self[15]

    @payload_update_value.setter
    def payload_update_value(self, value):
        self[14] = value << 8 & 0xFF
        self[15] = value & 0xFF

    @property
    def payload_file_security_code_2(self):
        return self[16]

    @payload_file_security_code_2.setter
    def payload_file_security_code_2(self, value):
        self[16] = value


class SetUserMenuResponse(SetUserMenuRequest):
    message_type = SET_USER_MENU_RESPONSE
    _payload_length = 8
    _payload_data = bytearray(b'\x00' * 8)
    _payload_data[3] = 0x55
    _payload_data[6] = 0xAA

    @property
    def payload_result(self):
        # ACK or NAK
        return self[17]

    @payload_result.setter
    def payload_result(self, value):
        self[17] = value


class SetFactorySharedDataToApplicationRequest(Packet):
    message_type = SET_FACTORY_SHARED_DATA_TO_APPLICATION

    @property
    def payload_shared_data_len(self):
        # 6 to 200
        return self[10]

    @payload_shared_data_len.setter
    def payload_shared_data_len(self, value):
        while len(self) != 11:
            self.append(0x00)

        self[10] = value

    @property
    def payload_control_id(self):
        return self[11] >> 8 | self[12]

    @payload_control_id.setter
    def payload_control_id(self, value):
        while len(self) != 13:
            self.append(0x00)

        self[11] = value << 8 & 0xFF
        self[12] = value & 0xFF

    @property
    def payload_manufacturer_id(self):
        return self[13] >> 8 | self[14]

    @payload_manufacturer_id.setter
    def payload_manufacturer_id(self, value):
        while len(self) != 15:
            self.append(0x00)

        self[13] = value << 8 & 0xFF
        self[14] = value & 0xFF

    @property
    def payload_app_node_type(self):
        return self[15]

    @payload_app_node_type.setter
    def payload_app_node_type(self, value):
        while len(self) != 16:
            self.append(0x00)

        self[15] = value

    @property
    def payload_application_data(self):
        return self[16:self.payload_shared_data_len - 6]

    @payload_application_data.setter
    def payload_application_data(self, value):
        while len(self) != len(value) + 16:
            self.append(0x00)

        for i, item in enumerate(value):
            self[i + 16] = item

        self.payload_shared_data_len = len(value) + 6


class SetFactorySharedDataToApplicationResponse(SetFactorySharedDataToApplicationRequest):
    message_type = SET_FACTORY_SHARED_DATA_TO_APPLICATION_RESPONSE


class GetSharedDataFromApplicationRequest(Packet):
    message_type = GET_SHARED_DATA_FROM_APPLICATION
    _payload_length = 1
    _payload_data = bytearray(b'\x00')


class GetSharedDataFromApplicationResponse(Packet):
    message_type = GET_SHARED_DATA_FROM_APPLICATION_RESPONSE

    @property
    def payload_app_node_type_1(self):
        return self[10]

    @payload_app_node_type_1.setter
    def payload_app_node_type_1(self, value):
        while len(self) != 11:
            self.append(0x00)

        self[10] = value

    @property
    def payload_shared_data_len(self):
        # 6 to 200
        return self[11]

    @payload_shared_data_len.setter
    def payload_shared_data_len(self, value):
        while len(self) != 12:
            self.append(0x00)

        self[11] = value

    @property
    def payload_control_id(self):
        return self[12] >> 8 | self[13]

    @payload_control_id.setter
    def payload_control_id(self, value):
        while len(self) != 14:
            self.append(0x00)

        self[12] = value << 8 & 0xFF
        self[13] = value & 0xFF

    @property
    def payload_manufacturer_id(self):
        return self[14] >> 8 | self[15]

    @payload_manufacturer_id.setter
    def payload_manufacturer_id(self, value):
        while len(self) != 16:
            self.append(0x00)

        self[14] = value << 8 & 0xFF
        self[15] = value & 0xFF

    @property
    def payload_app_node_type_2(self):
        return self[16]

    @payload_app_node_type_2.setter
    def payload_app_node_type_2(self, value):
        while len(self) != 17:
            self.append(0x00)

        self[16] = value

    @property
    def payload_application_data(self):
        return self[17:self.payload_shared_data_len - 6]

    @payload_application_data.setter
    def payload_application_data(self, value):
        while len(self) != len(value) + 17:
            self.append(0x00)

        for i, item in enumerate(value):
            self[i + 17] = item

        self.payload_shared_data_len = len(value) + 6


class SetEchoRequest(Packet):
    message_type = SET_ECHO_DATA


class SetEchoResponse(Packet):
    message_type = SET_ECHO_DATA_RESPONSE


class RequestToReceiveRequest(Packet):
    message_type = REQUEST_TO_RECEIVE
    _payload_length = 17
    _payload_data = bytearray(b'\x00' * 17)

    @property
    def payload_r2r_code(self):
        return self[10]

    @payload_r2r_code.setter
    def payload_r2r_code(self, value):
        self[10] = value

    @property
    def payload_mac_address(self):
        return mac_address.MACAddress(self[11:19])

    @payload_mac_address.setter
    def payload_mac_address(self, value):
        mac = mac_address.MACAddress(value)
        for i, item in enumerate(mac):
            self[i + 11] = item

    @property
    def payload_session_id(self):
        return session_id.SessionId(self[19:27])

    @payload_session_id.setter
    def payload_session_id(self, value):
        mac = session_id.SessionId(value)
        for i, item in enumerate(mac):
            self[i + 19] = item


class RequestToReceiveResponse(RequestToReceiveRequest):
    message_type = REQUEST_TO_RECEIVE_RESPONSE
    _payload_length = 17
    _payload_data = bytearray(b'\x00' * 17)
    _payload_data[10] = 0x06


class NetworkStateRequest(Packet):
    message_type = NETWORK_STATE_REQUEST
    _payload_length = 1
    _payload_data = bytearray(b'\x00')


class NetworkStateResponse(Packet):
    message_type = NETWORK_STATE_REQUEST_RESPONSE

    @property
    def payload_coord_virtual_node_type(self):
        return self[10]

    @payload_coord_virtual_node_type.setter
    def payload_coord_virtual_node_type(self, value):
        self[10] = value

    def get_node_type(self, index):
        return self[11:][index]

    def set_node_type(self, index, value):
        index += 11

        while index > len(self) - 1:
            self.append(0x00)

        self[index + 11] = value


class AddressConfirmationRequest(Packet):
    message_type = ADDRESS_CONFIRMATION

    @property
    def payload_coord_virtual_node_type(self):
        return self[10]

    @payload_coord_virtual_node_type.setter
    def payload_coord_virtual_node_type(self, value):
        self[10] = value

    def get_node_type(self, index):
        return self[11:][index]

    def set_node_type(self, index, value):
        index += 11

        while index > len(self) - 1:
            self.append(0x00)

        self[index + 11] = value


class AddressConfirmationResponse(Packet):
    message_type = ADDRESS_CONFIRMATION_RESPONSE

    @property
    def payload_coord_virtual_node_type(self):
        return self[10]

    @payload_coord_virtual_node_type.setter
    def payload_coord_virtual_node_type(self, value):
        self[10] = value

    def get_node_type(self, index):
        return self[11:][index]

    def set_node_type(self, index, value):
        index += 11

        while index > len(self) - 1:
            self.append(0x00)

        self[index + 11] = value


class TokenOffer(Packet):
    message_type = TOKEN_OFFER
    _payload_length = 1
    _payload_data = bytearray(b'\x00')

    @property
    def payload_node_type_filter(self):
        return self[10]

    @payload_node_type_filter.setter
    def payload_node_type_filter(self, value):
        self[10] = value


class TokenOfferResponse(Packet):
    message_type = TOKEN_OFFER_RESPONSE
    _payload_length = 18
    _payload_data = bytearray(b'\x00' * 18)

    @property
    def payload_address(self):
        return self[10]

    @payload_address.setter
    def payload_address(self, value):
        self[10] = value

    @property
    def payload_subnet(self):
        return self[11]

    @payload_subnet.setter
    def payload_subnet(self, value):
        self[11] = value

    @property
    def payload_mac_address(self):
        return mac_address.MACAddress(self[12:20])

    @payload_mac_address.setter
    def payload_mac_address(self, value):
        mac = mac_address.MACAddress(value)
        for i, item in enumerate(mac):
            self[i + 12] = item

    @property
    def payload_session_id(self):
        return session_id.SessionId(self[20:28])

    @payload_session_id.setter
    def payload_session_id(self, value):
        mac = session_id.SessionId(value)
        for i, item in enumerate(mac):
            self[i + 20] = item


class VersionAnnouncement(Packet):
    # Broadcast
    message_type = VERSION_ANNOUNCEMENT
    _payload_length = 5
    _payload_data = bytearray(b'\x00' * 5)

    @property
    def payload_ct_485_version(self):
        return self[10] << 8 | self[11]

    @payload_ct_485_version.setter
    def payload_ct_485_version(self, value):
        self[10] = value >> 8 & 0xFF
        self[11] = value & 0xFF

    @property
    def payload_ct_485_revision(self):
        return self[12] << 8 | self[13]

    @payload_ct_485_revision.setter
    def payload_ct_485_revision(self, value):
        self[12] = value >> 8 & 0xFF
        self[13] = value & 0xFF

    @property
    def payload_ct_485_ffd(self):
        return self[14]

    @payload_ct_485_ffd.setter
    def payload_ct_485_ffd(self, value):
        self[14] = value


class NodeDiscoveryRequest(Packet):
    # AutoNet
    # Broadcast
    message_type = NODE_DISCOVERY
    _payload_length = 1
    _payload_data = bytearray(b'\x00')

    @property
    def payload_node_type_filter(self):
        return self[10]

    @payload_node_type_filter.setter
    def payload_node_type_filter(self, value):
        self[10] = value


class NodeDiscoveryResponse(Packet):
    # AutoNet
    message_type = NODE_DISCOVERY_RESPONSE
    _payload_length = 18
    _payload_data = bytearray(b'\x00' * 18)

    @property
    def payload_node_type(self):
        return self[10]

    @payload_node_type.setter
    def payload_node_type(self, value):
        self[10] = value

    @property
    def payload_mac_address(self):
        return mac_address.MACAddress(self[12:20])

    @payload_mac_address.setter
    def payload_mac_address(self, value):
        mac = mac_address.MACAddress(value)
        for i, item in enumerate(mac):
            self[i + 12] = item

    @property
    def payload_session_id(self):
        return session_id.SessionId(self[20:28])

    @payload_session_id.setter
    def payload_session_id(self, value):
        mac = session_id.SessionId(value)
        for i, item in enumerate(mac):
            self[i + 20] = item


class SetAddressRequest(Packet):
    # AutoNet
    message_type = SET_ADDRESS
    _payload_length = 19
    _payload_data = bytearray(b'\x00' * 18 + b'\x01')

    @property
    def payload_address(self):
        return self[10]

    @payload_address.setter
    def payload_address(self, value):
        self[10] = value

    @property
    def payload_subnet(self):
        return self[11]

    @payload_subnet.setter
    def payload_subnet(self, value):
        self[11] = value

    @property
    def payload_mac_address(self):
        return mac_address.MACAddress(self[12:20])

    @payload_mac_address.setter
    def payload_mac_address(self, value):
        mac = mac_address.MACAddress(value)
        for i, item in enumerate(mac):
            self[i + 12] = item

    @property
    def payload_session_id(self):
        return session_id.SessionId(self[20:28])

    @payload_session_id.setter
    def payload_session_id(self, value):
        mac = session_id.SessionId(value)
        for i, item in enumerate(mac):
            self[i + 20] = item


class SetAddressResponse(SetAddressRequest):
    # AutoNet
    message_type = SET_ADDRESS_RESPONSE


class GetNodeIdRequest(Packet):
    message_type = GET_NODE_ID
    _payload_length = 1
    _payload_data = bytearray(b'\x00')


class GetNodeIdResponse(Packet):
    message_type = GET_NODE_ID_RESPONSE
    _payload_length = 17
    _payload_data = bytearray(b'\x00' * 17)

    @property
    def payload_node_type(self):
        return self[11]

    @payload_node_type.setter
    def payload_node_type(self, value):
        self[11] = value

    @property
    def payload_mac_address(self):
        return mac_address.MACAddress(self[12:20])

    @payload_mac_address.setter
    def payload_mac_address(self, value):
        mac = mac_address.MACAddress(value)
        for i, item in enumerate(mac):
            self[i + 12] = item

    @property
    def payload_session_id(self):
        return session_id.SessionId(self[20:28])

    @payload_session_id.setter
    def payload_session_id(self, value):
        mac = session_id.SessionId(value)
        for i, item in enumerate(mac):
            self[i + 20] = item


class NetworkSharedDataSectorImageReadWriteRequest(Packet):
    message_type = NETWORK_SHARED_DATA_SECTOR_IMAGE_READ_WRITE_REQUEST


class NetworkSharedDataSectorImageReadWriteResponse(Packet):
    message_type = NETWORK_SHARED_DATA_SECTOR_IMAGE_READ_WRITE_REQUEST_RESPONSE


class NetworkEncapsulationRequest(Packet):
    message_type = NETWORK_ENCAPSULATION_REQUEST


class NetworkEncapsulationResponse(Packet):
    message_type = NETWORK_ENCAPSULATION_REQUEST_RESPONSE


PACKET_CLASSES = (
    GetConfigurationRequest,
    GetConfigurationResponse,
    GetStatusRequest,
    GetStatusResponse,
    SetControlCommandRequest,
    SetControlCommandResponse,
    SetDisplayMessageRequest,
    SetDisplayMessageResponse,
    SetDisgnosticsRequest,
    SetDisgnosticsResponse,
    GetDiagnosticsRequest,
    GetDiagnosticsResponse,
    GetSensorDataRequest,
    GetSensorDataResponse,
    SetIdentificationDataRequest,
    SetIdentificationDataResponse,
    GetIdentificationDataRequest,
    GetIdentificationDataResponse,
    SetApplicationSharedDataToNetworkRequest,
    SetApplicationSharedDataToNetworkResponse,
    GetApplicationSharedDataToNetworkRequest,
    GetApplicationSharedDataToNetworkResponse,
    SetManufacturerDeviceDataRequest,
    SetManufacturerDeviceDataResponse,
    GetManufacturerDeviceDataRequest,
    GetManufacturerDeviceDataResponse,
    SetNetworkNodeListRequest,
    SetNetworkNodeListResponse,
    DirectMemoryAccessReadRequest,
    DirectMemoryAccessReadResponse,
    DirectMemoryAccessReadResponseMotor,
    SetManufacturerGenericDataRequest,
    SetManufacturerGenericDataResponse,
    GetManufacturerGenericDataRequest,
    GetManufacturerGenericDataResponse,
    GetManufacturerGenericDataResponseMotor,
    GetUserMenuRequest,
    GetUserMenuResponse,
    SetUserMenuRequest,
    SetUserMenuResponse,
    SetFactorySharedDataToApplicationRequest,
    SetFactorySharedDataToApplicationResponse,
    GetSharedDataFromApplicationRequest,
    GetSharedDataFromApplicationResponse,
    SetEchoRequest,
    SetEchoResponse,
    RequestToReceiveRequest,
    RequestToReceiveResponse,
    NetworkStateRequest,
    NetworkStateResponse,
    AddressConfirmationRequest,
    AddressConfirmationResponse,
    TokenOffer,
    TokenOfferResponse,
    VersionAnnouncement,
    NodeDiscoveryRequest,
    NodeDiscoveryResponse,
    SetAddressRequest,
    SetAddressResponse,
    GetNodeIdRequest,
    GetNodeIdResponse,
    NetworkSharedDataSectorImageReadWriteRequest,
    NetworkSharedDataSectorImageReadWriteResponse,
    NetworkEncapsulationRequest,
    NetworkEncapsulationResponse
)
