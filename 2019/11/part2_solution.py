import argparse
import sys
sys.path.append('..')
from Intcode.IntcodeComputer import IntcodeComputer
from util.print_to_console import print_bw_image_to_console
from collections import defaultdict
from typing import Union
from itertools import product


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


def paint_hull(memory:list, initial_panel=PANELS.BLACK) -> Union[defaultdict, defaultdict]:
    program = IntcodeComputer(memory)
    loc = (0,0)

    hull = defaultdict(lambda:PANELS.BLACK)
    hull[loc] = initial_panel
    painted = defaultdict(lambda:0)

    res = IntcodeComputer.OUTPUT_CODES.OK
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
        move_vector = (0,-1)
    elif new_direction == DIRECTION.SOUTH:
        move_vector = (0,1)
    elif new_direction == DIRECTION.WEST:
        move_vector = (-1,0)
    elif new_direction == DIRECTION.EAST:
        move_vector = (1,0)

    loc = tuple(map(sum,zip(loc,move_vector)))
    return loc, new_direction


def print_registration_identifier(hull:defaultdict) -> None:
    panels = list(hull.keys())
    identifier = create_painted_identifier(panels)
    print_bw_image_to_console(identifier, PANELS.WHITE, PANELS.BLACK)


def create_painted_identifier(panels) -> list:
    x_min, x_max, y_min, y_max = get_hull_boundaries(panels)
    width = x_max-x_min+1
    height = y_max-y_min+1
    painted_identifer = [[None]*width for __ in range(height)]
    for x, y in product(range(x_min, x_max+1), range(y_min, y_max+1)):
        painted_identifer[y-y_min][x-x_min] = hull[(x,y)]
    
    return painted_identifer


def get_hull_boundaries(panels:list) -> Union[int, int, int, int]:
    panels_by_x = sorted(panels, key=lambda x: x[0])
    x_min = panels_by_x[0][0]
    x_max = panels_by_x[-1][0]

    panels_by_y = sorted(panels, key=lambda y: y[1])
    y_min = panels_by_y[0][1]
    y_max = panels_by_y[-1][1]

    return x_min, x_max, y_min, y_max


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 11, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    memory = read_from_file(args.input)
    hull, painted = paint_hull(memory, PANELS.WHITE)
    print_registration_identifier(hull)