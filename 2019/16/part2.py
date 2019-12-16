import argparse
from math import ceil
from functools import reduce
from itertools import accumulate


def read_from_file(fp:str) -> str:
    with open(fp, 'r') as f:
        return f.read()

"""
The key for this puzzle is to realize that the output can be 
determined by multiplying the input with an upper-triangular matrix and
then taking the modulo of the absolute value of each output element.
Taking the abs means the operation as a whole is non-linear, and
cannot be calculated using efficient matrix multiplication tools.

An additional observation is that when multiplying with an upper-triangular
matrix, the second half of the output only ever depends on the second half 
of the input. This effectively means we can ignore the first half to speed up 
computation, if the indices we are looking for are in the second half of 
the output (they always are - its part of the puzzle).

The final trick is to realize that in an upper-triangular matrix the
bottom half of the matrix (the one producing the last half of the output) 
contains no negative numbers, which means we can disregard the abs operation
and reduce each phase to taking the modulo of partial sums of the reversed
input signal.


Example:
We calculate the output by taking the modulo of the partial sums of the reversed 
input - starting from the last element (8), then moving to (7), then (6) and finally (5).
Once we have found half the output, we have all we need for the next phase.

signal = 12345678
1*1  + 2*0  + 3*-1 + 4*0  + 5*1  + 6*0  + 7*-1 + 8*0  = - no need to calculate
1*0  + 2*1  + 3*1  + 4*0  + 5*0  + 6*-1 + 7*-1 + 8*0  = - no need to calculate
1*0  + 2*0  + 3*1  + 4*1  + 5*1  + 6*0  + 7*0  + 8*0  = - no need to calculate
1*0  + 2*0  + 3*0  + 4*1  + 5*1  + 6*1  + 7*1  + 8*0  = - no need to calculate
1*0  + 2*0  + 3*0  + 4*0  + 5*1  + 6*1  + 7*1  + 8*1  = (5+6+7+8) % 10 = 6
1*0  + 2*0  + 3*0  + 4*0  + 5*0  + 6*1  + 7*1  + 8*1  = (6+7+8) % 10 = 1
1*0  + 2*0  + 3*0  + 4*0  + 5*0  + 6*0  + 7*1  + 8*1  = (7+8) % 10 = 5
1*0  + 2*0  + 3*0  + 4*0  + 5*0  + 6*0  + 7*0  + 8*1  = 8 % 10 = 8
output = ----6158
"""

def fft_phases(seq:str, repeats:int, phases:int) -> list:
    # the offset is the first seven digits of the input sequence
    offset = int(seq[:7])

    # slice sequence from the index of interest and forward (assuming index is always in the second half)
    # reverse the sequence to prepare for efficiently calculating the partial sums
    sig = list(map(int, (seq*repeats)[offset:][::-1]))
    
    # each phase is modulo 10 of the partial sums of the reversed list
    for _ in range(phases):
        sig = list(accumulate(sig, lambda x,y: (x + y) % 10))
    return sig[::-1]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 16, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    input_sequence = read_from_file(args.input)
    out = fft_phases(input_sequence, 10000, 100)
    print(out[:8])