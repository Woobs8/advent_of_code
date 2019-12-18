import argparse
import sys
sys.path.append('..')
from intcode.IntcodeComputer import IntcodeComputer
from typing import Union
from enum import IntEnum
from functools import reduce


def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return list(map(int, f.read().split(',')))


def run_ascii_program(memory:list) -> list:
    print(memory)
    program = IntcodeComputer(memory)
    out = []
    program.execute([], out)
    return list(map(chr, out))


def sum_alignment_params(ascii_code:list) -> Union[int, list]:
    camera_view = create_camera_view(ascii_code)
    alignment_sum = 0

    for y in range(len(camera_view)):
        if y-1 < 0 or y+1 > len(camera_view)-1 or not camera_view[y+1]:
            continue
        for x in range(len(camera_view[y])):
            if x-1 < 0 or x+1 > len(camera_view[y])-1:
                continue

            left = camera_view[y][x-1]
            right = camera_view[y][x+1]
            top = camera_view[y-1][x]
            bottom = camera_view[y+1][x]

            is_intersection = all(is_scaffold(e) for e in [left, right, top, bottom])
            if is_intersection and camera_view[y][x] == '#':
                camera_view[y][x] = 'O'
                alignment_sum += x*y
    return alignment_sum, camera_view
        

def is_scaffold(ascii_char:int) -> bool:
    return ascii_char in ['#', '<', '>', '^', 'V']


def create_camera_view(ascii_code:list) -> None:
    lines = "".join(ascii_code).split('\n')
    return list(map(lambda x: [str(e) for e in x], lines))


def print_camera_view(view:list) -> None:
    for line in view:
        if line:
            print("".join(line))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 17, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    memory = read_from_file(args.input)
    output = run_ascii_program(memory)
    alignment_sum, camera_view = sum_alignment_params(output)
    print_camera_view(camera_view)
    print('Sum of alignment parameters: {}'.format(alignment_sum))