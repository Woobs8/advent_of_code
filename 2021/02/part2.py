import argparse

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return [(i.split()[0], int(i.split()[1])) for i in f.read().splitlines()]

def traverse(instructios: list) -> (int, int):
    x, y, aim = 0, 0, 0
    for instruction in instructions:
        direction = instruction[0]
        distance = instruction[1]
        if direction == 'forward':
            x += distance
            y += aim * distance
        elif direction == 'up':
            aim -= distance
        elif direction == 'down':
            aim += distance
    return (x,y)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 2, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    instructions = read_from_file(args.input)
    destination = traverse(instructions)
    result = destination[0] * destination[1]
    print(result)