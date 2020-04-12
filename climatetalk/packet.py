# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser
import six
from .message_types import *
from . import mac_address
from . import session_id

CT_ISUM1 = 0xAA  # New Fletcher Seed.
CT_ISUM2 = 0x00

ACK = 0x06
NAK = 0x15

SEND_METHOD_NON_ROUTED = 0x00
SEND_METHOD_ROUTED_PRIORITY_CONTROL_COMMAND = 0x01
SEND_METHOD_ROUTED_PRIORITY_NODE_TYPE = 0x02
SEND_METHOD_ROUTED_SOCKET = 0x03


def _set_bit(value, bit, flag):
    if flag:
        value |= (1 << bit)
    else:
        value &= ~(1 << bit)

    return value


def _get_bit(value, bit):
    return value & (1 << bit) != 0


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
            if cl._message_type == data[7]:
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
    _message_type = 0x00
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
            self[7] = self._message_type
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
    _message_type = GET_CONFIGURATION
    _payload_length = 0
    _payload_data = bytearray()


class GetConfigurationResponse(Packet):
    _message_type = GET_CONFIGURATION_RESPONSE

    @property
    def payload_data(self):
        return self[11:-2]

    @payload_data.setter
    def payload_data(self, value):

        while len(self) < 10 + len(value):
            self.append(0x00)

        for i, item in enumerate(value):
            self[10 + i] = item


class GetStatusRequest(Packet):
    _message_type = GET_STATUS
    _payload_length = 0
    _payload_data = bytearray()


class GetStatusResponse(Packet):
    _message_type = GET_STATUS_RESPONSE

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
    _message_type = SET_CONTROL_COMMAND

    @property
    def payload_command_code(self):
        return self[10] << 8 | self[11]

    @payload_command_code.setter
    def payload_command_code(self, value):
        while len(self) < 12:
            self.append(0x00)

        self[10] = value >> 8 & 0xFF
        self[11] = value & 0xFF

    @property
    def payload_command_data(self):
        if len(self) == 17:
            return self[12] << 8 | self[13]
        else:
            return self[12]

    @payload_command_data.setter
    def payload_command_data(self, value):

        while len(self) < 12 + len(value):
            self.append(0x00)

        if len(value) == 2:
            self[12] = value >> 8 & 0xFF
            self[13] = value & 0xFF
        else:
            self[12] = value


class SetControlCommandResponse(SetControlCommandRequest):
    _message_type = SET_CONTROL_COMMAND_RESPONSE


class SetDisplayMessageRequest(Packet):
    _message_type = SET_DISPLAY_MESSAGE

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
    _message_type = SET_DISPLAY_MESSAGE_RESPONSE
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
    _message_type = SET_DISGNOSTICS

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
    _message_type = SET_DISGNOSTICS_RESPONSE
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
    _message_type = GET_DIAGNOSTICS
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
    _message_type = GET_DIAGNOSTICS_RESPONSE

    def __iter__(self):
        fault = bytearray()
        for char in self[11:-2]:
            if char == 0x00:
                yield fault
                fault = bytearray()
            else:
                fault.append(char)


class GetSensorDataRequest(Packet):
    _message_type = GET_SENSOR_DATA
    _payload_length = 0
    _payload_data = bytearray()


class GetSensorDataResponse(Packet):
    _message_type = GET_SENSOR_DATA_RESPONSE

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
    _message_type = SET_IDENTIFICATION

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
    _message_type = SET_IDENTIFICATION_RESPONSE
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
    _message_type = GET_IDENTIFICATION
    _payload_length = 0
    _payload_data = bytearray()


class GetIdentificationDataResponse(Packet):
    _message_type = GET_IDENTIFICATION_RESPONSE

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
    _message_type = SET_APPLICATION_SHARED_DATA_TO_NETWORK

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
    _message_type = SET_APPLICATION_SHARED_DATA_TO_NETWORK_RESPONSE


class GetApplicationSharedDataToNetworkRequest(Packet):
    _message_type = GET_APPLICATION_SHARED_DATA_TO_NETWORK
    _payload_length = 1
    _payload_data = bytearray(b'\x00')

    @property
    def payload_sector_node_type(self):
        return self[10]

    @payload_sector_node_type.setter
    def payload_sector_node_type(self, value):
        self[10] = value


class GetApplicationSharedDataToNetworkResponse(GetApplicationSharedDataToNetworkRequest):
    _message_type = GET_APPLICATION_SHARED_DATA_TO_NETWORK_RESPONSE

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
    _message_type = SET_MANUFACTURER_DEVICE_DATA

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
    _message_type = SET_MANUFACTURER_DEVICE_DATA_RESPONSE


class GetManufacturerDeviceDataRequest(Packet):
    _message_type = GET_MANUFACTURER_DEVICE_DATA
    _payload_length = 0
    _payload_data = bytearray()


