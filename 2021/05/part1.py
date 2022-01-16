import argparse
from collections import defaultdict

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        lines = f.read().splitlines()
        return [parse_line(line) for line in lines]

def parse_line(line: list) -> (int, int, int, int):
    start, end = line.split(' -> ')
    x1, y1 = start.split(',')
    x2, y2 = end.split(',')
    return (int(x1), int(y1), int(x2), int(y2))

def create_diagram(line_segments: list) -> list:
    diagram = defaultdict(lambda: defaultdict(int))
    for x1,y1,x2,y2 in line_segments:
        x_max, x_min = max(x1,x2), min(x1,x2)
        y_max, y_min = max(y1,y2), min(y1,y2)
        if x1 != x2 and y1 == y2:
            for x in range(x_min, x_max+1):
                diagram[x][y1] += 1
        elif y1 != y2 and x1 == x2:
            for y in range(y_min, y_max+1):
                diagram[x1][y] += 1
    return diagram

def count_overlaps(diagram: dict, threshold: int) -> int:
    overlapping_points = 0
    for x in diagram.keys():
        for y in diagram[x].keys():
            if diagram[x][y] >= threshold:
                if diagram[x][y] >= threshold:
                    overlapping_points += 1
    return overlapping_points


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 5, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    line_segments = read_from_file(args.input)
    diagram = create_diagram(line_segments)
    overlapping_points = count_overlaps(diagram, 2)
    print(overlapping_points)