import argparse


def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return f.readlines()


# shuffle the deck while keeping track track of a single card
def shuffle(deck_size:int, index:int, shuffle_process:list) -> list:
    for move in shuffle_process:
        words = move.strip().split(' ')
        if 'new' in words:
            index = deck_size-1-index
        elif 'increment' in words:
            increment = int(words[3])
            index = (index*increment) % deck_size        
        elif 'cut' in words:
            cut_size = int(words[1])
            index = (index - cut_size) % deck_size
    return index


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 22, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    lines = read_from_file(args.input)
    index = shuffle(10007, 2019, lines)
    print(index)
