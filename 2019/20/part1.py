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
    for y, row in enumerate(maze_map):
        for x, col in enumerate(row):
            pos = complex(x,y)
            maze[pos] = col

            # find portal pairs
            if maze_map[y][x] == PASSAGE:
                if y-1 >= 0 and maze_map[y-1][x].isupper():
                    portal_id = frozenset({maze_map[y-1][x], maze_map[y-2][x]})
                elif y+1 < len(maze_map) and maze_map[y+1][x].isupper():
                    portal_id = frozenset({maze_map[y+1][x], maze_map[y+2][x]})
                elif x-1 >= 0 and maze_map[y][x-1].isupper():
                    portal_id = frozenset({maze_map[y][x-1], maze_map[y][x-2]})
                elif x+1 < len(row) and maze_map[y][x+1].isupper():
                    portal_id = frozenset({maze_map[y][x+1], maze_map[y][x+2]})
                else:
                    portal_id = None
                
                if portal_id:
                    portal_pairs[portal_id].append(pos)

    # create mapping between coordinates of portal pairs
    portals = {}
    for k, v in portal_pairs.items():
        if len(v) == 2:
            portals[v[0]] = v[1]
            portals[v[1]] = v[0]
        elif 'A' in k:
            start = v[0]
        elif 'Z' in k:
            finish = v[0]

    return maze, portals, start, finish


# BFS traversal of maze
def traverse_maze(maze:dict, portals:dict, start:complex, finish:complex) -> int:
    visited = set()
    step = 0
    queue = deque()
    queue.append((start, step))
    while queue:
        pos, step = queue.popleft()
        if pos in visited:
            continue
        visited.add(pos)

        loc = maze[pos]
        if pos == finish:
            break
        elif loc == WALL:
            continue
        elif loc == PASSAGE:
            for s in [1, -1, 1j, -1j]:
                queue.append((pos+s, step+1))

        if pos in portals.keys():
            queue.append((portals[pos], step+1))
    
    return step


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 20, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    maze_map = read_from_file(args.input)
    maze, portals, start, finish = map_maze(maze_map)
    steps = traverse_maze(maze, portals, start, finish)
    print(steps)