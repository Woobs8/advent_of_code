import argparse
from itertools import product

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        commands = []
        for line in f.read().splitlines():
            action, coordinates = line.split()
            x, y, z = coordinates.split(',')
            x_interval = create_interval(x)
            y_interval = create_interval(y)
            z_interval = create_interval(z)
            command = [action, x_interval, y_interval, z_interval]
            commands.append(command)
    return commands

def create_interval(str_internal: str) -> list:
    start, stop = [int(num) for num in str_internal[2:].split('..')]
    return [min(start, stop), max(start, stop)]

def execute_reboot(commands: list, x_limit: int, y_limit: int, z_limit: int) -> dict:
    cubes = {}
    for command in commands:
        state = 1 if command[0] == 'on' else 0
        if x_limit[0] <= command[1][0] and command[1][1] <= x_limit[1] and y_limit[0] <= command[2][0] and command[2][1] <= y_limit[1] and z_limit[0] <= command[3][0] and command[3][1] <= z_limit[1]:
            for x, y, z in product(range(command[1][0], command[1][1] + 1), range(command[2][0], command[2][1] + 1), range(command[3][0], command[3][1] + 1)):
                cubes[(x,y,z)] = state
    return cubes

def count_cubes(cubes: dict, state: int) -> int:
    return list(cubes.values()).count(state)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 22, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    commands = read_from_file(args.input)
    cubes = execute_reboot(commands, [-50, 50], [-50, 50], [-50, 50])
    on = count_cubes(cubes, 1)
    print(on)