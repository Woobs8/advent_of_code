import argparse
from typing import Union
from functools import reduce

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


# simulate the state of a systems of moons for a specified number of steps
def simulate_moons(moon_positions:list, steps:int) -> Union[list, list]:
    velocities = [[0]*3 for __ in range(len(moon_positions))]

    for step in range(steps):
        velocities = apply_gravity(moon_positions, velocities)
        moon_positions = list(map(lambda x: move_moon(x[0], x[1]), zip(moon_positions, velocities)))
    return moon_positions, velocities


# apply the effects of gravity on velocities
def apply_gravity(moon_positions:list, velocities:list) -> list:
    new_velocities = velocities.copy()
    
    # naive approach: iterate all dimensions and combinations of moons
    for dim in range(3):
        moons = sorted(moon_positions, key=lambda x: x[dim])
        for m1 in range(len(new_velocities)):
            delta_velocity = 0
            for m2 in range(len(new_velocities)):
                if m1 == m2:
                    continue

                if moons[m1][dim] > moons[m2][dim]:
                    delta_velocity -= 1
                elif moons[m1][dim] < moons[m2][dim]:
                    delta_velocity += 1
            new_velocities[moons[m1][3]][dim] += delta_velocity
    return new_velocities              


# update the position of a moon based on its velocity
def move_moon(position:list, velocity:list) -> list:
    new_pos = position.copy()
    for i in range(3):
        new_pos[i] += velocity[i]
    return new_pos


# calculate the total energy of a system of moons
def calc_total_energy(moon_positions:list, velocities:list) -> int:
    potential_energy = map(lambda x: sum([abs(e) for e in x[:3]]), moon_positions)
    kinetic_energy = map(lambda x: sum([abs(e) for e in x]), velocities)
    return reduce(lambda x, y: y[0]*y[1]+x, zip(potential_energy, kinetic_energy), 0)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 12, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    moon_positions = read_from_file(args.input)
    final_moon_postions, velocities = simulate_moons(moon_positions, 1000)
    print(calc_total_energy(final_moon_postions, velocities))
    