# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser
import six
from .message_types import *

CT_ISUM1 = 0xAA  # New Fletcher Seed.
CT_ISUM2 = 0x00


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
            _payload_data=data[10:-2]
        )
        cl = type('DynamicPacket', (cl,), namespace)
        instance = cl(*args, **kwargs)
        return instance


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

    def cacl_checksum(self):
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


class GetConfiguration(Packet):
    _message_type = GET_CONFIGURATION
    _payload_length = 0x01
    _payload_data = bytearray(b'\x00')


class GetConfigurationResponse(Packet):
    _message_type = GET_CONFIGURATION_RESPONSE


class GetStatus(Packet):
    _message_type = GET_STATUS
    _payload_length = 0x01
    _payload_data = bytearray(b'\x00')


class GetStatusResponse(Packet):
    _message_type = GET_STATUS_RESPONSE


class SetControlCommand(Packet):
    _message_type = SET_CONTROL_COMMAND


class SetControlCommandResponse(Packet):
    _message_type = SET_CONTROL_COMMAND_RESPONSE


class SetDisplayMessage(Packet):
    _message_type = SET_DISPLAY_MESSAGE


class SetDisplayMessageResponse(Packet):
    _message_type = SET_DISPLAY_MESSAGE_RESPONSE
    _payload_length = 2
    _payload_data = bytearray(b'\xAC\x06')


class SetDisgnostics(Packet):
    _message_type = SET_DISGNOSTICS


class SetDisgnosticsResponse(Packet):
    _message_type = SET_DISGNOSTICS_RESPONSE
    _payload_length = 2
    _payload_data = bytearray(b'\xAC\x06')


class GetDiagnostics(Packet):
    _message_type = GET_DIAGNOSTICS
    _payload_length = 2
    _payload_data = bytearray(b'\x00\x00')


class GetDiagnosticsResponse(Packet):
    _message_type = GET_DIAGNOSTICS_RESPONSE


class GetSensorData(Packet):
    _message_type = GET_SENSOR_DATA
    _payload_length = 1
    _payload_data = bytearray(b'\x00')


class GetSensorDataResponse(Packet):
    _message_type = GET_SENSOR_DATA_RESPONSE


class SetIdentification(Packet):
    _message_type = SET_IDENTIFICATION


class SetIdentificationResponse(Packet):
    _message_type = SET_IDENTIFICATION_RESPONSE
    _payload_length = 2
    _payload_data = bytearray(b'\xAC\x06')


class GetIdentification(Packet):
    _message_type = GET_IDENTIFICATION
    _payload_length = 1
    _payload_data = bytearray(b'\x00')


class GetIdentificationResponse(Packet):
    _message_type = GET_IDENTIFICATION_RESPONSE


class SetApplicationSharedDataToNetwork(Packet):
    _message_type = SET_APPLICATION_SHARED_DATA_TO_NETWORK


class SetApplicationSharedDataToNetworkResponse(Packet):
    _message_type = SET_APPLICATION_SHARED_DATA_TO_NETWORK_RESPONSE


class GetApplicationSharedDataToNetwork(Packet):
    _message_type = GET_APPLICATION_SHARED_DATA_TO_NETWORK
    _payload_length = 1
    _payload_data = bytearray(b'\x00')


class GetApplicationSharedDataToNetworkResponse(Packet):
    _message_type = GET_APPLICATION_SHARED_DATA_TO_NETWORK_RESPONSE


class SetManufacturerDeviceData(Packet):
    _message_type = SET_MANUFACTURER_DEVICE_DATA


class SetManufacturerDeviceDataResponse(Packet):
    _message_type = SET_MANUFACTURER_DEVICE_DATA_RESPONSE


class GetManufacturerDeviceData(Packet):
    _message_type = GET_MANUFACTURER_DEVICE_DATA
    _payload_length = 1
    _payload_data = bytearray(b'\x00')


class GetManufacturerDeviceDataResponse(Packet):
    _message_type = GET_MANUFACTURER_DEVICE_DATA_RESPONSE


