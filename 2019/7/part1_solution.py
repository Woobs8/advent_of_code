import argparse
from itertools import permutations
import math
from functools import reduce


ADD = 1
MULT = 2
INPUT = 3
OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUALS = 8
HALT = 99


PARAM_COUNT = {
    ADD:3,
    MULT:3,
    INPUT:1,
    OUTPUT:1,
    INPUT:1,
    OUTPUT:1,
    JUMP_IF_TRUE:2,
    JUMP_IF_FALSE:2,
    LESS_THAN:3,
    EQUALS:3,
    HALT:0,
}


POSITION_MODE = 0
IMMEDIATE_MODE = 1


NO_OUTPUT = None
INPUT_REQUIRED = 1j


def read_from_file(fp):
    with open(fp, 'r') as f:
        return list(map(int, f.read().split(',')))


# calculate the thruster output for all possible permutations of inputs
def calc_max_thruster_output(valid_inputs, memory):
    return reduce(lambda x, y: max(x, calc_phase_sequence_output(y, memory)), permutations(valid_inputs), 0)


# execute program for each amplifier with the specified phase sequence and return the last recorded output
def calc_phase_sequence_output(phase_seq, memory):
    return reduce(lambda x, y: execute_from(0, memory.copy(), [y, x[-1]]), phase_seq, [0])[-1]


# executes the program until reaching a halt operation and returns the recorded output as a list
def execute_from(instr_idx, memory, inputs):
    input_idx = 0
    out = []
    while instr_idx != None:
        res, instr_idx = execute_instruction(instr_idx, memory)
        if res == INPUT_REQUIRED:
            res, instr_idx = execute_instruction(instr_idx, memory, inputs[input_idx])
            input_idx += 1
        elif res != None:
            out.append(res)
    return out


# executes a single instruction and returns the output and the next index of the next instruction
def execute_instruction(instr_idx, memory, in_buf=None):
    op = memory[instr_idx]
    op_len = int(math.log10(op))+1

    op_code, param_modes = get_op_code_and_param_modes(op)

    params = get_params(instr_idx, param_modes, memory)
    out = NO_OUTPUT
    if op_code == ADD:
        memory[memory[instr_idx+3]] = params[0] + params[1]
    elif op_code == MULT:
        memory[memory[instr_idx+3]] = params[0] * params[1]
    elif op_code == INPUT:
        if in_buf != None:
            memory[memory[instr_idx+1]] = in_buf
        else:
            return INPUT_REQUIRED, instr_idx
    elif op_code == OUTPUT:
        out = params[0]
    elif op_code == JUMP_IF_TRUE:
        instr_idx = params[1] if params[0] != 0 else instr_idx + PARAM_COUNT[op_code] + 1
    elif op_code == JUMP_IF_FALSE:
        instr_idx = params[1] if params[0] == 0 else instr_idx + PARAM_COUNT[op_code] + 1
    elif op_code == LESS_THAN:
        memory[memory[instr_idx+3]] = 1 if params[0] < params[1] else 0
    elif op_code == EQUALS:
        memory[memory[instr_idx+3]] = 1 if params[0] == params[1] else 0
    elif op_code == HALT:
        return NO_OUTPUT, None
    else:
        raise AssertionError('opcode {} does not exist. You messed up :('.format(op_code))

    # update instruction index if not already done by operation
    if op_code != JUMP_IF_TRUE and op_code != JUMP_IF_FALSE:
        instr_idx += PARAM_COUNT[op_code] + 1

    return out, instr_idx


def get_op_code_and_param_modes(op):
    op_len = int(math.log10(op))+1
    if op_len >= 3:
        op_code = op % 10
        param_modes = [int(x) for x in str(op)][-3::-1]
        param_modes += [0]*(PARAM_COUNT[op_code]-len(param_modes))
    else:
        op_code = op
        param_modes = [0]*PARAM_COUNT[op_code]
    return op_code, param_modes


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
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 7, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    memory = read_from_file(args.input)
    max_thruster_output = calc_max_thruster_output(range(0,5), memory)
    print(max_thruster_output)