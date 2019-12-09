import argparse
from itertools import permutations
import math
from functools import reduce
from collections import deque


# intcode instructions
ADD = 1
MULT = 2
INPUT = 3
OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUALS = 8
HALT = 99


# instruction parameter count
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


# parameter modes
POSITION_MODE = 0
IMMEDIATE_MODE = 1


# output codes
OK = 1j
INPUT_REQUIRED = -1j
HALTED = 2j


def read_from_file(fp):
    with open(fp, 'r') as f:
        return list(map(int, f.read().split(',')))


# calculate the thruster output for all possible permutations of inputs
def calc_max_thruster_output(valid_inputs, memory):
    return reduce(lambda x, y: max(x, calc_phase_sequence_output(memory, y, 0)[-1]), permutations(valid_inputs), 0)


# executes the program until reaching a halt operation and returns the recorded output as a list
def calc_phase_sequence_output(memory, phase_seq, input):
    memory_pool = [memory.copy() for __ in range(len(phase_seq))]
    instr_idcs = [0]*len(memory_pool)

    # initialize programs
    for i in range(len(memory_pool)):
        __, instr_idcs[i] = init_program(instr_idcs[i], memory_pool[i], [phase_seq[i]])
    
    signal = deque([input])
    # one loop of the pipeline
    while any(idx != None for idx in instr_idcs):
        # execute each program sequentially
        for i in range(len(memory_pool)):
            signal, instr_idcs[i] = execute_until_halted(instr_idcs[i], memory_pool[i], signal)
    return signal


# initalizes a program by running it until the first required input and supplying a specifed input parameter
def init_program(instr_idx, memory, input: list):
    in_buf = deque(input)
    out_buf = deque()
    while instr_idx != None:
        res, instr_idx = execute_instruction(instr_idx, memory, in_buf, out_buf)
        if res == INPUT_REQUIRED:
            break
    return out_buf, instr_idx


# executes a program until input is required or it halts and return the output and the index of the next instruction
def execute_until_halted(instr_idx, memory, input: list):
    in_buf = deque(input)
    out_buf = deque()
    res = OK
    while instr_idx != None and res != HALTED and res != INPUT_REQUIRED:
        res, instr_idx = execute_instruction(instr_idx, memory, in_buf, out_buf)        
    return out_buf, instr_idx


# executes a single instruction and returns the status and the index of the next instruction
def execute_instruction(instr_idx, memory, in_buf=deque(), out_buf=deque()):
    op = memory[instr_idx]
    op_len = int(math.log10(op))+1

    op_code, param_modes = get_op_code_and_param_modes(op)

    params = get_params(instr_idx, param_modes, memory)
    if op_code == ADD:
        memory[memory[instr_idx+3]] = params[0] + params[1]
    elif op_code == MULT:
        memory[memory[instr_idx+3]] = params[0] * params[1]
    elif op_code == INPUT:
        if len(in_buf) <= 0:
            return INPUT_REQUIRED, instr_idx 
        else:
            memory[memory[instr_idx+1]] = in_buf.popleft()
    elif op_code == OUTPUT:
        out_buf.append(params[0])
    elif op_code == JUMP_IF_TRUE:
        instr_idx = params[1] if params[0] != 0 else instr_idx + PARAM_COUNT[op_code] + 1
    elif op_code == JUMP_IF_FALSE:
        instr_idx = params[1] if params[0] == 0 else instr_idx + PARAM_COUNT[op_code] + 1
    elif op_code == LESS_THAN:
        memory[memory[instr_idx+3]] = 1 if params[0] < params[1] else 0
    elif op_code == EQUALS:
        memory[memory[instr_idx+3]] = 1 if params[0] == params[1] else 0
    elif op_code == HALT:
        return HALTED, None
    else:
        raise AssertionError('opcode {} does not exist. You messed up :('.format(op_code))

    # update instruction index if not already done by operation
    if op_code != JUMP_IF_TRUE and op_code != JUMP_IF_FALSE:
        instr_idx += PARAM_COUNT[op_code] + 1

    return OK, instr_idx


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
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 7, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    memory = read_from_file(args.input)
    max_thruster_output = calc_max_thruster_output(range(5,10), memory)
    print(max_thruster_output)