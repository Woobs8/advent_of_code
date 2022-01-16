import argparse

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return [int(draw) for draw in f.readline().split(',')]


# the minimum cost is efficiently found by a ternary search since the cost function is unimodal
def calc_alignment_position(positions: list) -> int:
    min_position = min(positions)
    max_position = max(positions)
    while(max_position - min_position > 2):
        left_third_end_position = min_position + (max_position - min_position) // 3
        left_third_end_position_cost = calc_fuel_cost(positions, left_third_end_position)
        right_third_start_position = max_position - (max_position - min_position) // 3
        right_third_start_position_cost = calc_fuel_cost(positions, right_third_start_position)    
        if left_third_end_position_cost < right_third_start_position_cost:
            max_position = right_third_start_position
        else:
            min_position = left_third_end_position
    return (min_position + max_position) // 2


def calc_fuel_cost(positions: list, target_position: int) -> int:
    fuel_cost = 0
    for position in positions:
        fuel_cost += abs(target_position - position)
    return fuel_cost

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 7, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    positions = read_from_file(args.input)
    alignment_position = calc_alignment_position(positions)
    fuel_cost = calc_fuel_cost(positions, alignment_position)
    print(fuel_cost)