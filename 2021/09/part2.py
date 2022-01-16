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

def find_basins(height_map: list, valleys: list) -> list:
    return [find_basin(height_map, (x,y)) for x,y in valleys]

def find_basin(height_map: list, center_point: tuple) -> int:
    x, y = center_point
    adjacent_points = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    visied_points = {center_point}
    basin_size = 1
    while len(adjacent_points) > 0:
        x, y = adjacent_points[0]
        adjacent_points = adjacent_points[1:]
        if (x,y) not in visied_points:
            visied_points.add((x,y))
            if (len(height_map) > y >= 0) and (len(height_map[y]) > x >= 0):
                if height_map[y][x] < 9:
                    basin_size += 1
                    adjacent_points += [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    return basin_size

def calc_result(basins: list) -> int:
    product = 1
    for basin in sorted(basins, reverse=True)[0:3]:
        product *= basin
    return product

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 9, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    height_map = read_from_file(args.input)
    valleys = find_valleys(height_map)
    basins = find_basins(height_map, valleys)
    result = calc_result(basins)
    print(result)