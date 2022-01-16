import argparse

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return [(i.split()[0], int(i.split()[1])) for i in f.read().splitlines()]

def traverse(instructios: list) -> (int, int):
    x, y = 0, 0
    for instruction in instructions:
        direction = instruction[0]
        distance = instruction[1]
        if direction == 'forward':
            x += distance
        elif direction == 'up':
            y -= distance
        elif direction == 'down':
            y += distance
    return (x,y)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 2, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    instructions = read_from_file(args.input)
    destination = traverse(instructions)
    result = destination[0] * destination[1]
    print(result)