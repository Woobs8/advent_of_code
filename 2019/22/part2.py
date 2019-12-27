import argparse
from typing import Union

N = 119315717514047
M = 101741582076661
pos = 2020


def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return f.readlines()


# express the shuffle process as a linear transformation: a*x + b
def express_shuffle(shuffle:list, n) -> Union[int, int]:
    a, b = 1, 0
    for line in shuffle:
        words = line.strip().split(' ')
        if 'new' in words:
            t_a, t_b = -1, -1
        elif 'increment' in words:
            increment = int(words[3])
            t_a = increment
            t_b = 0
        elif 'cut' in words:
            cut_size = int(words[1])
            t_a = 1
            t_b = -cut_size
        
        # ta * (a * x + b) + tb == ta * a * x + ta*b + tb
        # modulo n is applied to reduce the size of the coefficients, and has no effect on the result
        a = (t_a * a) % n
        b = (t_a * b + t_b) % n
    return a, b


# find the card at the specified index after applying the linear transformation ax+b m times for a sorted deck of size n
def get_card(index:int, a:int, b:int, n:int, m:int) -> int:
    # calculate the coefficients after applying the m iterations
    # Ma = (a**m) % n
    Ma = pow(a, m, n)

    # Mb = b * (a**m - 1) / (a-1) (clever rewrite of the expression ta*b + tb for m in M)
    Mb = (b * (Ma - 1) * inv(a-1, n)) % n

    # to find the card at the specified index after a shuffle, we simply reverse the shuffle
    # by applying the inverse transformation: ((pos - Mb) / Ma) % n
    return ((index - Mb) * inv(Ma, n)) % n


# find the inverse transformation using Fermat's little theorem (because N is prime)
def inv(a:int, n:int) -> int:
    return pow(a, n-2, n)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 22, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    lines = read_from_file(args.input)
    a, b = express_shuffle(lines, N)
    card = get_card(2020, a, b, N, M)
    print(card)
