import argparse
import sys
sys.path.append('..')
from Intcode.IntcodeComputer import IntcodeComputer
from typing import Union
from functools import reduce
import operator
import re
from collections import deque


class DIRECTIONS():
    LEFT = '<'
    RIGHT = '>'
    UP = '^'
    DOWN = 'V'


MOVES = {
    DIRECTIONS.LEFT:(-1,0),
    DIRECTIONS.RIGHT:(1,0),
    DIRECTIONS.UP:(0,-1),
    DIRECTIONS.DOWN:(0,1)
}


def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return list(map(int, f.read().split(',')))


def find_path(memory:list) -> list:
    memory = memory[:]
    camera_view = create_camera_view(memory)
    print_camera_view(camera_view)
    path = []
    x, y, dir = find_robot(camera_view)
    pos = (x,y)
    while dir:
        pos, dir, cmd = take_step(camera_view, pos, dir)
        path += cmd if cmd else []
    return path


def create_camera_view(memory:list) -> list:
    ascii_code = run_ascii_program(memory)
    lines = "".join(ascii_code).split('\n')
    camera_view = list(map(lambda x: [str(e) for e in x], lines))
    camera_view = list(filter(lambda x: x, camera_view))
    return camera_view


def run_ascii_program(memory:list) -> list:
    program = IntcodeComputer(memory)
    out = []
    program.execute([], out)
    return list(map(chr, out))


def print_camera_view(view:list) -> None:
    for line in view:
        if line:
            print("".join(line))


def find_robot(view:list) -> Union[int, int, str]:
    for y in range(len(view)):
        for x in range(len(view[y])):
            if view[y][x] in ['<', '>', '^', 'V']:
                return (x, y, view[y][x])


def take_step(view:list, pos:Union[int, int], dir:str) -> Union[int, str, str, str]:
    dir_cmd, new_dir = change_direction(view, pos, dir)
    if not dir_cmd:
        return pos, None, None
    step_count = 0
    x, y = pos
    next_step = '#'
    while next_step == '#':
        x, y = move_pos((x,y), MOVES[new_dir])
        if x >= 0 and x < len(view[0]) and y >= 0 and y < len(view):
            next_step = view[y][x]
            
            if next_step == '#':
                pos = (x,y)
                step_count += 1
        else:
            break
    return pos, new_dir, [dir_cmd, str(step_count)]


def change_direction(view:list, pos:Union[int, int], dir:str) -> Union[str, str]:
    x, y = pos
    if dir == DIRECTIONS.RIGHT or dir == DIRECTIONS.LEFT:
        if y > 0 and view[y-1][x] == '#':
            cmd = 'R' if dir == DIRECTIONS.LEFT else 'L'
            new_dir = DIRECTIONS.UP
        elif y < (len(view)-1) and view[y+1][x] == '#':
            cmd = 'L' if dir == DIRECTIONS.LEFT else 'R'
            new_dir = DIRECTIONS.DOWN
        else:
            cmd, new_dir = None, None
    else:
        if x > 0 and view[y][x-1] == '#':
            cmd = 'L' if dir == DIRECTIONS.UP else 'R'
            new_dir = DIRECTIONS.LEFT
        elif x < (len(view[0])-1) and view[y][x+1] == '#':
            cmd = 'R' if dir == DIRECTIONS.UP else 'L'
            new_dir = DIRECTIONS.RIGHT
        else:
            cmd, new_dir = None, None
    return cmd, new_dir      


def move_pos(cur_pos:Union[int, int], step:Union[int, int]) -> Union[int, int]:
    return tuple(map(operator.add, cur_pos, step))


def move_robot(memory:list, path:list, video_feed:bool=False) -> int:
    memory[0] = 2
    program = IntcodeComputer(memory)
    routines = convert_path_to_routines(path)
    routine_sequence = find_routine_sequence(path, routines)
    ascii_input = create_input(routines, routine_sequence, video_feed)
    out = []
    program.execute(deque(ascii_input), out)
    out_str = "".join(map(chr, out))
    return out[-1]


def convert_path_to_routines(path:list) -> list:
    path_str = ",".join(map(str,path))+','
    # shamelessly stolen from the AoC subreddit to avoid bruteforcing
    regex = r"^(.{1,21})\1*(.{1,21})(?:\1|\2)*(.{1,21})(?:\1|\2|\3)*$"
    return list(re.match(regex, path_str).groups())
    

def find_routine_sequence(path:list, routines:list) -> list:
    path_str = ",".join(map(str,path))+','
    sequence = []
    while path_str:
        for i, rout in enumerate(routines):
            idx = path_str.index(rout) if rout in path_str else -1
            if idx == 0:
                sequence.append(i)
                path_str = path_str[idx+len(rout):]
    return sequence


def create_input(routines:list, sequence:list, video_feed:bool=False) -> list:
    newline = ord('\n')
    main_routine = []
    for i in sequence:
        main_routine += [i + ord('A'), ord(',')]
    
    main_routine[-1] = newline
    input = main_routine
    for rout in routines:
        input += [ord(e) for e in rout[:-1]] + [newline]
    input += [ord('y')] if video_feed else [ord('n')]
    return input + [newline]
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 17, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    memory = read_from_file(args.input)
    path = find_path(memory)
    dust = move_robot(memory, path)
    print('Dust collected: {}'.format(dust))