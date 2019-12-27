import argparse
import sys
sys.path.append('..')
from Intcode.IntcodeComputer import IntcodeComputer
from typing import Union
from collections import deque


def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return list(map(int, f.read().split(',')))


def survey_hull(memory:list) -> int:
    program = IntcodeComputer(memory)
    input = deque(create_input())
    out = []
    program.execute(input, out)
    print_output(out)
    return out[-1]


def create_input() -> list:
    logic = define_logic()
    input = []
    for instr in logic:
        input += [ord(c) for c in instr] + [ord('\n')]
    input += [ord('R'), ord('U'), ord('N')]
    return input + [ord('\n')]


def define_logic() -> list:
    # D && (!A || !B || (!C && (!F || H))
    return ['NOT F T',
            'OR H T',
            'OR T J',
            'NOT C T',
            'AND T J',
            'NOT A T',
            'OR T J',
            'NOT B T',
            'OR T J',
            'AND D J']


def print_output(out:list) -> None:
    for c in out:
        if c in range(0x110000):
            print(chr(c), end='')
        else:
            print(c)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 21, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    memory = read_from_file(args.input)
    hull_damage = survey_hull(memory)