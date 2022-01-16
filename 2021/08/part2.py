import argparse

DIGIT_0_SEGMENTS = 6
DIGIT_1_SEGMENTS = 2
DIGIT_2_SEGMENTS = 5
DIGIT_3_SEGMENTS = 5
DIGIT_4_SEGMENTS = 4
DIGIT_5_SEGMENTS = 5
DIGIT_6_SEGMENTS = 6
DIGIT_7_SEGMENTS = 3
DIGIT_8_SEGMENTS = 7
DIGIT_9_SEGMENTS = 6

def read_from_file(fp:str) -> (list, list):
    with open(fp, 'r') as f:
        lines = f.readlines()
        signal_patterns, output_values = [], []
        for line in lines:
            signals, output = line.split(' | ')
            signal_patterns.append([''.join(sorted(pattern)) for pattern in signals.split()])
            output_values.append([''.join(sorted(value)) for value in output.split()])
        return signal_patterns, output_values

def find_patterns(signal_patterns: list) -> list:
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
    digit0, digit2, digit3, digit5, digit6, digit9 = '', '', '', '', '', ''
    for pattern in signal_patterns:
        if len(pattern) == DIGIT_9_SEGMENTS:
            if all(digit in pattern for digit in digit4):
                digit9 = pattern
    for pattern in signal_patterns:
        if len(pattern) == DIGIT_0_SEGMENTS:
            if pattern != digit9 and all(digit in pattern for digit in digit7):
                digit0 = pattern  
    for pattern in signal_patterns:
        if len(pattern) == DIGIT_6_SEGMENTS:
            if pattern != digit9 and pattern != digit0:
                digit6 = pattern                     
    for pattern in signal_patterns:
        if len(pattern) == DIGIT_3_SEGMENTS:
            if all(digit in pattern for digit in digit1):
                digit3 = pattern
    for pattern in signal_patterns:
        if len(pattern) == DIGIT_5_SEGMENTS:
            if  all(digit in digit6 for digit in pattern):
                digit5 = pattern
    for pattern in signal_patterns:
        if len(pattern) == DIGIT_2_SEGMENTS:
            if pattern != digit3 and pattern != digit5:
                digit2 = pattern
    return [digit0, digit1, digit2, digit3, digit4, digit5, digit6, digit7, digit8, digit9]

def parse_output(output_values: list, digits: list) -> int:
    output = ''
    for output_value in output_values:
        for i, digit in enumerate(digits):
            if digit == output_value:
                output += str(i)
    return int(output)

def parse_segments(signal_patterns: list, output_values: list) -> int:
    total = 0
    for pattern, output in zip(signal_patterns, output_values):
        digits = find_patterns(pattern)
        total += parse_output(output, digits)
    return total

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 8, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    signal_patterns, output_values = read_from_file(args.input)
    total = parse_segments(signal_patterns, output_values)
    print(total)
