import argparse

ILLEGAL_CHAR_TABLE = {')': 3, ']': 57, '}': 1197, '>': 25137}

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return f.read().splitlines()

def parse_lines(lines: list) -> list:
    illegal_characters = []
    for line in lines:
        illegal_character = find_first_illegal_character(line)
        if illegal_character != None:
            illegal_characters.append(illegal_character)
    return illegal_characters

def find_first_illegal_character(line: str) -> str:
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
            expected = expected_stack.pop()
            if char != expected:
                return char

def calc_score(illegal_characters: list) -> int:
    return sum([ILLEGAL_CHAR_TABLE[char] for char in illegal_characters])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 10, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    navigation_subsystem = read_from_file(args.input)
    illegal_characters = parse_lines(navigation_subsystem)
    score = calc_score(illegal_characters)
    print(score)