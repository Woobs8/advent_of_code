import argparse

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        lines = f.read().splitlines()
        octopi = []
        for line in lines:
            octopi.append([int(num) for num in line])
        return octopi

def simulate(octopi: list) -> int:
    flash_count = 0
    octopi_count = sum([len(line) for line in octopi])
    steps = 0
    while flash_count < octopi_count:
        octopi, step_flash_count = advance(octopi)
        flash_count = step_flash_count
        steps += 1
    return steps

def advance(octopi: list) -> (list, int):
    flashing = []
    for y in range(len(octopi)):
        for x in range(len(octopi[y])):
            octopi[y][x] += 1
            if octopi[y][x] > 9:
                flashing.append((x,y))
    already_detected = set()
    while len(flashing) > 0:
        x, y = flashing.pop()
        if (x,y) not in already_detected:
            already_detected.add((x,y))
            adjacent = [(x-1,y-1), (x-1,y), (x-1,y+1), (x, y-1), (x,y+1), (x+1,y-1), (x+1,y), (x+1,y+1)]
            for adj_x, adj_y in adjacent:
                if len(octopi[y]) > adj_x >= 0 and len(octopi) > adj_y >= 0:
                    octopi[adj_y][adj_x] += 1
                    if octopi[adj_y][adj_x] > 9:
                        flashing.append((adj_x, adj_y))
    flash_count = 0
    for y in range(len(octopi)):
        for x in range(len(octopi[y])):
            if octopi[y][x] > 9:
                flash_count += 1
                octopi[y][x] = 0
    return octopi, flash_count
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 11, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    octopi = read_from_file(args.input)
    steps = simulate(octopi)
    print(steps)