class GetManufacturerDeviceDataResponse(Packet):
    _message_type = GET_MANUFACTURER_DEVICE_DATA_RESPONSE

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
    _message_type = SET_NETWORK_NODE_LIST

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
    _message_type = SET_NETWORK_NODE_LIST_RESPONSE


class DirectMemoryAccessReadRequest(Packet):
    """
    MDI values (byte 1 of the payload)
    Configuration: 0x01
    Status: 0x02
    Sensor: 0x07
    IdentificationL 0x0E

    """
    _message_type = DIRECT_MEMORY_ACCESS_READ
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
    def payload_start_db_id(self):
        return self[12]

    @payload_start_db_id.setter
    def payload_start_db_id(self, value):
        self[12] = value

    @property
    def payload_range(self):
        return self[13]

    @payload_range.setter
    def payload_range(self, value):
        self[13] = value


class DirectMemoryAccessReadResponse(Packet):
    _message_type = DIRECT_MEMORY_ACCESS_READ_RESPONSE

    @property
    def payload_data(self):
        return self[11:-2]

    @payload_data.setter
    def payload_data(self, value):
        while len(self) < 11 + len(value):
            self.append(0x00)

        for i, item in enumerate(value):
            self[i + 10] = item


class SetManufacturerGenericDataRequest(Packet):
    _message_type = SET_MANUFACTURER_GENERIC_DATA

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
    _message_type = SET_MANUFACTURER_GENERIC_DATA_RESPONSE


class GetManufacturerGenericDataRequest(Packet):
    _message_type = GET_MANUFACTURER_GENERIC_DATA

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
    _message_type = GET_MANUFACTURER_GENERIC_DATA_RESPONSE


class GetUserMenuRequest(Packet):
    _message_type = GET_USER_MENU
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
    _message_type = GET_USER_MENU_RESPONSE

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
    _message_type = SET_USER_MENU
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
    _message_type = SET_USER_MENU_RESPONSE
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
    _message_type = SET_FACTORY_SHARED_DATA_TO_APPLICATION

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
    _message_type = SET_FACTORY_SHARED_DATA_TO_APPLICATION_RESPONSE


class GetSharedDataFromApplicationRequest(Packet):
    _message_type = GET_SHARED_DATA_FROM_APPLICATION
    _payload_length = 1
    _payload_data = bytearray(b'\x00')


class GetSharedDataFromApplicationResponse(Packet):
    _message_type = GET_SHARED_DATA_FROM_APPLICATION_RESPONSE

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
    _message_type = SET_ECHO_DATA


class SetEchoResponse(Packet):
    _message_type = SET_ECHO_DATA_RESPONSE


class RequestToReceiveRequest(Packet):
    _message_type = REQUEST_TO_RECEIVE
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
    _message_type = REQUEST_TO_RECEIVE_RESPONSE
    _payload_length = 17
    _payload_data = bytearray(b'\x00' * 17)
    _payload_data[10] = 0x06


class NetworkStateRequest(Packet):
    _message_type = NETWORK_STATE_REQUEST
    _payload_length = 1
    _payload_data = bytearray(b'\x00')


class NetworkStateResponse(Packet):
    _message_type = NETWORK_STATE_REQUEST_RESPONSE

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
    _message_type = ADDRESS_CONFIRMATION

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
    _message_type = ADDRESS_CONFIRMATION_RESPONSE

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
    _message_type = TOKEN_OFFER
    _payload_length = 1
    _payload_data = bytearray(b'\x00')

    @property
    def payload_node_type_filter(self):
        return self[10]

    @payload_node_type_filter.setter
    def payload_node_type_filter(self, value):
        self[10] = value


class TokenOfferResponse(Packet):
    _message_type = TOKEN_OFFER_RESPONSE
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
    _message_type = VERSION_ANNOUNCEMENT
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
    _message_type = NODE_DISCOVERY
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
    _message_type = NODE_DISCOVERY_RESPONSE
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
    _message_type = SET_ADDRESS
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
    _message_type = SET_ADDRESS_RESPONSE


class GetNodeIdRequest(Packet):
    _message_type = GET_NODE_ID
    _payload_length = 1
    _payload_data = bytearray(b'\x00')


class GetNodeIdResponse(Packet):
    _message_type = GET_NODE_ID_RESPONSE
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
    _message_type = NETWORK_SHARED_DATA_SECTOR_IMAGE_READ_WRITE_REQUEST


class NetworkSharedDataSectorImageReadWriteResponse(Packet):
    _message_type = NETWORK_SHARED_DATA_SECTOR_IMAGE_READ_WRITE_REQUEST_RESPONSE


class NetworkEncapsulationRequest(Packet):
    _message_type = NETWORK_ENCAPSULATION_REQUEST


class NetworkEncapsulationResponse(Packet):
    _message_type = NETWORK_ENCAPSULATION_REQUEST_RESPONSE


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
    SetManufacturerGenericDataRequest,
    SetManufacturerGenericDataResponse,
    GetManufacturerGenericDataRequest,
    GetManufacturerGenericDataResponse,
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
