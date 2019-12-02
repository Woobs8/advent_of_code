import argparse
from functools import reduce


def read_from_file(fp):
    with open(fp) as f:
        return [int(line.strip()) for line in f.readlines()]


def calc_fuel_req(mass):
    return mass // 3 - 2


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 1, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    modules = read_from_file(args.input)
    fuel_req = reduce(lambda x, y: x + calc_fuel_req(y), modules, 0)
    print("The total fuel requirement is: {:.0f}".format(fuel_req))