import argparse
from math import ceil
from functools import reduce


BASE_PATTERN = [0, 1, 0, -1]


def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return [int(x) for x in f.readlines()[0]]


def fft_phases(seq:list, base_pattern:list, phases:int) -> list:
    for __ in range(phases):
        seq = list(map(lambda x: calc_output_element(seq, x, base_pattern), range(len(seq))))
    return seq


def calc_output_element(seq:list, idx:int, base_pattern:list) -> int:
    pattern = get_pattern(base_pattern, len(seq), idx)
    return abs(sum(map(lambda x: x[0]*x[1], zip(seq, pattern)))) % 10


def get_pattern(base:list, pattern_len:int, idx:int) -> list:
    repeating = []
    for e in base:
        repeating += [e]*(idx+1)  
    pattern = repeating*(ceil(pattern_len/len(repeating))+1)
    return pattern[1:pattern_len+1]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 16, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    input_sequence = read_from_file(args.input)
    out = fft_phases(input_sequence, BASE_PATTERN, 100)
    print(out[:8])