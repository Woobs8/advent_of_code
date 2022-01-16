import argparse

def read_from_file(fp:str) -> (list, list):
    with open(fp, 'r') as f:
        dots = []
        line = f.readline().strip()
        max_x = 0
        max_y = 0
        while line != '':
            x, y = line.split(',')
            x, y = int(x), int(y)
            max_x = x if x > max_x else max_x
            max_y = y if y > max_y else max_y
            dots.append((int(x),int(y)))
            line = f.readline().strip()
        width = max_x + 2 if max_x % 2 != 0 else max_x + 1
        height = max_y + 2 if max_y % 2 != 0 else max_y + 1
        manual = [[0]*width for __ in range(height+1)]
        test = 0
        for x,y in dots:
            manual[y][x] += 1
        folds = []
        lines = f.read().splitlines()
        for line in lines:
            axis, value = line[len('fold along '):].split('=')
            folds.append((axis, int(value)))
        return manual, folds 

def apply_folds(folds: list, manual: list, limit: int) -> list:
    for axis, value in folds[:limit]:
        manual = fold_along_axis(axis, value, manual)
    return manual

def fold_along_axis(fold_axis: str, fold_axis_value: int, manual: list) -> list:
    if fold_axis == 'x':
        return fold_along_x_axis(manual, fold_axis_value)
    elif fold_axis == 'y':
        return fold_along_y_axis(manual, fold_axis_value)

def fold_along_x_axis(manual: list, axis_value: int) -> list:
    folded_manual = []
    for i, line in enumerate(manual):
        folded_line = []
        for j, (value, folded_value) in enumerate(zip(line[:axis_value], line[-1:axis_value:-1])):
            folded_line.append(value + folded_value) 
        folded_manual.append(folded_line)
    return folded_manual

def fold_along_y_axis(manual: list, axis_value: int) -> list:
    folded_manual = []
    for line, bottom_line in zip(manual[:axis_value], manual[-1:axis_value:-1]):
        folded_line = []
        for value, folded_value in zip(line, bottom_line):
            folded_line.append(value + folded_value)
        folded_manual.append(folded_line)
    return folded_manual

def count_dots(folded_manual: list) -> int:
    dot_count = 0
    for y in range(len(folded_manual)):
        for x in range(len(folded_manual[y])):
            if folded_manual[y][x] > 0:
                dot_count += 1
    return dot_count

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 13, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    manual, folds = read_from_file(args.input)
    folded_manual = apply_folds(folds, manual, 1)
    dot_count = count_dots(folded_manual)
    print(dot_count)