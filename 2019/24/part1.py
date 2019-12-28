import argparse
from collections import Counter
from copy import deepcopy

BUG = '#'
EMPTY = '.'


def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return [list(line.strip('\n')) for line in f.readlines()]


def observe_bugs(state:list) -> int:
    biodiversity = {}
    state_tracker = Counter()
    
    while True:
        state_repr = binary_string_repr(state)
        biodiversity[state_repr] = calc_biodiversity(state)
        state_tracker[state_repr] += 1
        if state_tracker[state_repr] == 2:
            return biodiversity[state_repr]
        state = advance_time(state)


def binary_string_repr(state:list) -> str:
    str_repr = ""
    for y, row in enumerate(state):
        for x, col in enumerate(row):
            str_repr += '1' if col == BUG else '0'
    return str_repr


def advance_time(state:list) -> list:
    next_state = deepcopy(state)
    for y, row in enumerate(state):
        for x, col in enumerate(row):
            adj_bugs = adjacent_bugs(state, x, y)
            if col == BUG and adj_bugs != 1:
                next_state[y][x] = EMPTY
            elif col == EMPTY and (adj_bugs == 1 or adj_bugs == 2):
                next_state[y][x] = BUG
    return next_state


def adjacent_bugs(state:list, x:int, y:int) -> int:
    bugs = 0
    if x-1 >= 0:
        bugs += 1 if state[y][x-1] == BUG else 0
    
    if x+1 < len(state[0]):
        bugs += 1 if state[y][x+1] == BUG else 0
    
    if y-1 >= 0:
        bugs += 1 if state[y-1][x] == BUG else 0
    
    if y+1 < len(state):
        bugs += 1 if state[y+1][x] == BUG else 0
    return bugs


def calc_biodiversity(state:list) -> int:
    biodiversity = 0
    for y, row in enumerate(state):
        for x, col in enumerate(row, y*len(row)):
            biodiversity += 2**x if col == BUG else 0
    return biodiversity


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 24, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    lines = read_from_file(args.input)
    biodiversity = observe_bugs(lines)
    print(biodiversity)
