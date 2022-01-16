import argparse

DIGIT_1_SEGMENTS = 2
DIGIT_4_SEGMENTS = 4
DIGIT_7_SEGMENTS = 3
DIGIT_8_SEGMENTS = 7

def read_from_file(fp:str) -> (list, list):
    with open(fp, 'r') as f:
        lines = f.readlines()
        signal_patterns, output_values = [], []
        for line in lines:
            signals, output = line.split(' | ')
            signal_patterns.append([''.join(sorted(pattern)) for pattern in signals.split()])
            output_values.append([''.join(sorted(value)) for value in output.split()])
        return signal_patterns, output_values

def find_patterns(signal_patterns: list) -> (str, str, str, str):
    digit1, digit4, digit7, digit8 = '', '', '', ''
    for pattern in signal_patterns:
        if len(pattern) == DIGIT_1_SEGMENTS:
            digit1 = pattern
        elif len(pattern) == DIGIT_4_SEGMENTS:
            digit4 = pattern
        elif len(pattern) == DIGIT_7_SEGMENTS:
            digit7 = pattern
        elif len(pattern) == DIGIT_8_SEGMENTS:
            digit8 = pattern
    return digit1, digit4, digit7, digit8

def parse_output(output_values: list, digit1: str, digit4: str, digit7: str, digit8: str) -> (int, int, int, int):
    digit1_count, digit4_count, digit7_count, digit8_count = 0, 0, 0, 0
    for output_value in output_values:
        if output_value == digit1:
            digit1_count += 1
        elif output_value == digit4:
            digit4_count += 1
        elif output_value == digit7:
            digit7_count += 1
        elif output_value == digit8:
            digit8_count += 1
    return digit1_count, digit4_count, digit7_count, digit8_count

def parse_segments(signal_patterns: list, output_values: list) -> (int, int, int, int):
    digit1_count_total, digit4_count_total, digit7_count_total, digit8_count_total = 0, 0, 0, 0
    for pattern, output in zip(signal_patterns, output_values):
        digit1, digit4, digit7, digit8 = find_patterns(pattern)
        digit1_count, digit4_count, digit7_count, digit8_count = parse_output(output, digit1, digit4, digit7, digit8)
        digit1_count_total += digit1_count
        digit4_count_total += digit4_count
        digit7_count_total += digit7_count
        digit8_count_total += digit8_count
    return digit1_count_total, digit4_count_total, digit7_count_total, digit8_count_total

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 8, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    signal_patterns, output_values = read_from_file(args.input)
    digit1_count, digit4_count, digit7_count, digit8_count = parse_segments(signal_patterns, output_values)
    result = digit1_count + digit4_count + digit7_count + digit8_count
    print(result)
