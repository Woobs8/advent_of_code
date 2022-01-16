import argparse
from collections import defaultdict
from math import inf
from copy import deepcopy
from itertools import chain


DESTINATIONS = {'A': [(3,2), (3,3)], 'B': [(5,2), (5,3)], 'C':[(7,2), (7,3)], 'D':[(9,2), (9,3)]}
ROOMS = {(3,2):(3,3), (3,3):(3,2), (5,2):(5,3), (5,3):(5,2), (7,2):(7,3), (7,3):(7,2), (9,2):(9,3), (9,2):(9,3)}
ENERGY = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
TARGET = 'A0302A0303B0502B0503C0702C0703D0902D0903'

STEP0 = 'A0303A0903B0302B0702C0502C0703D0503D0902'
STEP1 = 'A0303A0903B0302B0401C0502C0703D0503D0902'
STEP2 = 'A0303A0903B0302B0401C0702C0703D0503D0902'
STEP3 = 'A0303A0903B0302B0401C0702C0703D0601D0902'
STEP4 = 'A0303A0903B0302B0503C0702C0703D0601D0902'
STEP5 = 'A0303A0903B0502B0503C0702C0703D0601D0902'
STEP6 = 'A0303A0903B0502B0503C0702C0703D0601D0801'
STEP7 = 'A0303A1001B0502B0503C0702C0703D0601D0801'
STEP8 = 'A0303A1001B0502B0503C0702C0703D0601D0903'
STEP9 = 'A0303A1001B0502B0503C0702C0703D0902D0903'
STEP9 = 'A0303A0302B0502B0503C0702C0703D0902D0903'


def read_from_file(fp:str) -> (dict, dict):
    with open(fp, 'r') as f:
        burrow = defaultdict(list)
        amphipods = defaultdict(list)
        lines = f.read().splitlines()
        for r, line in enumerate(lines):
            for c, element in enumerate(line):
                if element != '#':
                    for ri,ci in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
                        if 0 <= ri < len(lines) and 0 <= ci < len(line) and lines[ri][ci] != '#':
                            burrow[(c, r)].append((ci, ri))
                if element in ['A', 'B', 'C', 'D']:
                    amphipods[element].append((c,r))
    return burrow, amphipods 

def organize(burrow: dict, amphipods: dict) -> int:
    energy_required = defaultdict(lambda: inf)
    initital_config = serialize_configuration(amphipods)
    energy_required[initital_config] = 0
    configurations = [initital_config]
    while len(configurations) > 0:
        serial_config = configurations.pop()
        if serial_config != TARGET:
            config = deserialize_configuration(serial_config)
            for a, locations in config.items():
                for l in locations:
                    valid_next_configurations = get_valid_next_configurations(l, a, burrow, config)
                    for next_config, cost in valid_next_configurations:
                        serialized = serialize_configuration(next_config)
                        total_cost = energy_required[serial_config] + cost
                        if total_cost < energy_required[serialized]:
                            configurations.append(serialized)
                            energy_required[serialized] = total_cost
                            print(serialized)
                            
    return energy_required[TARGET]

def get_valid_next_configurations(location: tuple, amphipod_type: str, burrow: dict, configuration: dict) -> list:
    # the amphipod is at the back of its destination room or both of its type are in their destination room
    if location == DESTINATIONS[amphipod_type][1] or all([a in DESTINATIONS[amphipod_type] for a in configuration[amphipod_type]]):
        return []
    valid_configurations = []
    valid_targets = get_valid_targets(location, amphipod_type, burrow, configuration)
    for target, steps in valid_targets:
        new_configuration = deepcopy(configuration)
        new_configuration[amphipod_type]
        new_configuration[amphipod_type].remove(location)
        new_configuration[amphipod_type].append(target)
        cost = steps * ENERGY[amphipod_type]
        valid_configurations.append((new_configuration, cost))
    return valid_configurations

def get_valid_targets(location: tuple, amphipod_type: str, burrow: dict, configuration: dict) -> list:
    visited = []
    nodes = [(location, 0)]
    valid_targets = []
    while len(nodes) > 0:
        curr, steps = nodes.pop()
        if not curr in visited:
            visited.append(curr)
            for node in burrow[curr]:
                # space can't be occupied by another amphipod, 
                if node not in list(chain.from_iterable(configuration.values())):
                    nodes.append((node, steps + 1))
                    if can_move_into_hallway(location, node, burrow) or can_move_into_room(node, amphipod_type):
                        valid_targets.append((node, steps + 1))
    return valid_targets

# amphipods can only move into hallways if they start in a room don't end in front of a room
def can_move_into_hallway(start: tuple, stop: tuple, burrow: dict) -> bool:
    return start in ROOMS.keys() and (not stop in ROOMS.keys() and all([not adj in ROOMS.keys() for adj in burrow[stop]]))

# amphipods can only move into a room if that room is their destination
def can_move_into_room(stop: tuple, amphipod_type: str) -> bool:
    return stop in DESTINATIONS[amphipod_type]

def serialize_configuration(configuration: dict) -> str:
    serialized_configuration = ''
    for type in ['A', 'B', 'C', 'D']:
        for amphipod in sorted(configuration[type], key=lambda element: (element[0], element[1])):
            serialized_configuration += type + str(amphipod[0]).zfill(2) + str(amphipod[1]).zfill(2)
    return serialized_configuration

def deserialize_configuration(configuration: str) -> dict:
    deserialized_configuration = defaultdict(list)
    for i in range(0, len(configuration), 5):
        amphipod = configuration[i:i+5]
        type = amphipod[0]
        x = int(amphipod[1:3])
        y = int(amphipod[3:5])
        deserialized_configuration[type].append((x,y))
    return deserialized_configuration

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 23, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    burrow, amphipods = read_from_file(args.input)
    energy_required = organize(burrow, amphipods)
    print(energy_required)