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
    update_map(maze, poi)
    all_keys = set(filter(str.islower, poi.keys()))

    # paths from every key to every other key (some will be unreachable)
    paths = map_paths_between_keys(maze, poi, all_keys)

    # paths from each of the four entrances to every key (some will be unreachable)
    for i in range(1,5):
        paths[ENTRANCE+str(i)] = map_paths_from_point(maze, poi[ENTRANCE+str(i)])
    return find_shortest_path({ENTRANCE+str(i) for i in range(1,5)}, paths, all_keys, {})


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


# update the map and split it into four separate maps
def update_map(maze:dict, poi:dict) -> dict:
    entrance = poi[ENTRANCE]

    for i, d in enumerate([-1-1j, -1+1j, 1-1j, 1+1j], 1):
        maze[entrance+d] = ENTRANCE + str(i)
        poi[ENTRANCE + str(i)] = entrance+d

    for d in [0, -1, 1, -1j, 1j]:
        maze[entrance+d] = WALL
        if entrance+d in poi:
            del poi[entrance+d]


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


# recursively finds the shortest path that collects all keys
def find_shortest_path(start_points:set, paths:dict, missing_keys:set, key_cache:dict) -> int:
    if len(missing_keys) == 0:
        return 0
    
    # memoize to improve performance
    cache_key = (str(start_points), str(missing_keys))
    if cache_key in key_cache:
        return key_cache[cache_key]
    
    # continue collection sequence from each of the keys reachable from this point
    dist = float('inf')
    for k1 in missing_keys:
        # try to find a path from the current location in each section of the maze to find the one where the key is reachable
        for k2 in start_points:
            # key can't be found from this key
            if k1 not in paths[k2]:
                continue
            
            # unreachable keys are filtered here, since they will return inf steps
            steps, doors = paths[k2][k1]

            # path is longer than current min, so skip
            if steps >= dist:
                continue
            
            # don't have keys for every door along the path, so skip
            if not doors.isdisjoint(missing_keys):
                continue
            
            # the location k2 is moved to k1 and the collection continues
            t_dist = find_shortest_path((start_points-{k2}) | {k1}, paths, missing_keys-{k1}, key_cache)
            dist = min(dist, steps + t_dist)
    key_cache[cache_key] = dist
    return dist


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 18, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    tunnel_map = read_from_file(args.input)
    dist = collect_keys(tunnel_map)
    print(dist)