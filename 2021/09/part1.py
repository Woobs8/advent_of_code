import argparse

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        lines = f.read().splitlines()
        height_map = []
        for line in lines:
            height_map.append([int(num) for num in line])
    return height_map

def find_valleys(height_map: list) -> list:
    valleys = []
    for y in range(len(height_map)):
        for x in range(len(height_map[y])):
            left, right, top, bottom = True, True, True, True
            curr_element = height_map[y][x]
            if x-1 >= 0:
                left = height_map[y][x-1] > curr_element
            if x+1 < len(height_map[y]):
                right = height_map[y][x+1] > curr_element
            if y-1 >= 0:
                top = height_map[y-1][x] > curr_element
            if y+1 < len(height_map):
                bottom = height_map[y+1][x] > curr_element
            if all([left, right, top, bottom]):
                valleys.append((x,y))
    return valleys

def calc_risk(height_map: list, valleys: list) -> int:
    return len(valleys) + sum([height_map[y][x] for x,y in valleys])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 9, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    height_map = read_from_file(args.input)
    valleys = find_valleys(height_map)
    risk = calc_risk(height_map, valleys)
    print(risk)