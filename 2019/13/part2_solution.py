import argparse
import sys
sys.path.append('..')
from Intcode.IntcodeComputer import IntcodeComputer
from util.print_to_console import print_bw_image_to_console
from typing import Union
from enum import IntEnum
from time import sleep
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


# plays the game program by providing input to move the paddle and animate the gameplay if specified
def play_game(memory:list, animate:bool=False, refresh_rate:int=20) -> int:
    memory[0] = 2
    program = IntcodeComputer(memory)

    # set up the initial game board
    out, tiles, height, width = init_board(program)
    score = update(out, tiles)
    block_count, ball, paddle = get_game_info(tiles)
    input = deque([move_joystick(ball, paddle)])
    if animate:
        animate_game(out, tiles, height, width, score)

    # game is played until all blocks are gone
    while block_count > 0:
        out = []
        res = program.execute(input, out)
        out = [out[i:i + 3] for i in range(0, len(out), 3)]
        tmp_score = update(out, tiles)
        if tmp_score:
            score = tmp_score
        block_count, ball, paddle = get_game_info(tiles)
        input.append(move_joystick(ball, paddle))
        if animate:
            animate_game(out, tiles, height, width, score, True)
            sleep(1/refresh_rate)
    return score


# runs the initial step of the program and sets up the game board
def init_board(program:IntcodeComputer) -> Union[list, list, int, int]:
    out = []
    res = program.execute([], out)
    out = [out[i:i + 3] for i in range(0, len(out), 3)]  
    height = max(out, key=lambda x: x[1])[1]+1
    width = max(out, key=lambda x: x[0])[0]+1
    tiles = [[TileSet.EMPTY]*width for __ in range(height)]
    for x, y, id in out:
        tiles[y][x] = TileSet(id)
    return out, tiles, height, width


# extracts block count, ball loc and paddle loc from the game board
def get_game_info(tiles:list) -> Union[int, int, int]:
    block_count = 0
    for y in range(len(tiles)):
        for x in range(len(tiles[0])):
            block_count += 1 if tiles[y][x] == TileSet.BLOCK else 0

            if tiles[y][x] == TileSet.BALL:
                ball = x
            elif tiles[y][x] == TileSet.PADDLE:
                paddle = x
    return block_count, ball, paddle


# update the score and game board
def update(game_output:list, tiles:list) -> int:
    score = None
    for x, y, id in game_output:
        if x == -1 and y == 0:
            score = id
        else:
            tiles[y][x] = TileSet(id)
    return score


# determine how the joystick should move based on ball and paddle locations
def move_joystick(ball:int, paddle:int) -> int:
    if paddle < ball:
        return 1
    elif paddle > ball:
        return -1
    return 0  


# prints the current game board and score to the terminal
def animate_game(game_output:list, tiles:list, height:int, width:int, score:int, refresh:bool=False) -> None:
    print_str = "\033[F"*(height+1) if refresh else ""
    for line in tiles:
        print_str += "".join(map(lambda x: str(x), line)) + "\n"
    print(print_str, flush=True, end="")
    print("Score: {0}".format(score), flush=True, end="\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 13, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    parser.add_argument('-animate', help='show game animation in terminal', default=True, nargs='?')
    parser.add_argument('-rr', help='animation refresh rate', default=20, nargs='?')
    args = parser.parse_args()

    memory = read_from_file(args.input)
    score = play_game(memory, args.animate, args.rr)
    print("### Final score: {0} ###".format(score))