class SetNetworkNodeList(Packet):
    _message_type = SET_NETWORK_NODE_LIST


class SetNetworkNodeListResponse(Packet):
    _message_type = SET_NETWORK_NODE_LIST_RESPONSE


class DirectMemoryAccessRead(Packet):
    """
    MDI values (byte 1 of the payload)
    Configuration: 0x01
    Status: 0x02
    Sensor: 0x07
    IdentificationL 0x0E

    """
    _message_type = DIRECT_MEMORY_ACCESS_READ


class DirectMemoryAccessReadResponse(Packet):
    _message_type = DIRECT_MEMORY_ACCESS_READ_RESPONSE


class SetManufacturerGenericData(Packet):
    _message_type = SET_MANUFACTURER_GENERIC_DATA


class SetManufacturerGenericDataResponse(Packet):
    _message_type = SET_MANUFACTURER_GENERIC_DATA_RESPONSE


class GetManufacturerGenericData(Packet):
    _message_type = GET_MANUFACTURER_GENERIC_DATA


class GetManufacturerGenericDataResponse(Packet):
    _message_type = GET_MANUFACTURER_GENERIC_DATA_RESPONSE


class GetUserMenu(Packet):
    _message_type = GET_USER_MENU


class GetUserMenuResponse(Packet):
    _message_type = GET_USER_MENU_RESPONSE


class SetUserMenu(Packet):
    _message_type = SET_USER_MENU
    _payload_length = 7
    _payload_data = bytearray(b'\x00' * 7)


class SetUserMenuResponse(Packet):
    _message_type = SET_USER_MENU_RESPONSE
    _payload_length = 8
    _payload_data = bytearray(b'\x00' * 8)


class SetFactorySharedDataToApplication(Packet):
    _message_type = SET_FACTORY_SHARED_DATA_TO_APPLICATION


class SetFactorySharedDataToApplicationResponse(Packet):
    _message_type = SET_FACTORY_SHARED_DATA_TO_APPLICATION_RESPONSE


class GetSharedDataFromApplication(Packet):
    _message_type = GET_SHARED_DATA_FROM_APPLICATION
    _payload_length = 1
    _payload_data = bytearray(b'\x00')


class GetSharedDataFromApplicationResponse(Packet):
    _message_type = GET_SHARED_DATA_FROM_APPLICATION_RESPONSE


class SetEchoData(Packet):
    _message_type = SET_ECHO_DATA


class SetEchoDataResponse(Packet):
    _message_type = SET_ECHO_DATA_RESPONSE


class RequestToReceive(Packet):
    _message_type = REQUEST_TO_RECEIVE
    _payload_length = 17
    _payload_data = bytearray(b'\x00' * 17)


class RequestToReceiveResponse(Packet):
    _message_type = REQUEST_TO_RECEIVE_RESPONSE
    _payload_length = 17
    _payload_data = bytearray(b'\x00' * 17)


class NetworkStateRequest(Packet):
    _message_type = NETWORK_STATE_REQUEST
    _payload_length = 1
    _payload_data = bytearray(b'\x00')


class NetworkStateRequestResponse(Packet):
    _message_type = NETWORK_STATE_REQUEST_RESPONSE


class AddressConfirmation(Packet):
    _message_type = ADDRESS_CONFIRMATION


class AddressConfirmationResponse(Packet):
    _message_type = ADDRESS_CONFIRMATION_RESPONSE


class TokenOffer(Packet):
    _message_type = TOKEN_OFFER
    _payload_length = 1
    _payload_data = bytearray(b'\x00')


class TokenOfferResponse(Packet):
    _message_type = TOKEN_OFFER_RESPONSE
    _payload_length = 18
    _payload_data = bytearray(b'\x00' * 18)


class VersionAnnouncement(Packet):
    _message_type = VERSION_ANNOUNCEMENT
    _payload_length = 5
    _payload_data = bytearray(b'\x00' * 5)


