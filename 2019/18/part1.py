import argparse
from typing import Union
from itertools import permutations
from collections import deque, defaultdict
from itertools import count


WALL = '#'
ENTRANCE = '@'
PASSAGE = '.'


def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]


# finds the shortest path to collect all keys
def collect_keys(tunnel_map:list) -> int:
    maze, poi = map_pois(tunnel_map)
    all_keys = set(filter(str.islower, poi.keys()))

    # paths from every key to every other key
    paths = map_paths_between_keys(maze, poi, all_keys)

    # paths from entrance to every key
    paths[ENTRANCE] = map_paths_from_point(maze, poi[ENTRANCE])
    return find_shortest_path(ENTRANCE, paths, all_keys, {})


# returns dict that maps positions to tile types and poi's to positions
def map_pois(tunnel_map:list) -> Union[dict, dict]:
    poi = {}
    maze = {}
    for y, row in enumerate(tunnel_map):
        for x, col in enumerate(row):
            pos = complex(x,y)
            maze[pos] = col
            if tunnel_map[y][x] not in {WALL, PASSAGE}:
                poi[tunnel_map[y][x]] = pos
    return maze, poi


# maps each key to the distance and doors encountered on the path to each of the other keys
def map_paths_between_keys(maze:dict, poi:dict, keys:dict) -> dict:
    paths = {}
    for key in keys:
        paths[key] = map_paths_from_point(maze, poi[key])
    return paths


# does a BFS to map a key to the distance and doors encountered on the path to each of the other keys
def map_paths_from_point(maze:dict, start:complex) -> dict:
    paths = {}
    queue = deque([(start, set(), 0)])
    walk = defaultdict(lambda:[float('inf'), set()])
    
    while queue:
        loc, doors, step = queue.popleft()
        cell = maze[loc]
        prev_steps, __ = walk[loc]
        # reached wall or a previously encountered cell in too many steps, no point continuing
        if cell == WALL or prev_steps <= step:
            continue
        # cell is a key, add path
        elif cell.islower():
            paths[cell] = (step, doors)
        # cell is a door, add to set
        elif cell.isupper():
            doors = doors | {cell.lower()}
        
        walk[loc] = (step, doors)
        
        # add each adjacent cell to the queue
        for d in [1,1j,-1,-1j]:
            queue.append((loc+d, doors, step+1))
    return paths


# recursively tries all key collection sequences and returns the one with the lowest overall distance
def find_shortest_path(start:str, paths:dict, missing_keys:set, key_cache:dict) -> int:
    if len(missing_keys) == 0:
        return 0
    
    # memoize to improve performance
    cache_key = (start, str(missing_keys))
    if cache_key in key_cache:
        return key_cache[cache_key]
    
    # continue collection sequence from each of the keys reachable from this point
    dist = float('inf')
    for key in missing_keys:
        # unreachable keys are filtered here, since they will return inf steps
        steps, doors = paths[start][key]

        # path is longer than current min, so skip
        if steps >= dist:
            continue
        
        # don't have keys for every door along the path, so skip
        if not doors.isdisjoint(missing_keys):
            continue
        
        t_dist = find_shortest_path(key, paths, missing_keys-{key}, key_cache)
        dist = min(dist, steps + t_dist)
    key_cache[cache_key] = dist
    return dist


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 18, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    tunnel_map = read_from_file(args.input)
    dist = collect_keys(tunnel_map)
    print(dist)