import argparse
from pair import Pair

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return [parse_number(line, None) for line in f.read().splitlines()]

def parse_number(number: str, parent: Pair):
    if len(number) == 1:
        return Pair(int(number), None, None, parent)
    else:
        assert([number[0] == '['])
        closing_braces = [']']
        i = 0
        left_stopping_index = None
        right_starting_index = None
        while len(closing_braces) > 0:
            i += 1
            if number[i] == '[':
                closing_braces.append(']')
            elif number[i] == ']':
                closing_braces.pop()
            elif len(closing_braces) == 1 and number[i] == ',':
                left_stopping_index = i
                right_starting_index = i + 1
        pair = Pair(None, None, None, None)
        pair.left = parse_number(number[1:left_stopping_index], pair)
        pair.right = parse_number(number[right_starting_index:i], pair)
        pair.parent = parent
        return pair

def sum_numbers(numbers: list) -> Pair:
    current_sum = numbers[0]
    for i in range(1, len(numbers)):
        current_sum = reduce_number(add(current_sum, numbers[i]))
    return current_sum

def add(left_operand: Pair, right_operand: Pair) -> Pair:
    sum_pair = Pair(None, left_operand, right_operand, None)
    left_operand.parent = sum_pair
    right_operand.parent = sum_pair
    return sum_pair


def reduce_number(pair: Pair) -> Pair:
    explosions = []
    splits = []
    map_explosions(pair, explosions)
    explosions.reverse()
    while len(explosions) > 0 or len(splits) > 0:
        if len(explosions) > 0:
            exploding_pair = explosions.pop()
            left_adjacent, right_adjacent = exploding_pair.explode()
            if not left_adjacent is None and left_adjacent.value >= 10:
                splits.append(left_adjacent)
            if not right_adjacent is None and  right_adjacent.value >= 10:
                splits.append(right_adjacent)
        else:
            splits = sort_by_rightmost(splits)
            splitting_pair = splits.pop()
            if is_valid_pair(splitting_pair) and not splitting_pair.value is None and splitting_pair.value >= 10:
                splitting_pair.split()
                if splitting_pair.get_depth() >= 4:
                    explosions.append(splitting_pair)
                if splitting_pair.left.value >= 10:
                    splits.append(splitting_pair.left)
                if splitting_pair.right.value >= 10:
                    splits.append(splitting_pair.right)
    return pair

def map_explosions(pair: Pair, explosions: list = []) -> None:
    if pair is None:
        return
    else:
        if pair.get_depth() >= 4 and pair.value is None:
            explosions.append(pair)
        else:
            map_explosions(pair.left, explosions)
            map_explosions(pair.right, explosions)

def sort_by_rightmost(pairs: list) -> list:
    return sorted(pairs, key = lambda x: x.get_position(), reverse=True)

def is_valid_pair(pair: Pair) -> bool:
    if not pair.parent is None:
        return pair.parent.left is pair or pair.parent.right is pair
    else:
        return not pair.value is None or (not pair.left is None and not pair.right is None)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 18, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    numbers = read_from_file(args.input)
    numbers_sum = sum_numbers(numbers)
    print(numbers_sum)
    sum_magnitude = numbers_sum.get_magnitude()
    print(sum_magnitude)
    

