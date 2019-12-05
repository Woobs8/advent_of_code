import argparse
from itertools import permutations
import math


ADD = 1
MULT = 2
INPUT = 3
OUTPUT = 4
HALT = 99


PARAM_COUNT = {
    ADD:3,
    MULT:3,
    INPUT:1,
    OUTPUT:1,
    HALT:0
}


POSITION_MODE = 0
IMMEDIATE_MODE = 1


def read_from_file(fp):
    with open(fp, 'r') as f:
        return list(map(int, f.read().split(',')))


# recursively execute the program until reaching a halt operation
def execute_program(instr_idx, memory, inputs):
    op = memory[instr_idx]
    op_len = int(math.log10(op))+1

    # parameter modes are extracted from instruction and set to zero if missing
    if op_len >= 3:
        op_code = op % 10
        param_modes = [int(x) for x in str(op)][-3::-1]
        param_modes += [0]*(PARAM_COUNT[op_code]-len(param_modes))
    else:
        op_code = op
        param_modes = [0]*PARAM_COUNT[op_code]
    params = get_params(instr_idx, param_modes, memory)
    if op_code == ADD:
        memory[memory[instr_idx+3]] = params[0] + params[1]
    elif op_code == MULT:
        memory[memory[instr_idx+3]] = params[0] * params[1]
    elif op_code == INPUT:
        memory[memory[instr_idx+1]] = inputs[0]
        inputs = inputs[1:]
    elif op_code == OUTPUT:
        print("{}\n".format(params[0]))
    elif op_code == HALT:
        return
    else:
        raise AssertionError('opcode {} does not exist. You messed up :('.format(op_code))

    execute_program(instr_idx+PARAM_COUNT[op_code]+1, memory, inputs)


# returns list of params for specified parameter mode
def get_params(instr_idx, param_modes, memory):
    params = []
    for i, mode in enumerate(param_modes, 1):
        if mode == POSITION_MODE:
            params.append(memory[memory[instr_idx+i]])
        elif mode == IMMEDIATE_MODE:
            params.append(memory[instr_idx+i])
        else: 
            raise AssertionError('parameter mode {} does not exist. You messed up :('.format(mode))
    return params


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 5, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    memory = read_from_file(args.input)
    execute_program(0, memory, [1])