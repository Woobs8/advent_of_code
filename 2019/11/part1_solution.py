import argparse
import sys
sys.path.append('..')
from Intcode.IntcodeComputer import IntcodeComputer
from collections import defaultdict
from typing import Union


# represenations of panel colors
class PANELS():
    BLACK = '.'
    WHITE = '#'


# values representing the panel colors
COLOR_CODES = {
    PANELS.BLACK:0,
    PANELS.WHITE:1,
    0:PANELS.BLACK,
    1:PANELS.WHITE
}


# the direction the robot is facing
class DIRECTION():
    NORTH = 1
    SOUTH = -1
    WEST = 1j
    EAST = -1j


# values representing whether the robot must turn left or right
class TURN():
    LEFT = 0
    RIGHT = 1


def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return list(map(int, f.read().split(',')))


def paint_hull(memory:list) -> Union[dict, dict]:
    program = IntcodeComputer(memory)
    hull = defaultdict(lambda:PANELS.BLACK)
    painted = defaultdict(lambda:0)

    res = IntcodeComputer.OUTPUT_CODES.OK
    loc = (0,0)
    facing = DIRECTION.NORTH
    while res != IntcodeComputer.OUTPUT_CODES.HALTED:
        panel_color = hull[loc]
        out = []
        res = program.execute([COLOR_CODES[panel_color]], out)
        hull[loc] = COLOR_CODES[out[0]]
        painted[loc] += 1
        loc, facing = move(loc, facing, out[1])
    return hull, painted


def move(loc:tuple, cur_direction:complex, move_code:int) -> Union[tuple, complex]:
    new_direction = cur_direction*1j if move_code == TURN.LEFT else cur_direction*-1j
    if new_direction == DIRECTION.NORTH:
        move_vector = (0,1)
    elif new_direction == DIRECTION.SOUTH:
        move_vector = (0,-1)
    elif new_direction == DIRECTION.WEST:
        move_vector = (-1,0)
    elif new_direction == DIRECTION.EAST:
        move_vector = (1,0)

    loc = tuple(map(sum,zip(loc,move_vector)))
    return loc, new_direction


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 11, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    memory = read_from_file(args.input)
    hull, painted = paint_hull(memory)
    print(len(painted))