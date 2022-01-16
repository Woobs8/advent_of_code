import argparse
import sys
sys.path.append("..")
from BITS.packet import Packet
from BITS.packet_decoder import PacketDecoder

def read_from_file(fp:str) -> str:
    with open(fp, 'r') as f:
        return ''.join(f.read().splitlines())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 16, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    transmission = read_from_file(args.input)
    decoder = PacketDecoder()
    packet, remaining_transmission = decoder.decode_transmission(transmission)
    print(packet)