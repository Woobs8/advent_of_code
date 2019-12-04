import argparse
from collections import defaultdict
from functools import reduce


def read_from_file(fp):
    with open(fp, 'r') as f:
        lines = f.readlines()
    return lines[0].strip().split(','), lines[1].strip().split(',')


# trace wire and add positions to a set
def trace_wire(wire):
    # use imaginary numbers to track 2D position in one value
    move = {'R':1, 'L':-1, 'U':1j, 'D':-1j}
    trace = set()
    pos = 0
    for step in wire:
        direction = step[0]
        dist = int(step[1:])
        for __ in range(dist):
            pos += move[direction]
            trace.add(pos)
    return trace


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 3, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    wire1, wire2 = read_from_file(args.input)
    trace1 = trace_wire(wire1)
    trace2 = trace_wire(wire2)
    intersections = trace1.intersection(trace2)

    short_dist = reduce(lambda x, y: min(abs(y.real) + abs(y.imag), x), intersections, float('Inf'))
    print('The Manhattan distance to the intersection closest to the central port is: {}'.format(short_dist))
