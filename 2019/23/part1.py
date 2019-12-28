import argparse
import sys
sys.path.append('..')
from Intcode.IntcodeComputer import IntcodeComputer
from typing import Union
from collections import deque


def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return list(map(int, f.read().split(',')))


def boot_network(n_computers:int, memory:list) -> Union[int, int]:
    computers = [IntcodeComputer(memory.copy()) for __ in range(n_computers)]
    in_queue = [deque([i]) for i in range(n_computers)]
    out_queue = [deque() for __ in range(n_computers)]
    while True:
        # computers
        for i in range(n_computers):
            in_queue[i] = deque([-1]) if not in_queue[i] else in_queue[i]
            computers[i].execute(in_queue[i], out_queue[i])
        
        # router
        for i in range(n_computers):
            while out_queue[i]:
                addr =  out_queue[i].popleft()
                x = out_queue[i].popleft()
                y = out_queue[i].popleft()
                if addr == 255:
                    return x, y
                in_queue[addr] += deque([x, y])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 23, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    memory = read_from_file(args.input)
    x, y = boot_network(50, memory)
    print(y)