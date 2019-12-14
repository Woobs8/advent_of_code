import argparse
import sys
sys.path.append('..')
from intcode.IntcodeComputer import IntcodeComputer
from util.print_to_console import print_bw_image_to_console
from typing import Union
from enum import IntEnum
from functools import reduce
from collections import deque


# characters used to repsent the tileset when animating the game
TILESET = {
    0: ' ',
    1: '|',
    2: '#',
    3: '_',
    4: 'o'
}


class TileSet(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4

    def __str__(self):
        return TILESET[self.value]


def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return list(map(int, f.read().split(',')))


# execute the game program and return the output
def run_game(memory:list) -> list:
    program = IntcodeComputer(memory)
    out = []
    program.execute(deque(), out)
    return [out[i:i + 3] for i in range(0, len(out), 3)]
    

# animate the game output
def animate_game(game_output:list) -> None:
    height = max(game_output, key=lambda x: x[1])[1]+1
    width = max(game_output, key=lambda x: x[0])[0]+1
    tiles = [[TileSet.EMPTY]*width for __ in range(height)]
    for x, y, id in game_output:
        tiles[y][x] = TileSet(id)
    
    print_str = ""
    for line in tiles:
        print_str += "".join(map(lambda x: str(x), line)) + "\n"
    print(print_str)


# count the number of blocks on the game board
def count_blocks(game_output:list) -> int:
    return reduce(lambda x,y: x+1 if y[2]==TileSet.BLOCK else x, game_output, 0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 13, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    memory = read_from_file(args.input)
    output = run_game(memory)
    animate_game(output)
    blocks = count_blocks(output)
    print('Block count: {0}'.format(blocks))
