import argparse
from functools import reduce


def read_from_file(fp):
    with open(fp) as f:
        return [int(line.strip()) for line in f.readlines()]


def calc_fuel_req(mass):
    return mass // 3 - 2


# recursively calculates the fuel required for a given mass, and adds it to the current fuel amount 
def recursive_fuel_req(mass):
    if mass <= 0:
        return 0

    fuel_req = calc_fuel_req(mass)
    fuel_req = fuel_req if fuel_req >= 0 else 0
    return fuel_req + recursive_fuel_req(fuel_req)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 1, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    fuel_req = reduce(lambda x, y: x + recursive_fuel_req(y), read_from_file(args.input), 0)
    print("The total fuel requirement is: {}".format(fuel_req))