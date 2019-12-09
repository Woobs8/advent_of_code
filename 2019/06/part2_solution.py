import argparse
from collections import defaultdict, Counter


def read_from_file(fp):
    with open(fp) as f:
        return [line.strip() for line in f.readlines()]


# maps each object to its orbiting center (note the mapping is reversed compared to part 1)
def map_obj_to_com(orbit_map):
    orbits = defaultdict(str)
    for orbit_pair in orbit_map:
        center, in_orbit = orbit_pair.split(')')
        orbits[in_orbit] = center
    return orbits


# find the sequence of transfers required to reach a destination travelling in only one direction
def uni_dir_transfers(obj, dest, coms):
    if obj == dest:
        return []

    if not obj:
        raise RecursionError('Destination not reachable')
    
    transfers = [obj]
    transfers += uni_dir_transfers(coms[obj], dest, coms)
    return transfers


def transfers_to_reach(seq1, seq2, coms):
    seq1_transfers, seq2_transfers = get_first_common_element_idcs(seq1, seq2)
    return seq1_transfers + seq2_transfers


# find the indices of the first common element in two lists
def get_first_common_element_idcs(list1, list2):
    for i, obj1 in enumerate(list1):
        for j, obj2 in enumerate(list2):
            if obj1 == obj2:
                return i, j
    return None, None



if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 6, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    orbit_map = read_from_file(args.input)
    coms = map_obj_to_com(orbit_map)
    you_to_com = uni_dir_transfers(coms['YOU'], 'COM', coms)
    san_to_com = uni_dir_transfers(coms['SAN'], 'COM', coms)

    # compute the transfers required to reach SAN from YOU as the sum of transfers required to reach the first object reachable by both
    transfers = transfers_to_reach(you_to_com, san_to_com, coms)
    print(transfers)