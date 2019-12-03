import argparse
from collections import defaultdict
from functools import reduce


def read_from_file(fp):
    with open(fp, 'r') as f:
        lines = f.readlines()
    return lines[0].strip().split(','), lines[1].strip().split(',')


# trace wire along grid and store lowest number of steps required to reach each trace point
def trace_wire(wire, grid):   
    x = 0
    y = 0
    traced = set()
    cumulative_steps = 0
    for trace in wire:
        direction = trace[0]
        dist = int(trace[1:])
        new_x, new_y = x, y

        for step in range(1, dist+1):
            cumulative_steps += 1
            if direction == 'R':
                new_x = x + step
                if (new_x,y) not in traced:
                    grid[(new_x,y)].append(cumulative_steps)
                    traced.add((new_x,y))
            elif direction == 'L':
                new_x = x - step
                if (new_x,y) not in traced:
                    grid[(new_x,y)].append(cumulative_steps)
                    traced.add((new_x,y))
            elif direction == 'U':
                new_y = y + step
                if (x,new_y) not in traced:
                    grid[(x,new_y)].append(cumulative_steps)
                    traced.add((x,new_y))
            elif direction == 'D':
                new_y = y - step
                if (x,new_y) not in traced:
                    grid[(x,new_y)].append(cumulative_steps)
                    traced.add((x,new_y))
        x = new_x
        y = new_y


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 3, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    wire1, wire2 = read_from_file(args.input)
    grid = defaultdict(list)
    trace_wire(wire1, grid)
    trace_wire(wire2, grid)
    fewest_steps = min([sum(value) for (key, value) in grid.items() if len(value) == 2 and key != (0,0)])
    print('The fewest numbers of steps wires must take to intersect is: {}'.format(fewest_steps))
