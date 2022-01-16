import argparse
from collections import Counter, defaultdict

def read_from_file(fp:str) -> (list, list):
    with open(fp, 'r') as f:
        template = f.readline().strip()
        insertion_rules = {}
        for line in f.read().splitlines():
            if line != '':
                pair, target = line.split(' -> ')
                insertion_rules[pair] = target
        return template, insertion_rules 

def process(template: str, insertion_rules: list, steps: int) -> dict:
    initial_pair_count = defaultdict(int)
    element_count = defaultdict(int)
    for i in range(len(template)):
        current_element = template[i]
        element_count[current_element] += 1
        if i + 1 < len(template):
            next_element = template[i+1]
            initial_pair_count[current_element + next_element] += 1
        
    for step in range(steps):
        pair_count = initial_pair_count.copy()
        for pair, count in initial_pair_count.items():
            if count > 0:
                inserted_element = insertion_rules[pair]
                element_count[inserted_element] += initial_pair_count[pair]
                pair_count[pair] -= initial_pair_count[pair]
                pair_count[pair[0] + inserted_element] += initial_pair_count[pair]
                pair_count[inserted_element + pair[1]] += initial_pair_count[pair]
        initial_pair_count = pair_count
    return element_count

def calc_result(element_count: dict) -> int:
    counter = Counter(element_count)
    sorted_by_frequency = counter.most_common(len(counter.keys()))
    return sorted_by_frequency[0][1] - sorted_by_frequency[-1][1] 
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 14, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    template, insertion_rules = read_from_file(args.input)
    element_count = process(template, insertion_rules, 40)
    result = calc_result(element_count)
    print(result)