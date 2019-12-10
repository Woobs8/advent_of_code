import argparse
from itertools import permutations
import math
from functools import reduce
from collections import deque
from typing import Union
from enum import Enum

class IntcodeComputer():
    class INSTRUCTIONS():
        ADD = 1
        MULT = 2
        INPUT = 3
        OUTPUT = 4
        JUMP_IF_TRUE = 5
        JUMP_IF_FALSE = 6
        LESS_THAN = 7
        EQUALS = 8
        ADJUST_REL = 9
        HALT = 99

    # instruction parameter count
    PARAM_COUNT = {
        INSTRUCTIONS.ADD:3,
        INSTRUCTIONS.MULT:3,
        INSTRUCTIONS.INPUT:1,
        INSTRUCTIONS.OUTPUT:1,
        INSTRUCTIONS.JUMP_IF_TRUE:2,
        INSTRUCTIONS.JUMP_IF_FALSE:2,
        INSTRUCTIONS.LESS_THAN:3,
        INSTRUCTIONS.EQUALS:3,
        INSTRUCTIONS.ADJUST_REL:1,
        INSTRUCTIONS.HALT:0,
    }

    class PARAMETER_MODES():
        POSITION_MODE = 0
        IMMEDIATE_MODE = 1
        RELATIVE_MODE = 2

    class OUTPUT_CODES():
        OK = 1
        INPUT_REQUIRED = 2
        HALTED = 3


    def __init__(self, memory:list, instr_idx:int=0, rel_base:int=0):
        self.memory = memory
        self.instr_idx = instr_idx
        self.relative_base = rel_base


    # executes the program until reaching a halt operation
    def execute(self, input:list, out:list) -> int:
        in_buf = deque(input)
        res = IntcodeComputer.OUTPUT_CODES.OK
        while self.instr_idx != None and res !=IntcodeComputer.OUTPUT_CODES.HALTED and res !=IntcodeComputer.OUTPUT_CODES.HALTED:
            res, self.instr_idx, self.relative_base = IntcodeComputer._execute_instruction(self.instr_idx, 
                                                                self.memory, 
                                                                self.relative_base, 
                                                                in_buf=in_buf, 
                                                                out_buf=out)
        return res


    # executes a single instruction and returns the status and the index of the next instruction
    @classmethod
    def _execute_instruction(cls, instr_idx:int, memory:list, rel_base:int, in_buf:deque=deque(), out_buf:list=[]) -> Union[int, int, int]:
        op = memory[instr_idx]
        op_len = int(math.log10(op))+1

        op_code, param_modes = cls._get_op_code_and_param_modes(op)

        params = cls._get_params(instr_idx, memory, rel_base, op_code, param_modes)
        if op_code == cls.INSTRUCTIONS.ADD:
            memory[params[2]] = params[0] + params[1]
        elif op_code == cls.INSTRUCTIONS.MULT:
            memory[params[2]] = params[0] * params[1]
        elif op_code == cls.INSTRUCTIONS.INPUT:
            if len(in_buf) <= 0:
                return cls.OUTPUT_CODES.INPUT_REQUIRED, instr_idx, rel_base 
            else:
                memory[params[0]] = in_buf.popleft()
        elif op_code == cls.INSTRUCTIONS.OUTPUT:
            out_buf.append(params[0])
        elif op_code == cls.INSTRUCTIONS.JUMP_IF_TRUE:
            instr_idx = params[1] if params[0] != 0 else instr_idx + cls.PARAM_COUNT[op_code] + 1
        elif op_code == cls.INSTRUCTIONS.JUMP_IF_FALSE:
            instr_idx = params[1] if params[0] == 0 else instr_idx + cls.PARAM_COUNT[op_code] + 1
        elif op_code == cls.INSTRUCTIONS.LESS_THAN:
            memory[params[2]] = 1 if params[0] < params[1] else 0
        elif op_code == cls.INSTRUCTIONS.EQUALS:
            memory[params[2]] = 1 if params[0] == params[1] else 0
        elif op_code == cls.INSTRUCTIONS.ADJUST_REL:
            rel_base += params[0]
        elif op_code == cls.INSTRUCTIONS.HALT:
            return cls.OUTPUT_CODES.HALTED, None, rel_base
        else:
            raise AssertionError('opcode {} does not exist. You messed up :('.format(op_code))

        # update instruction index if not already done by operation
        if op_code != cls.INSTRUCTIONS.JUMP_IF_TRUE and op_code != cls.INSTRUCTIONS.JUMP_IF_FALSE:
            instr_idx += cls.PARAM_COUNT[op_code] + 1
        return cls.OUTPUT_CODES.OK, instr_idx, rel_base


    @classmethod
    def _get_op_code_and_param_modes(cls, op:int) -> Union[int, list]:
        op_len = int(math.log10(op))+1
        if op_len >= 3:
            op_code = op % 10
            param_modes = [int(x) for x in str(op)][-3::-1]
            param_modes += [0]*(cls.PARAM_COUNT[op_code]-len(param_modes))
        else:
            op_code = op
            param_modes = [0]*cls.PARAM_COUNT[op_code]
        return op_code, param_modes


    # returns list of params for specified parameter mode
    @classmethod
    def _get_params(cls, instr_idx:int, memory:list, rel_base:int, op_code:int, param_modes:list) -> list:
        params = []
        for i, mode in enumerate(param_modes, 1):
            if mode == cls.PARAMETER_MODES.POSITION_MODE:
                param_idx = memory[instr_idx+i]
            elif mode == cls.PARAMETER_MODES.IMMEDIATE_MODE:
                param_idx = instr_idx+i
            elif mode == cls.PARAMETER_MODES.RELATIVE_MODE:
                param_idx = memory[instr_idx+i]+rel_base
            else: 
                raise AssertionError('parameter mode {} does not exist. You messed up :('.format(mode))
            
            if param_idx >= len(memory):
                memory.extend([0]*(param_idx-len(memory)+1))

            if (op_code in {cls.INSTRUCTIONS.ADD, cls.INSTRUCTIONS.MULT, cls.INSTRUCTIONS.INPUT, cls.INSTRUCTIONS.LESS_THAN, cls.INSTRUCTIONS.EQUALS} 
                and cls.PARAM_COUNT[op_code] == i):
                params.append(param_idx)
            else:
                params.append(memory[param_idx])

        return params


def read_from_file(fp:str) -> list:
    with open(fp, 'r') as f:
        return list(map(int, f.read().split(',')))


def BOOST_program(memory:list) -> int:
    program = IntcodeComputer(memory)
    out = []
    res = program.execute([2], out)
    return out.pop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 9, part 2')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    memory = read_from_file(args.input)
    keycode = BOOST_program(memory)
    print(keycode)