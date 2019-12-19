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


def scan_area(memory:list, x_fit, y_fit, start_pos=None) -> Union[list, int]:
    program = IntcodeComputer(memory)
    affected = 0
    positions = [start_pos] if start_pos else [(0,0)]
    visited = set()
    while positions:
        rx, ry = positions.pop()
        if (rx, ry) in visited:
            continue
        visited.add((rx, ry))
        in_beam(program, rx, ry)

        if in_beam(program, rx, ry):    
            lx = rx - (x_fit-1)
            ly = ry + (y_fit-1)
            if lx >= 0 and ly >= 0:
                if in_beam(program, lx, ly):
                    break
            positions += [(rx, ry+1), (rx+1, ry)]
    return (lx, ry)


def in_beam(program:IntcodeComputer, x:int, y:int) -> int:
    out = []
    program.execute(deque([x,y]), out)
    program.reset()
    return out.pop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 19, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    memory = read_from_file(args.input)
    point = scan_area(memory, 100, 100, (11,6))
    print(point[0]*10000+point[1])
    