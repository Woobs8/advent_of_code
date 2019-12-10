import argparse
from itertools import product
import math
from functools import partial


ASTEROID = '#'
SPACE = '.'
STATION = (19,14)

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]


# vaporize asteroids until count is reached
def vaporize(asteroid_map:list, count:int, laser_loc:list) -> list:
    vaporized_asteroids = []

    while len(vaporized_asteroids) < count:
        in_view = asteroids_in_view(laser_loc[0], laser_loc[1], asteroid_map)
        order = vaporize_order(asteroid_map, in_view, laser_loc)

        for x, y in order:
            asteroid_map[y][x] = SPACE

        vaporized_asteroids += order
    return vaporized_asteroids[:count]


# determines the order asteroids will be vaporized in from the angles between the vector and the laser
def vaporize_order(asteroid_map:list, in_view:list, laser_loc:list) -> list:
    in_view_vectors = [[x-laser_loc[0], y-laser_loc[1]] for x, y in in_view]
    return [x for _,x in sorted(zip(map(partial(clockwise_angle, start_vec=[0,-1]), in_view_vectors),in_view))]


# calculates the angle between an arbitrary vector and the vector representing the direction of the laser at the start of a rotation
def clockwise_angle(vec:list, start_vec:list) -> float:
    vec_angle = angle(start_vec, vec)
    if vec[0]-start_vec[0] < 0:
        vec_angle = 360 - vec_angle
    return vec_angle

    
def angle(v1:list, v2:list) -> float:
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))


def dotproduct(v1:list, v2:list) -> float:
    return sum((a*b) for a, b in zip(v1, v2))


def length(v:list) -> float:
  return math.sqrt(dotproduct(v, v))


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
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 10, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    asteroid_map = read_from_file(args.input)
    vaporized_asteroids = vaporize(asteroid_map, 200, [STATION[0], STATION[1]])
    last = vaporized_asteroids[-1]
    print(last[0]*100 + last[1])