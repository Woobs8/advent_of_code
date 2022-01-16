import argparse
from collections import defaultdict

START = 'start'
FINISH = 'end'

def read_from_file(fp:str) -> dict:
    with open(fp, 'r') as f:
        lines = f.read().splitlines()
        cave_map = defaultdict(list)
        for line in lines:
            key, connection = line.split('-')
            cave_map[key].append(connection)
            cave_map[connection].append(key)
        return cave_map

def find_paths(cave_map: dict) -> list:
    paths = []
    visited = [set()]
    current_path = [START]
    while len(current_path) > 0:
        current_step = current_path[-1]
        if current_step == FINISH:
            paths.append(current_path.copy())
            current_path.pop()
            visited.pop()
        else:
            current_visited = visited[-1]
            connections = cave_map[current_step]
            for connection in connections:
                if connection != START and connection not in current_visited:
                    current_visited.add(connection)
                    if connection.isupper():
                        current_path.append(connection)
                        visited.append(set())
                        break
                    elif small_caves_only_visited_once(current_path) or not (connection in current_path):
                        current_path.append(connection)
                        visited.append(set())
                        break
            if current_path[-1] == current_step:
                current_path.pop()
                visited.pop()
    return paths  

def small_caves_only_visited_once(path: list) -> bool:
    small_caves_visited = defaultdict(int)
    for cave in path:
        if not cave.isupper():
            small_caves_visited[cave] += 1
    return all([count < 2 for count in small_caves_visited.values()])
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 12, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    cave_map = read_from_file(args.input)
    paths = find_paths(cave_map)
    print(len(paths))