import argparse
from collections import defaultdict
from math import inf
from queue import PriorityQueue
from itertools import product

def read_from_file(fp:str) -> (list, tuple):
    with open(fp, 'r') as f:
        risk_level_map = []
        for line in f.read().splitlines():
            risk_level_map.append([int(num) for num in line])
        target = (len(risk_level_map[0])-1, len(risk_level_map)-1)
        return risk_level_map, target
    
# Dijkstra's algorithm (risk interpreted as distance)
def find_shortest_path(risk_level_map: list, start: tuple) -> dict:
    distance = defaultdict(lambda: inf)
    distance[start] = 0
    nodes = PriorityQueue()
    nodes.put((distance[start], start))
    visited = set()
    while not nodes.empty():
        # PriorityQueue returns the item with the lowest priority (in this case distance)
        dist, (x,y) = nodes.get()
        visited.add((x,y))
        # iterate horizontally and vertically adjacent neighbors
        for x_adj,y_adj in [(x-1,y), (x+1,y), (x,y-1), (x, y+1)]:
            # only update neighboring node distance if neighbor node has not already been visited
            if (x_adj,y_adj) not in visited and 0 <= y_adj < len(risk_level_map) and 0 <= x_adj < len(risk_level_map[y_adj]):
                dist_to_adjacent_node = risk_level_map[y_adj][x_adj]
                old_cost = distance[(x_adj,y_adj)]
                new_cost = distance[(x,y)] + dist_to_adjacent_node
                if new_cost < old_cost:
                    distance[(x_adj, y_adj)] = new_cost
                    nodes.put((new_cost, (x_adj, y_adj)))
    return distance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 15, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    risk_level_map, target = read_from_file(args.input)
    minimum_risk_levels = find_shortest_path(risk_level_map, (0,0))
    print(minimum_risk_levels[target])