class NodeDiscovery(Packet):
    _message_type = NODE_DISCOVERY
    _payload_length = 1
    _payload_data = bytearray(b'\x00')


class NodeDiscoveryResponse(Packet):
    _message_type = NODE_DISCOVERY_RESPONSE
    _payload_length = 18
    _payload_data = bytearray(b'\x00' * 18)


class SetAddress(Packet):
    _message_type = SET_ADDRESS
    _payload_length = 19
    _payload_data = bytearray(b'\x00' * 19)


class SetAddressResponse(Packet):
    _message_type = SET_ADDRESS_RESPONSE
    _payload_length = 19
    _payload_data = bytearray(b'\x00' * 19)


class GetNodeId(Packet):
    _message_type = GET_NODE_ID
    _payload_length = 1
    _payload_data = bytearray(b'\x00')


class GetNodeIdResponse(Packet):
    _message_type = GET_NODE_ID_RESPONSE
    _payload_length = 17
    _payload_data = bytearray(b'\x00' * 17)


class NetworkSharedDataSectorImageReadWriteRequest(Packet):
    _message_type = NETWORK_SHARED_DATA_SECTOR_IMAGE_READ_WRITE_REQUEST


class NetworkSharedDataSectorImageReadWriteRequestResponse(Packet):
    _message_type = NETWORK_SHARED_DATA_SECTOR_IMAGE_READ_WRITE_REQUEST_RESPONSE


class NetworkEncapsulationRequest(Packet):
    _message_type = NETWORK_ENCAPSULATION_REQUEST


class NetworkEncapsulationRequestResponse(Packet):
    _message_type = NETWORK_ENCAPSULATION_REQUEST_RESPONSE


PACKET_CLASSES = (
    GetConfiguration,
    GetConfigurationResponse,
    GetStatus,
    GetStatusResponse,
    SetControlCommand,
    SetControlCommandResponse,
    SetDisplayMessage,
    SetDisplayMessageResponse,
    SetDisgnostics,
    SetDisgnosticsResponse,
    GetDiagnostics,
    GetDiagnosticsResponse,
    GetSensorData,
    GetSensorDataResponse,
    SetIdentification,
    SetIdentificationResponse,
    GetIdentification,
    GetIdentificationResponse,
    SetApplicationSharedDataToNetwork,
    SetApplicationSharedDataToNetworkResponse,
    GetApplicationSharedDataToNetwork,
    GetApplicationSharedDataToNetworkResponse,
    SetManufacturerDeviceData,
    SetManufacturerDeviceDataResponse,
    GetManufacturerDeviceData,
    GetManufacturerDeviceDataResponse,
    SetNetworkNodeList,
    SetNetworkNodeListResponse,
    DirectMemoryAccessRead,
    DirectMemoryAccessReadResponse,
    SetManufacturerGenericData,
    SetManufacturerGenericDataResponse,
    GetManufacturerGenericData,
    GetManufacturerGenericDataResponse,
    GetUserMenu,
    GetUserMenuResponse,
    SetUserMenu,
    SetUserMenuResponse,
    SetFactorySharedDataToApplication,
    SetFactorySharedDataToApplicationResponse,
    GetSharedDataFromApplication,
    GetSharedDataFromApplicationResponse,
    SetEchoData,
    SetEchoDataResponse,
    RequestToReceive,
    RequestToReceiveResponse,
    NetworkStateRequest,
    NetworkStateRequestResponse,
    AddressConfirmation,
    AddressConfirmationResponse,
    TokenOffer,
    TokenOfferResponse,
    VersionAnnouncement,
    NodeDiscovery,
    NodeDiscoveryResponse,
    SetAddress,
    SetAddressResponse,
    GetNodeId,
    GetNodeIdResponse,
    NetworkSharedDataSectorImageReadWriteRequest,
    NetworkSharedDataSectorImageReadWriteRequestResponse,
    NetworkEncapsulationRequest,
    NetworkEncapsulationRequestResponse
)
