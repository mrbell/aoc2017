"""
2017 Advent Of Code, day 23
https://adventofcode.com/2017/day/23
Michael Bell
12/28/2017
Solution 1 passed, working on solution 2
"""


class Coprocessor(object):
    def __init__(self, debug_mode=True):
        self.registers = [0] * 8
        self.register_names = [letter for letter in 'abcdefgh']
        if not debug_mode:
            self.set_register('a', 1)

    def get_register(self, reg):
        return self.registers[self.reg_index(reg)]

    def reg_index(self, reg):
        return self.register_names.index(reg)
    
    def set_register(self, reg, val):
        ndx = self.reg_index(reg)
        self.registers[ndx] = val

    def multiply_register(self, reg, val):
        ndx = self.reg_index(reg)
        self.registers[ndx] *= val
    
    def sub_from_register(self, reg, val):
        ndx = self.reg_index(reg)
        self.registers[ndx] -= val

    def _get_op_params(self, X, Y):
        try:
            params = {'reg': X, 'val': int(Y)}
        except ValueError:
            params = {'reg': X, 'val': self.get_register(Y)}
        return params

    def jump_instructions(self, test_val, offset):
        if test_val != 0:
            return offset
        else:
            return 1

    def parse_instruction(self, instruction):

        parts = instruction.split()

        if parts[0] == 'set':
            func = self.set_register
            params = self._get_op_params(*parts[1:])

        elif parts[0] == 'sub':
            func = self.sub_from_register
            params = self._get_op_params(*parts[1:])

        elif parts[0] == 'mul':
            func = self.multiply_register
            params = self._get_op_params(*parts[1:])
            
        elif parts[0] == 'jnz':
            func = self.jump_instructions

            try:
                test_val = int(parts[1])
            except ValueError:
                test_val = self.get_register(parts[1])

            try:
                offset = int(parts[2])
            except ValueError:
                offset = self.get_register(parts[2])

            params = {'test_val': test_val, 'offset': offset}

        else:
            raise ValueError('Unrecognized instruction')
    
        return func, params
    
    def execute_program(self, program, return_first=True):

        if isinstance(program, str):
            program = program.replace('\r', '').split('\n')
        
        current_instruction = 0
        mul_invocations = 0

        while current_instruction >= 0 and current_instruction < len(program):
            func, params = self.parse_instruction(program[current_instruction])
            
            res = func(**params)

            if func == self.multiply_register:
                mul_invocations += 1
            
            if func == self.jump_instructions:
                current_instruction += res
            else:
                current_instruction += 1
        
        return mul_invocations


with open('data/day23_input.txt', 'r') as f:
    PUZZLE_INPUT = f.read()


if __name__ == '__main__':

    coproc = Coprocessor()
    print("Solution 1: {:}".format(coproc.execute_program(PUZZLE_INPUT)))

    coproc = Coprocessor(False)
    mul_invocations = coproc.execute_program(PUZZLE_INPUT)
    print(mul_invocations)
    print('Solution 2: {:}'.format(coproc.get_register('h')))