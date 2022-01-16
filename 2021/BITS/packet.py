class Packet:
    def __init__(self, version: int, packet_type: int, value: int, subpackets: list):
        self.version = version
        self.packet_type = packet_type
        self.value = value
        self.subpackets = subpackets
    
    def __str__(self):
        return self._print_packet(self).rstrip('\n')
    
    def _print_packet(self, packet, indentation_level = 0, subpacket_index = 0) -> str:
        indentation = ''.join(['\t'] * indentation_level)
        print_string = indentation + '##### Packet ' + str(subpacket_index) + ' #####\n'
        print_string += indentation + 'version: ' + str(packet.version) + '\n'
        print_string += indentation + 'type: ' + str(packet.packet_type) + '\n'
        print_string += '' if packet.value is None else indentation + 'value: ' + str(packet.value) + '\n'
        for i, subpacket in enumerate(packet.subpackets):
            print_string += '\n' + self._print_packet(subpacket, indentation_level + 1, i)
        return print_string