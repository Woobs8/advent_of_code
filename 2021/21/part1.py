import argparse

WINNING_SCORE = 1000

def read_from_file(fp:str) -> (int, int):
    with open(fp, 'r') as f:
        lines = f.read().splitlines()
        player1 = int(lines[0][-1])
        player2 = int(lines[1][-1])
    return player1, player2

def play(player1: int, player2: int) -> (int, int, int):
    player1_score = 0
    player2_score = 0
    turn = 0
    while player1_score < WINNING_SCORE and player2_score < WINNING_SCORE:
        dice_roll = roll_die(turn)
        if turn % 2 == 0:
            player1 = (player1 + dice_roll) % 10
            player1_score += player1 + 1
        else:
            player2 = (player2 + dice_roll) % 10
            player2_score += player2 + 1
        turn += 1
    return player1_score, player2_score, turn

def roll_die(turn: int) -> int:
    return (turn * 3 + 2) * 3

def calc_result(loser_score: int, turns: int) -> int:
    return loser_score * turns * 3

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 21, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    player1, player2 = read_from_file(args.input)
    player1_score, player2_score, turns = play(player1-1, player2-1)
    result = calc_result(min(player1_score, player2_score), turns)
    print(result)