from collections import defaultdict


from collections import defaultdict

class Instruction:
    def __init__(self, instruction: str):
        params = instruction.split(' ')
        self.instruction = params[0]
        if self.instruction == 'inp':
            self.operand1 = None
            self.operand2 = None
            self.target = params[1]
        elif self.instruction in ['add', 'mul', 'div', 'mod', 'eql']:
            self.operand1 = params[1]
            self.operand2 = params[2]
            self.target = params[1]

class ALU:
    def __init__(self, instructions: list):
        self.instructions = instructions
        self.reset()

    def reset(self):
        self.program_pointer = 0
        self.memory = {'w': 0 ,'x': 0, 'y': 0, 'z': 0}
    
    def MONAD(self, input: int) -> bool:
        input_pointer = 0
        for instr in self.instructions:
            instr:Instruction
            if instr.instruction == 'inp':
                value = input[input_pointer]
                input_pointer += 1
                self._inp(value, instr.target)
            elif instr.instruction == 'add':
                self._add(instr.operand1, instr.operand2, instr.target)
            elif instr.instruction == 'mul':
                self._mul(instr.operand1, instr.operand2, instr.target)
            elif instr.instruction == 'div':
                self._div(instr.operand1, instr.operand2, instr.target)
            elif instr.instruction == 'mod':
                self._mod(instr.operand1, instr.operand2, instr.target)
            elif instr.instruction == 'eql':
                self._eql(instr.operand1, instr.operand2, instr.target)
        return self.memory['z'] == 0

    def _inp(self, value: int, target: str) -> None:
        self.memory[target] = value

    def _add(self, operand1: str, operand2: str, target: str) -> None:
        if operand2 in self.memory.keys():
            self.memory[target] = self.memory[operand1] + self.memory[operand2]
        else:
            self.memory[target] = self.memory[operand1] + int(operand2)
    
    def _mul(self, operand1: str, operand2: str, target: str) -> None:
        if operand2 in self.memory.keys():
            self.memory[target] = self.memory[operand1] * self.memory[operand2]
        else:
            self.memory[target] = self.memory[operand1] * int(operand2)

    def _div(self, operand1: str, operand2: str, target: str) -> None:
        if operand2 in self.memory.keys():
            self.memory[target] = self.memory[operand1] // self.memory[operand2]
        else:
            self.memory[target] = self.memory[operand1] // int(operand2)

    def _mod(self, operand1: str, operand2: str, target: str) -> None:
        if operand2 in self.memory.keys():
            self.memory[target] = self.memory[operand1] % self.memory[operand2]
        else:
            self.memory[target] = self.memory[operand1] % int(operand2)

    def _eql(self, operand1: str, operand2: str, target: str) -> None:
        if operand2 in self.memory.keys():
            self.memory[target] = 1 if self.memory[operand1] == self.memory[operand2] else 0
        else:
            self.memory[target] = 1 if self.memory[operand1] == int(operand2) else 0