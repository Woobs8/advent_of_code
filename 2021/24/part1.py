import argparse
from alu import Instruction, ALU
from math import inf

def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        instructions = []
        for line in f.read().splitlines():
            instructions.append(Instruction(line))
    return instructions

def search_for_model_number(instructions: list) -> int:
    alu = ALU(instructions)
    max_valid_model_no = None
    curr_model_no = [9]*14
    while max_valid_model_no is None:
        model_no = int(''.join([str(x) for x in curr_model_no]))
        if not 0 in curr_model_no:
            if alu.MONAD(curr_model_no):
                max_valid_model_no = model_no
        model_no -= 1
        curr_model_no = [int(x) for x in str(model_no)]
    return max_valid_model_no  

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2021 - day 23, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()
    instructions = read_from_file(args.input)
    model_no = search_for_model_number(instructions)
    print(model_no)