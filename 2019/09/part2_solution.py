import argparse
import sys
sys.path.append('..')
from Intcode.IntcodeComputer import IntcodeComputer
from collections import defaultdict


# represenations of panel colors
BLACK = '.'
WHITE = '#'


# values representing the panel colors
COLOR_CODES = {
    BLACK:0,
    WHITE:1
}

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return list(map(int, f.read().split(',')))


def hull_painting_robot(memory:list):
    program = IntcodeComputer(memory)
    hull = defaultdict(lambda:BLACK)
    painted = defaultdict(lambda:0)

    res = IntcodeComputer.OUTPUT_CODES.OK
    loc = (0,0)
    while res != IntcodeComputer.OUTPUT_CODES.HALTED:
        panel_color = hull[loc]
        out = []
        res = program.execute([COLOR_CODES[panel_color]], out)

        hull[loc] = COLOR_CODES[out[0]]





def BOOST_program(memory:list) -> int:
    program = IntcodeComputer(memory)
    out = []
    res = program.execute([2], out)
    return out.pop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 9, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    memory = read_from_file(args.input)
    keycode = BOOST_program(memory)
    print(keycode)