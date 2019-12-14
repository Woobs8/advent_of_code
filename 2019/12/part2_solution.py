import argparse
from typing import Union
from functools import reduce
from fractions import gcd

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        unparsed = [line.strip() for line in f.readlines()]
    return parse_moon_positions(unparsed)


def parse_moon_positions(unparsed_strings:list) -> list:
    # each position contains the x,y,z coords and the original index of the moon
    parsed_positions = [[0]*4 for __ in range(len(unparsed_strings))]
    no_brackets = str.maketrans("", "", "<>")
    for i, line in enumerate(unparsed_strings):
        line = line.translate(no_brackets)
        coords = line.split(',')
        for dim in coords:
            dim = dim.strip().split('=')
            if dim[0] == 'x':
                axis = 0
            elif dim[0] == 'y':
                axis = 1
            elif dim[0] == 'z':
                axis = 2
            parsed_positions[i][axis] = int(dim[1])
        parsed_positions[i][3] = i
    return parsed_positions


# simulate the state of a systems of moons in 1D until its state repeats itself
def simulate_moons_in_1D_until_repeat(moon_positions, dim):
    moon_pos_in_dim = [[pos[dim], pos[3]] for pos in moon_positions]
    steps = 0
    velocity_in_dim = [0]*len(moon_pos_in_dim)
    initial_state = (moon_pos_in_dim, velocity_in_dim)
    state = None
    while state != initial_state:
        steps += 1
        velocity_in_dim = apply_gravity_in_1D(moon_pos_in_dim, velocity_in_dim)
        moon_pos_in_dim = list(map(lambda x: move_moon_in_1D(x[0], x[1]), zip(moon_pos_in_dim, velocity_in_dim)))
        state = (moon_pos_in_dim, velocity_in_dim)
    return steps


# apply the effects of gravity on velocities in 1D
def apply_gravity_in_1D(moon_positions:list, velocities:list) -> list:
    new_velocities = velocities.copy()
    moons = sorted(moon_positions, key=lambda x: x[0])
    for m1 in range(len(new_velocities)):
        delta_velocity = 0
        for m2 in range(len(new_velocities)):
            if m1 == m2:
                continue

            if moons[m1][0] > moons[m2][0]:
                delta_velocity -= 1
            elif moons[m1][0] < moons[m2][0]:
                delta_velocity += 1
        new_velocities[moons[m1][1]] += delta_velocity
    return new_velocities              


# update the position of a moon based on its velocity
def move_moon_in_1D(position:list, velocity:list) -> list:
    new_pos = position.copy()
    new_pos[0] += velocity
    return new_pos


# calculate the period of the state of the "universe" - ie. the steps before it repeats it self
def find_period_of_repetetion(moon_positions:list) -> int:
    x_period = simulate_moons_in_1D_until_repeat(moon_positions, 0)
    y_period = simulate_moons_in_1D_until_repeat(moon_positions, 1)
    z_period = simulate_moons_in_1D_until_repeat(moon_positions, 2)

    # the period of repetition of a composite state is the lcm of the periods of each individual state
    return lcmm(x_period, y_period, z_period)


# lcm of an arbitrary number of integers
def lcmm(*args) -> int:
    return reduce(lcm, args)


# the lcm (Lowest-Common-Multiple) between two integers
def lcm(a:int, b:int):
    return abs(a*b) // gcd(a, b)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 12, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    moon_positions = read_from_file(args.input)
    print(find_period_of_repetetion(moon_positions))
    