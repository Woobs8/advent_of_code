import argparse
from collections import defaultdict, Counter


def read_from_file(fp):
    with open(fp) as f:
        return [line.strip() for line in f.readlines()]


# maps each object to a list of its orbiting objects
def map_com_to_orbits(orbit_map):
    orbits = defaultdict(list)
    for orbit_pair in orbit_map:
        center, in_orbit = orbit_pair.split(')')
        orbits[center].append(in_orbit)
    return orbits


def count_all_orbits(dir_orbits):
    all_orbits = defaultdict(lambda:-1)
    com_orbits = count_indirect_orbits('COM', direct_orbits, all_orbits)
    return com_orbits + sum(all_orbits.values())


# recursively find the indirect orbits of objects
def count_indirect_orbits(com, dir_orbits, all_orbits):
    orbit = dir_orbits[com]
    if not orbit:
        return 0

    orbit_count = 0
    for obj in orbit:
        # check if indirect orbits have already been calculated
        if all_orbits[obj] == -1:
            all_orbits[obj] = count_indirect_orbits(obj, dir_orbits, all_orbits)
        orbit_count += all_orbits[obj]+1
    return orbit_count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 6, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    orbit_map = read_from_file(args.input)
    direct_orbits = map_com_to_orbits(orbit_map)
    orbit_count = count_all_orbits(direct_orbits)
    print(orbit_count)