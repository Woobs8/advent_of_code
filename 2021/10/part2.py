import argparse

MISSING_CHAR_TABLE = {')': 1, ']': 2, '}': 3, '>': 4}

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return f.read().splitlines()

def parse_lines(lines: list) -> list:
    missing_characters = []
    for line in lines:
        missing = find_missing_characters(line)
        if len(missing) > 0:
            missing_characters.append(missing)
    return missing_characters

def find_missing_characters(line: str) -> str:
    expected_stack = []
    for char in line:
        if char == '(':
            expected_stack.append(')')
        elif char == '[':
            expected_stack.append(']')
        elif char == '{':
            expected_stack.append('}')
        elif char == '<':
            expected_stack.append('>')
        else:
            if len(expected_stack) > 0:
                expected = expected_stack.pop()
                if char != expected:
                    expected_stack = []
                    break
            else:
                break
    expected_stack.reverse()
    return expected_stack

def calc_scores(missing_characters: list) -> list:
    scores = []
    for lines in missing_characters:
        total_score = 0
        for char in lines:
            total_score *= 5
            total_score += MISSING_CHAR_TABLE[char]
        scores.append(total_score)
    return scores

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 10, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    navigation_subsystem = read_from_file(args.input)
    missing_characters = parse_lines(navigation_subsystem)
    scores = sorted(calc_scores(missing_characters))
    print(scores[(len(scores)-1)//2])