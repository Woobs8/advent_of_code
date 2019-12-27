import argparse
from typing import Union
from collections import deque, defaultdict


WALL = '#'
PASSAGE = '.'


def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return [list(line.strip('\n')) for line in f.readlines()]


def map_maze(maze_map:list) -> Union[dict, dict, int, int]:
    portal_pairs = defaultdict(lambda: [])
    maze = {}
    inner_x = []
    inner_y = []
    for y, row in enumerate(maze_map):
        for x, col in enumerate(row):
            pos = complex(x,y)
            maze[pos] = col

            # find portal pairs and inner ring boundary
            if maze_map[y][x] == PASSAGE:
                if y-1 >= 0 and maze_map[y-1][x].isupper():
                    portal_id = frozenset({maze_map[y-1][x], maze_map[y-2][x]})
                    
                    if len(inner_y) == 1:
                        inner_y.append(y)
                
                elif y+1 < len(maze_map) and maze_map[y+1][x].isupper():
                    portal_id = frozenset({maze_map[y+1][x], maze_map[y+2][x]})
                    if not inner_y:
                        inner_y.append(y)
                
                elif x-1 >= 0 and maze_map[y][x-1].isupper():
                    portal_id = frozenset({maze_map[y][x-1], maze_map[y][x-2]})
                    
                    if len(inner_x) == 1:
                        inner_x.append(x)
                
                elif x+1 < len(row) and maze_map[y][x+1].isupper():
                    portal_id = frozenset({maze_map[y][x+1], maze_map[y][x+2]})

                    if not inner_x:
                        inner_x.append(x)

                else:
                    portal_id = None
                
                if portal_id:
                    portal_pairs[portal_id].append(pos)

    # find inner ring boundary that innter portals must be located on
    inner_x_boundary = range(inner_x[0], inner_x[1]+1)
    inner_y_boundary = range(inner_y[0], inner_y[1]+1)

    # create mapping between coordinates of portal pairs
    portals = {}
    for k, v in portal_pairs.items():
        if len(v) == 2:
            # the first portal is the inner portal
            if v[0].real in inner_x_boundary and v[0].imag in inner_y_boundary:
                portals[v[0]] = (v[1], 1)
                portals[v[1]] = (v[0], -1)
            # the second portal is the inner portal
            else:
                portals[v[0]] = (v[1], -1)
                portals[v[1]] = (v[0], 1)
        elif len(k) == 1 and 'A' in k:
            start = v[0]
        elif len(k) == 1 and 'Z' in k:
            finish = v[0]

    return maze, portals, start, finish    


# BFS traversal of maze
def traverse_maze(maze:dict, portals:dict, start:complex, finish:complex) -> int:
    visited = set()
    step = 0
    level = 0
    queue = deque()
    queue.append((start, step, level))
    while queue:
        pos, step, level = queue.popleft()
        if (pos, level) in visited:
            continue
        visited.add((pos, level))

        loc = maze[pos]
        if pos == finish and level == 0:
            break
        elif loc == WALL:
            continue
        elif loc == PASSAGE:
            for s in [1, -1, 1j, -1j]:
                queue.append((pos+s, step+1, level))

        if pos in portals.keys():
            n_pos, d_level = portals[pos]

            # outer portals do not work in the outer level (0)
            if level != 0 or (level == 0 and d_level > 0):
                queue.append((n_pos, step+1, level + d_level))
    return step


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 20, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    maze_map = read_from_file(args.input)
    maze, portals, start, finish = map_maze(maze_map)
    steps = traverse_maze(maze, portals, start, finish)
    print(steps)