import argparse
from itertools import product


ASTEROID = '#'
SPACE = '.'

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]


def get_asteroid_locations(asteroid_map:list) -> list:
    asteroids = []
    for y in range(len(asteroid_map)):
        for x in range(len(asteroid_map[y])):
            if asteroid_map[y][x] == ASTEROID:
                asteroids.append([x,y])
    return asteroids


# determines the asteroids in view from a specific point
def asteroids_in_view(x:int, y:int, asteroid_map:list) -> set:
    in_view = set()
    map_dims = [len(asteroid_map[0]), len(asteroid_map)]
    blocked = set()

    # iterate every possible direction
    for x_step, y_step in product(range(-(map_dims[0]-1), map_dims[1]), repeat=2):
        
        # ignore case where direction is 0 along both axes since it will cause an endless loop
        if x_step == 0 and y_step == 0:
            continue
        
        loc = [x,y]
        los_blocked = False
        
        # loop while location is within the map borders
        while loc[0] >= 0 and loc[0] < map_dims[0] and loc[1] >= 0 and loc[1] < map_dims[1]:
            # LoS is blocked by a closer asteroid
            if los_blocked:
                blocked.add((loc[0], loc[1]))
            
            if asteroid_map[loc[1]][loc[0]] == ASTEROID and loc != [x,y] and (loc[0], loc[1]) not in blocked:
                in_view.add((loc[0], loc[1]))
                los_blocked = True
            
            loc[0] += x_step
            loc[1] += y_step
    return in_view-blocked


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 10, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    asteroid_map = read_from_file(args.input)
    asteroids = get_asteroid_locations(asteroid_map)
    in_view = list(map(lambda loc: len(asteroids_in_view(loc[0], loc[1], asteroid_map)), asteroids))
    max_asteroids_in_view = max(in_view)
    station_loc = asteroids[in_view.index(max_asteroids_in_view)]
    print('Station loc {} with {} asteroids in view'.format(station_loc, max_asteroids_in_view))