import argparse

WINNING_SCORE = 21
DIE_ROLL_OUTCOMES = [i+j+k for i in range(1,4) for j in range(1,4) for k in range(1,4)]
DIE_ROLL = {roll:DIE_ROLL_OUTCOMES.count(roll) for roll in DIE_ROLL_OUTCOMES}.items()

def read_from_file(fp:str) -> (int, int):
    with open(fp, 'r') as f:
        lines = f.read().splitlines()
        player1 = int(lines[0][-1])
        player2 = int(lines[1][-1])
    return player1, player2

def play(player1: int, player2: int) -> (int, int):
    games = {(x,y,z,w):0 for x in range(10) for y in range(WINNING_SCORE + 1) for z in range(10) for w in range(WINNING_SCORE + 1)}
    games[(player1, 0, player2, 0)] = 1
    player1_wins = 0
    player2_wins = 0
    while not max(games.values()) == 0:
        for (player1_pos, player1_score, player2_pos, player2_score), count in games.items():
            if count > 0:
                for player1_roll, roll_freq1 in DIE_ROLL:
                    new_player1_pos = (player1_pos + player1_roll) % 10
                    new_player1_score = player1_score + new_player1_pos + 1
                    for player2_roll, roll_freq2 in DIE_ROLL:
                        new_player2_pos = (player2_pos + player2_roll) % 10
                        new_player2_score = player2_score + new_player2_pos + 1
                        if new_player1_score < WINNING_SCORE and new_player2_score < WINNING_SCORE:
                            games[(new_player1_pos, new_player1_score, new_player2_pos, new_player2_score)] += count * roll_freq1 * roll_freq2
                        elif new_player2_score >= WINNING_SCORE and new_player1_score < WINNING_SCORE:
                            player2_wins += count * roll_freq2
                    if new_player1_score >= WINNING_SCORE:
                        player1_wins += count * roll_freq1
                    games[(player1_pos, player1_score, player2_pos, player2_score)] = 0
    return player1_wins, player2_wins

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 21, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    player1, player2 = read_from_file(args.input)
    player1_wins, player2_wins = play(player1-1, player2-1)
    print(max(player1_wins, player2_wins))