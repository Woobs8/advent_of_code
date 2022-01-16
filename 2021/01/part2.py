import argparse


def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return [int(i) for i in f.read().splitlines()]

def compute_running_sum(measurements: list, window_size:int) -> list:
    running_sum = []
    for i in range(len(measurements)):
        if (i + window_size <= len(measurements)):
            running_sum.append(sum(measurements[i:i + window_size]))
    return running_sum

def compare_measurements(measurements:list) -> int:
    increases = 0
    for i1,i2 in zip(measurements[0::], measurements[1::]):
        if (not i1 is None and not i2 is None):
            increases += 1 if i2 > i1 else 0
    return increases

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 1, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    measurements = read_from_file(args.input)
    running_sum = compute_running_sum(measurements, 3)
    increases = compare_measurements(running_sum)
    print(increases)