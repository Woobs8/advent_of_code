import argparse

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return [int(draw) for draw in f.readline().split(',')]

def simulate(initial_timers: list, days: int) -> list:
    current_timers = [0]*9
    for timer in initial_timers:
        current_timers[timer] += 1
    for __ in range(days):
        spawn = current_timers[0]
        current_timers = current_timers[1:] + [spawn]
        current_timers[6] += spawn
    return current_timers

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 6, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    initial_timers = read_from_file(args.input)
    current_timers = simulate(initial_timers, 80)
    count = sum(current_timers)
    print(count)