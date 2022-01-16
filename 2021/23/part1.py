import argparse
from collections import defaultdict, namedtuple
from queue import PriorityQueue
from math import inf
from copy import deepcopy
from itertools import chain

Coordinate = namedtuple("Coordinate", "x y")
Vertice = namedtuple("Vertice", "configuration cost")
DESTINATIONS = {'A': [Coordinate(3,2), Coordinate(3,3)], 'B': [Coordinate(5,2), Coordinate(5,3)], 'C':[Coordinate(7,2), Coordinate(7,3)], 'D':[Coordinate(9,2), Coordinate(9,3)]}
ROOMS = {Coordinate(3,2):Coordinate(3,3), Coordinate(3,3):Coordinate(3,2), Coordinate(5,2):Coordinate(5,3), Coordinate(5,3):Coordinate(5,2), Coordinate(7,2):Coordinate(7,3), Coordinate(7,3):Coordinate(7,2), Coordinate(9,2):Coordinate(9,3), Coordinate(9,2):Coordinate(9,3)}
ENERGY_COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
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

def read_from_file(fp: str) -> (dict, dict):
    with open(fp, 'r') as f:
        burrow = defaultdict(list)
        amphipods = defaultdict(list)
        lines = f.read().splitlines()
        for r, line in enumerate(lines):
            for c, element in enumerate(line):
                if element != '#':
                    for ri,ci in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
                        if 0 <= ri < len(lines) and 0 <= ci < len(line) and lines[ri][ci] != '#':
                            burrow[Coordinate(c, r)].append(Coordinate(ci, ri))
                if element in ['A', 'B', 'C', 'D']:
                    amphipods[element].append(Coordinate(c,r))
    return burrow, amphipods 

def create_graph(burrow: dict, amphipods: dict) -> dict:
    configuration_graph = defaultdict(set)
    configurations = [amphipods]
    visited = set()
    while len(configurations) > 0:
        config = configurations.pop()
        serialized_config = serialize_configuration(config)
        if serialized_config != TARGET and not serialized_config in visited:
            for amph, locations in config.items():
                for location in locations:
                    next_configurations = find_next_configurations(location, amph, burrow, config)
                    for next_config, cost in next_configurations:
                        serialized__next_config = serialize_configuration(next_config)
                        configurations.append(next_config)
                        if not serialized__next_config in configuration_graph[serialized_config]:
                            configuration_graph[serialized_config].add(Vertice(serialized__next_config, cost))
        visited.add(serialized_config)
    return configuration_graph

def find_next_configurations(location: Coordinate, amph_type: str, burrow: dict, configuration: dict) -> list:
    # the amphipod is at the back of its destination room or both of its type are in their destination room
    if location == DESTINATIONS[amph_type][1] or all([a in DESTINATIONS[amph_type] for a in configuration[amph_type]]):
        return []
    valid_configurations = []
    valid_moves, required_steps = find_valid_moves(location, amph_type, burrow, configuration)
    for target in valid_moves:
        new_configuration = deepcopy(configuration)
        new_configuration[amph_type].remove(location)
        new_configuration[amph_type].append(target)
        cost = required_steps[target] * ENERGY_COST[amph_type]
        valid_configurations.append((new_configuration, cost))
    return valid_configurations

def find_valid_moves(location: tuple, amphipod_type: str, burrow: dict, configuration: dict) -> list:
    visited = []
    nodes = [(location, 0)]
    valid_targets = set()
    required_steps = defaultdict(lambda: inf)
    while len(nodes) > 0:
        curr, steps = nodes.pop()
        if not curr in visited:
            visited.append(curr)
            for node in burrow[curr]:
                # space can't be occupied by another amphipod, 
                if node not in list(chain.from_iterable(configuration.values())):
                    nodes.append((node, steps + 1))
                    if can_move_into_hallway(location, node, burrow) or can_move_into_room(node, amphipod_type):
                        valid_targets.add(node)
                        required_steps[node] = min(steps + 1, required_steps[node])
    return valid_targets, required_steps

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

def print_configuration(configuration: str) -> None:
    lines = [list('#############'), list('#...........#'), list('###.#.#.#.###'), list('  #.#.#.#.#  '), list('  #########  ')]
    for i in range(0, len(configuration), 5):
        type = configuration[i]
        x = int(configuration[i+1:i+3])
        y = int(configuration[i+3:i+5])
        lines[y][x] = type
    for line in lines:
        print(''.join(line))

# Dijkstra's algorithm (cost interpreted as distance)
def shortest_path_to_target(graph: dict, start: str) -> int:
    distance = defaultdict(lambda: inf)
    distance[start] = 0
    nodes = PriorityQueue()
    nodes.put((distance[start], start))
    visited = set()
    while not nodes.empty():
        # PriorityQueue returns the item with the lowest priority (in this case cost)
        cost, config = nodes.get()
        visited.add(config)
        # iterate adjacent configurations (meaning those that can be reached with one valid step)
        for vertice in graph[config]:
            # only update neighboring node cost if neighbor node has not already been visited
            if not vertice.configuration in visited:
                old_cost = distance[vertice.configuration]
                new_cost = distance[config] + vertice.cost
                if new_cost < old_cost:
                    distance[vertice.configuration] = new_cost
                    nodes.put((new_cost, vertice.configuration))
    return distance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 23, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    burrow, amphipods = read_from_file(args.input)
    graph = create_graph(burrow, amphipods)
    cost = shortest_path_to_target(graph, serialize_configuration(amphipods))
    print(cost[TARGET])