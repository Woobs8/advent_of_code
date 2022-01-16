import argparse

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return f.read().splitlines()

def find_oxygen_generator_rating(diagnostics: list, comparison_index: int) -> int:    
    filtered_diagnostics = []
    most_common_bit = find_most_common_bit(diagnostics, comparison_index)
    for i, diagnostic in enumerate(diagnostics):
        comparator = '1' if most_common_bit == '-' else most_common_bit
        if diagnostic[comparison_index] == comparator:
            filtered_diagnostics.append(diagnostic)
    if len(filtered_diagnostics) == 1:
        return int(filtered_diagnostics[0], 2)
    else:            
        return find_oxygen_generator_rating(filtered_diagnostics, comparison_index + 1)

def find_most_common_bit(diagnostics: list, comparison_index: int) -> str:
    bit_count = sum([int(diagnostic[comparison_index],2) for diagnostic in diagnostics])
    if bit_count > len(diagnostics)/2:
        return '1'
    elif bit_count < len(diagnostics)/2:
        return '0'
    else:
        return '-'

def find_co2_scrubber_rating(diagnostics: list, comparison_index: int) -> int:
    filtered_diagnostics = []
    least_common_bit = find_least_common_bit(diagnostics, comparison_index)
    for i, diagnostic in enumerate(diagnostics):
        comparator = '0' if least_common_bit == '-' else least_common_bit
        if diagnostic[comparison_index] == comparator:
            filtered_diagnostics.append(diagnostic)
    if len(filtered_diagnostics) == 1:
        return int(filtered_diagnostics[0], 2)
    else:            
        return find_co2_scrubber_rating(filtered_diagnostics, comparison_index + 1)

def find_least_common_bit(diagnostics: list, comparison_index: int) -> str:
    bit_count = sum([int(diagnostic[comparison_index],2) for diagnostic in diagnostics])
    if bit_count > len(diagnostics)/2:
        return '0'
    elif bit_count < len(diagnostics)/2:
        return '1'
    else:
        return '-'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 3, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    diagnostics = read_from_file(args.input)
    oxygen_generator_rating = find_oxygen_generator_rating(diagnostics, 0)
    co2_scrubber_rating = find_co2_scrubber_rating(diagnostics, 0)
    life_support_rating = oxygen_generator_rating * co2_scrubber_rating
    print(oxygen_generator_rating, co2_scrubber_rating, life_support_rating)