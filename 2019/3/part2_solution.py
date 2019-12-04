import argparse
from collections import defaultdict
from functools import reduce


def read_from_file(fp):
    with open(fp, 'r') as f:
        lines = f.readlines()
    return lines[0].strip().split(','), lines[1].strip().split(',')


# trace wire and add positions and steps as key-value pairs in hash map
def trace_wire(wire):
    # use imaginary numbers to track 2D position in one value
    move = {'R':1, 'L':-1, 'U':1j, 'D':-1j}
    trace = {}
    pos = 0
    cumulative_steps = 0
    for step in wire:
        direction = step[0]
        dist = int(step[1:])
        for __ in range(dist):
            cumulative_steps += 1
            pos += move[direction]
            if pos not in trace:
                trace[pos] = cumulative_steps
    return trace    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 3, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    wire1, wire2 = read_from_file(args.input)
    trace1 = trace_wire(wire1)
    trace2 = trace_wire(wire2)
    intersections = set(trace1.keys()).intersection(trace2.keys())
    
    fewest_steps = reduce(lambda x, y: min(trace1[y]+trace2[y], x), intersections, float('Inf'))
    print('The fewest numbers of steps wires must take to intersect is: {}'.format(fewest_steps))
