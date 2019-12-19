import argparse
import sys
sys.path.append('..')
from intcode.IntcodeComputer import IntcodeComputer
from typing import Union
from itertools import product
from collections import deque


def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return list(map(int, f.read().split(',')))


def scan_area(memory:list, x_lim:int, y_lim:int) -> Union[list, int]:
    program = IntcodeComputer(memory)
    area = [['.']*x_lim for __ in range(y_lim)]
    affected = 0
    for x, y in product(range(x_lim), range(y_lim)):
        out = []
        program.execute(deque([x,y]), out)
        program.reset()
        if out[-1] == 1:
            area[y][x] = '#'
            affected += 1
    return area, affected


def print_area(area:list) -> None:
    for line in area:
        print(''.join(line))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 19, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    memory = read_from_file(args.input)
    area, affected = scan_area(memory, 50, 50)
    print_area(area)
    print(affected)
