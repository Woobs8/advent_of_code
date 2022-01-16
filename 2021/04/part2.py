import argparse
from collections import defaultdict

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        draws = [int(draw) for draw in f.readline().split(',')]
        board_lines = f.read().splitlines()
        boards = create_boards(board_lines)
        return boards, draws

def create_boards(lines: list) -> list:
    prev_empty_line = False
    boards = []
    current_board = []
    for line in lines:
        if line == '':
            prev_empty_line = True
            if len(current_board) > 0:
                boards.append(current_board)
                current_board = []
        else:
            prev_empty_line = False
            current_board.append([int(num) for num in line.split()])
    if len(current_board) > 0:
        boards.append(current_board)
        current_board = []
    return boards

def index_boards(boards: list) -> dict:
    board_index = defaultdict(list)
    for i, board in enumerate(boards):
        for j, line in enumerate(board):
            for k, num in enumerate(line):
                board_index[num].append([i,j,k])
    return board_index

def play(boards: list, board_index: dict, draws: list, ) -> (list, int):
    line_marks = defaultdict(int)
    column_marks = defaultdict(int)
    remaining_boards = list(range(len(boards)))
    for draw in draws:
        for b, l, n in board_index[draw]:
            if b in remaining_boards:
                boards[b][l][n] = 0
                line_marks[(b,l)] += 1
                column_marks[(b,n)] += 1
                if line_marks[(b,l)] == 5 or column_marks[(b,n)] == 5:
                    remaining_boards.remove(b)
                    if len(remaining_boards) == 0:
                        return boards[b], draw

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 4, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    boards, draws = read_from_file(args.input)
    board_index = index_boards(boards)
    last_board_to_win, draw = play(boards, board_index, draws)
    score = sum([sum(line) for line in last_board_to_win]) * draw
    print(score)