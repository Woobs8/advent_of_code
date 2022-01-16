import argparse
from collections import namedtuple
from operator import le as leq

Coordinate = namedtuple("Coordinate", "x y z")
Cube = namedtuple("Cube", "min max")
Step = namedtuple("Step", "action cube")

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        steps = []
        for line in f.read().splitlines():
            action, coordinates = line.split()
            x, y, z = coordinates.split(',')
            x_min, x_max = create_interval(x)
            y_min, y_max = create_interval(y)
            z_min, z_max = create_interval(z)
            cube_min = Coordinate(x_min, y_min, z_min)
            cube_max = Coordinate(x_max, y_max, z_max)
            cube = Cube(cube_min, cube_max)
            step = Step(action, cube)
            steps.append(step)
    return steps

def create_interval(str_internal: str) -> list:
    start, stop = [int(num) for num in str_internal[2:].split('..')]
    return [min(start, stop), max(start, stop)]

def execute_reboot(steps: list) -> list:
    on = []
    for action, new_cube in steps:
        new_on = []
        for old_cube in on:
            intersect = all(map(leq, new_cube.min, old_cube.max)) and all(map(leq, old_cube.min, new_cube.max))
            if not intersect:
                new_on += [old_cube]
                continue
            #       |--- old ---|
            #       ******* (delete)
            # |--- new ---|
            if old_cube.min.x <= new_cube.max.x <= old_cube.max.x:
                new_on += [Cube(Coordinate(new_cube.max.x+1, old_cube.min.y, old_cube.min.z), Coordinate(old_cube.max.x, old_cube.max.y, old_cube.max.z))]
                old_cube = Cube(Coordinate(old_cube.min.x, old_cube.min.y, old_cube.min.z), Coordinate(new_cube.max.x, old_cube.max.y, old_cube.max.z))

            # |--- old ---|
            #       ******* (delete)
            #       |--- new ---|
            if old_cube.min.x <= new_cube.min.x <= old_cube.max.x:
                new_on += [Cube(Coordinate(old_cube.min.x, old_cube.min.y, old_cube.min.z), Coordinate(new_cube.min.x-1, old_cube.max.y, old_cube.max.z))]
                old_cube = Cube(Coordinate(new_cube.min.x, old_cube.min.y, old_cube.min.z), Coordinate(old_cube.max.x, old_cube.max.y, old_cube.max.z))
            #       |--- old ---|
            #       ******* (delete)
            # |--- new ---|
            if old_cube.min.y <= new_cube.max.y <= old_cube.max.y:
                new_on += [Cube(Coordinate(old_cube.min.x, new_cube.max.y+1, old_cube.min.z), Coordinate(old_cube.max.x, old_cube.max.y, old_cube.max.z))]
                old_cube = Cube(Coordinate(old_cube.min.x, old_cube.min.y, old_cube.min.z), Coordinate(old_cube.max.x, new_cube.max.y, old_cube.max.z))
            # |--- old ---|
            #       ******* (delete)
            #       |--- new ---|
            if old_cube.min.y <= new_cube.min.y <= old_cube.max.y:
                new_on += [Cube(Coordinate(old_cube.min.x, old_cube.min.y, old_cube.min.z), Coordinate(old_cube.max.x, new_cube.min.y-1, old_cube.max.z))]
                old_cube = Cube(Coordinate(old_cube.min.x, new_cube.min.y, old_cube.min.z), Coordinate(old_cube.max.x, old_cube.max.y, old_cube.max.z))
            #       |--- old ---|
            #       ******* (delete)
            # |--- new ---|
            if old_cube.min.z <= new_cube.max.z <= old_cube.max.z:
                new_on += [Cube(Coordinate(old_cube.min.x, old_cube.min.y, new_cube.max.z+1), Coordinate(old_cube.max.x, old_cube.max.y, old_cube.max.z))]
                old_cube = Cube(Coordinate(old_cube.min.x, old_cube.min.y, old_cube.min.z), Coordinate(old_cube.max.x, old_cube.max.y, new_cube.max.z))
            # |--- old ---|
            #       ******* (delete)
            #       |--- new ---|
            if old_cube.min.z <= new_cube.min.z <= old_cube.max.z:
                new_on += [Cube(Coordinate(old_cube.min.x, old_cube.min.y, old_cube.min.z), Coordinate(old_cube.max.x, old_cube.max.y, new_cube.min.z-1))]
                old_cube = Cube(Coordinate(old_cube.min.x, old_cube.min.y, new_cube.min.z), Coordinate(old_cube.max.x, old_cube.max.y, old_cube.max.z))
        if action == "on": 
            new_on += [new_cube]
        on = new_on 
    return on

def calc_volume(cubes: list) -> int:
    volume = 0
    for cube in cubes:
        volume += (cube.max.x - cube.min.x + 1) * (cube.max.y - cube.min.y + 1) * (cube.max.z - cube.min.z + 1)
    return volume

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 22, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    steps = read_from_file(args.input)
    on = execute_reboot(steps)
    volume = calc_volume(on)
    print(volume)