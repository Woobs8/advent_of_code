import argparse
from collections import defaultdict

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return f.read().splitlines()

def find_most_common_bits(diagnostics: list) -> str:
    bit_count = defaultdict(int)
    for diagnostic in diagnostics:
        for i in range(len(diagnostic)):
            bit_count[i] += int(diagnostic[i])
    return ''.join(['1' if b > len(diagnostics)/2 else '0' for i, b in sorted(bit_count.items())])

def calc_power_consumption(gamme_rate: str, epsilon_rate: str) -> int:
    return int(gamma_rate, 2) * int(epsilon_rate, 2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 3, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    diagnostics = read_from_file(args.input)
    gamma_rate = find_most_common_bits(diagnostics)
    epsilon_rate = ''.join(['0' if b == '1' else '1' for b in gamma_rate])
    power_consumption = calc_power_consumption(gamma_rate, epsilon_rate)
    print(power_consumption)