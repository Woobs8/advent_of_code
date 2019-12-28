import argparse
from collections import defaultdict
from copy import deepcopy


BUG = '#'
EMPTY = '.'
RECURSION = '?'


def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return [list(line.strip('\n')) for line in f.readlines()]


def observe_bugs(initial_state:list, steps:int) -> int:
    layout, height, width = map_layout(initial_state)
    state = defaultdict(lambda: {complex(x,y):EMPTY for x in range(width) for y in range(height)})
    state[0] = layout
    for i in range(steps):
        state = advance_time(state, height, width)
    return count_bugs(state, height, width)


def map_layout(lines:list) -> Union[dict, int, int]:
    layout = {}
    for y, row in enumerate(lines):
        for x, col in enumerate(row):
            pos = complex(x,y)
            layout[pos] = col
    return layout, len(lines), len(lines[0])


def advance_time(state:dict, h:int, w:int) -> dict:
    next_state = deepcopy(state)

    # update currently existing levels
    for level in list(state.keys()):
        next_state[level] = update_level(state, level, h, w)
    
    # add a recursive parent level
    min_level = min(state.keys())
    next_state[min_level] = update_level(state, min_level, h, w)

    # add a recursive child level
    max_level = max(state.keys())
    next_state[max_level] = update_level(state, max_level, h, w)
    return next_state


def update_level(state:dict, level:int, h:int, w:int) -> dict:
    next_level_state = deepcopy(state[level])
    centre = complex(w//2, h//2)
    for y in range(h):
        for x in range(w):
            pos = complex(x,y)
            if pos == centre:
                next_level_state[pos] = RECURSION
                continue
            col = state[level][pos]
            adj_bugs = adjacent_bugs(state, h, w, x, y, level)
            if col == BUG and adj_bugs != 1:
                next_level_state[pos] = EMPTY
            elif col == EMPTY and (adj_bugs == 1 or adj_bugs == 2):
                next_level_state[pos] = BUG
    return next_level_state


def adjacent_bugs(state:dict, h:int, w:int, x:int, y:int, z:int) -> int:
    bugs = 0
    centre = complex(w//2, h//2)
    for d in [1, -1, 1j, -1j]:
        adj_pos = complex(x,y) + d
        # adjacent tile is in child level
        if adj_pos == centre:
            child_state = state[z+1]
            # adjacent to right edge of child level
            if d == -1:
                x_range = [w-1]
                y_range = range(h)        
            # adjacent to left edge of child level
            elif d == 1:
                x_range = [0]
                y_range = range(h)
            # adjacent to bottom edge of child level
            elif d == -1j:
                x_range = range(w)
                y_range = [h-1]
            # adjacent to top edge of child level
            else:
                x_range = range(w)
                y_range = [0]
            
            for cy in y_range:
                for cx in x_range:
                    bugs += 1 if child_state[complex(cx, cy)] == BUG else 0
        
        # adjacent tile is left edge of parent level
        elif adj_pos.real == -1:
            bugs += 1 if state[z-1][centre-1] == BUG else 0
        # adjacent tile is right edge of parent level
        elif adj_pos.real == w:
            bugs += 1 if state[z-1][centre+1] == BUG else 0
        # adjacent tile is top edge of parent level
        elif adj_pos.imag == -1:
            bugs += 1 if state[z-1][centre-1j] == BUG else 0
        # adjacent tile is bottom edge of parent level
        elif adj_pos.imag == h:
            bugs += 1 if state[z-1][centre+1j] == BUG else 0
        # adjacent tile is in current level
        else:
            bugs += 1 if state[z][adj_pos] == BUG else 0
    return bugs
    

def count_bugs(state:dict, h:int, w:int) -> int:
    bugs = 0
    for level in state.keys():
        for y in range(h):
            for x in range(w):
                bugs += 1 if state[level][complex(x,y)] == BUG else 0
    return bugs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 24, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    lines = read_from_file(args.input)
    bugs = observe_bugs(lines, 200)
    print(bugs)
