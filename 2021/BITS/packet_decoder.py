from BITS.packet import Packet
from functools import reduce
import operator

# packet types
SUM_PACKET_TYPE = 0
PRODUCT_PACKET_TYPE = 1
MINIMUM_PACKET_TYPE = 2
MAXIMUM_PACKET_TYPE = 3
LITERAL_VALUE_PACKET_TYPE_ID = 4
GT_PACKET_TYPE = 5
LT_PACKET_TYPE = 6
EQ_PACKET_TYPE = 7

# field lengths
PACKET_VERSION_LENGTH = 3
PACKET_TYPE_LENGTH = 3
LITERAL_VALUE_LENGTH = 5
LENGTH_TYPE_ID_LENGTH = 1
SUBPACKETS_COUNT_LENGTH = 11
SUBPACKETS_LENGTH_LENGTH = 15

class PacketDecoder:
    def decode_transmission(self, transmission: str) -> (Packet, str):
        binary_transmission = self._hex_to_binary(transmission)
        packet, binary_transmission = self._decode_packet(binary_transmission)
        return packet, binary_transmission

    def _hex_to_binary(self, hex_string: str) -> str:
        return str(( bin(int(hex_string, 16))[2:] ).zfill(len(hex_string)*4))

    def _decode_packet(self, binary_transmission: str) -> (Packet, str):
        version, binary_transmission = self._extract_slice_as_int(binary_transmission, PACKET_VERSION_LENGTH)
        packet_type, binary_transmission = self._extract_slice_as_int(binary_transmission, PACKET_TYPE_LENGTH)
        if packet_type == LITERAL_VALUE_PACKET_TYPE_ID:
            literal_value, binary_transmission = self._extract_literal_value(binary_transmission)
            return Packet(version, packet_type, literal_value, []), binary_transmission
        else:
            length_type_id, binary_transmission = self._extract_slice_as_int(binary_transmission, LENGTH_TYPE_ID_LENGTH)
            if length_type_id == 1:
                subpackets_count, binary_transmission = self._extract_slice_as_int(binary_transmission, SUBPACKETS_COUNT_LENGTH)
                subpackets, binary_transmission = self._extract_subpackets_by_count(binary_transmission, subpackets_count)
            elif length_type_id == 0:
                subpackets_length, binary_transmission = self._extract_slice_as_int(binary_transmission, SUBPACKETS_LENGTH_LENGTH)
                subpackets, binary_transmission = self._extract_subpackets_by_length(binary_transmission, subpackets_length)
            else:
                subpackets = []
            value = self.calculate_package_value(packet_type, subpackets)
            return Packet(version, packet_type, value, subpackets), binary_transmission

    def _extract_slice_as_int(self, binary_transmission: str, length: int) -> (int, str):
        subsection = int(binary_transmission[:length], 2)
        binary_transmission = binary_transmission[length:]
        return subsection, binary_transmission

    def _extract_subpackets_by_count(self, binary_transmission: str, subpackets_count: int) -> (list, str):
        subpackets = []
        for __ in range(subpackets_count):
            subpacket, binary_transmission = self._decode_packet(binary_transmission)
            subpackets.append(subpacket)
        return subpackets, binary_transmission

    def _extract_subpackets_by_length(self, binary_transmission: str, subpackets_length: int) -> (list, str):
        subpackets = []
        initial_transmission_length = len(binary_transmission)
        while initial_transmission_length - len(binary_transmission) < subpackets_length:
            subpacket, binary_transmission = self._decode_packet(binary_transmission)
            subpackets.append(subpacket)
        return subpackets, binary_transmission

    def _extract_literal_value(self, binary_transmission: str) -> (int, str):
        literal_value_string = ''
        stop = False
        while not stop:
            group_order_bit = binary_transmission[0]
            value_bits = binary_transmission[1:LITERAL_VALUE_LENGTH]
            literal_value_string += value_bits
            binary_transmission = binary_transmission[LITERAL_VALUE_LENGTH:]
            if group_order_bit == '0':
                stop = True
        return int(literal_value_string, 2), binary_transmission 

    def calculate_package_value(self, packet_type: int, subpackets: list) -> int:
        if packet_type == SUM_PACKET_TYPE:
            return sum([subpacket.value for subpacket in subpackets])
        elif packet_type == PRODUCT_PACKET_TYPE:
            return reduce(operator.mul, [subpacket.value for subpacket in subpackets], 1)
        elif packet_type == MINIMUM_PACKET_TYPE:
            return min([subpacket.value for subpacket in subpackets])
        elif packet_type == MAXIMUM_PACKET_TYPE:
            return max([subpacket.value for subpacket in subpackets])
        elif packet_type == GT_PACKET_TYPE:
            return 1 if subpackets[0].value > subpackets[1].value else 0
        elif packet_type == LT_PACKET_TYPE:
            return 1 if subpackets[0].value < subpackets[1].value else 0
        elif packet_type == EQ_PACKET_TYPE:
            return 1 if subpackets[0].value == subpackets[1].value else 0
        else:
            return None