import argparse
import sys
sys.path.append('..')
from Intcode.IntcodeComputer import IntcodeComputer
from collections import deque


def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return list(map(int, f.read().split(',')))


def BOOST_program(memory:list) -> int:
    program = IntcodeComputer(memory)
    out = []
    res = program.execute(deque([1]), out)
    return out.pop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 9, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    memory = read_from_file(args.input)
    keycode = BOOST_program(memory)
    print(keycode)