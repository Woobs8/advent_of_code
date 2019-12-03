import argparse
from itertools import permutations


ADD = 1
MULT = 2
HALT = 99


def read_from_file(fp):
    with open(fp, 'r') as f:
        return list(map(int, f.read().split(',')))


# recursively execute the program until reaching a halt operation
def execute_program(op_idx, memory):
    op_code = memory[op_idx]
    if op_code == ADD:
        add(memory[op_idx+1], memory[op_idx+2], memory[op_idx+3], memory)
    elif op_code == MULT:
        mult(memory[op_idx+1], memory[op_idx+2], memory[op_idx+3], memory)
    elif op_code == HALT:
        return
    else:
        raise AssertionError('opcode {} does not exist. You messed up :('.format(op_code))
    execute_program(op_idx+4, memory)


def add(source1, source2, target, memory):
    memory[target] = memory[source1] + memory[source2]


def mult(source1, source2, target, memory):
    memory[target] = memory[source1] * memory[source2]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Advent of code 2019 - day 1, part 1')
    parser.add_argument('input', help='path to input file', default='input.txt', nargs='?')
    args = parser.parse_args()

    initial_memory = read_from_file(args.input)
    input_range = range(0,100)

    # naive brute-force approach
    # TODO: consider a more efficient approach
    for i,j in permutations(input_range, 2):
        memory = initial_memory.copy()
        memory[1] = i
        memory[2] = j
        execute_program(0, memory)
        if memory[0] == 19690720:
            print("The correct input is {}".format(100*i+j))
            exit(0)
    
    print("The correct input was not found")