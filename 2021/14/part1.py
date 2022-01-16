import argparse
from collections import Counter

def read_from_file(fp:str) -> (list, list):
    with open(fp, 'r') as f:
        template = f.readline().strip()
        insertion_rules = {}
        for line in f.read().splitlines():
            if line != '':
                pair, target = line.split(' -> ')
                insertion_rules[pair] = target
        return template, insertion_rules 

def process(template: str, insertion_rules: list, steps: int) -> str:
    initial_polymer = template
    for __ in range(steps):
        processed_polymer = ""
        for i in range(len(initial_polymer)):
            current_element = initial_polymer[i]
            processed_polymer += current_element
            if i + 1 < len(initial_polymer):
                next_element = initial_polymer[i+1]
                processed_polymer += insertion_rules[current_element + next_element]
        initial_polymer = processed_polymer
    return processed_polymer

def calc_result(polymer: str):
    counter = Counter(polymer)
    sorted_by_frequency = counter.most_common(len(counter.keys()))
    return sorted_by_frequency[0][1] - sorted_by_frequency[-1][1] 
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 14, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    template, insertion_rules = read_from_file(args.input)
    polymer = process(template, insertion_rules, 10)
    result = calc_result(polymer)
    print(result)