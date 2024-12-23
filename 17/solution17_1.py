import re
import sys


class Computer:

    _combo_map = {4: "A", 5: "B", 6: "C"}

    def __init__(self, registers: dict[str, int], program: list[int]):
        self.registers = registers
        self.outputs = []
        self.ip = 0
        self.jump_flag = False
        self.run(program)

    def combo(self, operand: int):
        return operand if operand <= 3 else self.registers[self._combo_map[operand]]

    def div(self, operand: int) -> int:
        numerator = self.registers['A']
        denominator = 2 ** self.combo(operand)
        return numerator // denominator

    def adv(self, operand: int):
        self.registers['A'] = self.div(operand)

    def bdv(self, operand: int):
        self.registers['B'] = self.div(operand)

    def cdv(self, operand: int):
        self.registers['C'] = self.div(operand)

    def out(self, operand: int):
        self.outputs.append(str(self.combo(operand) % 8))

    def bst(self, operand: int):
        self.registers['B'] = self.combo(operand) % 8

    def jnz(self, operand: int):
        if self.registers['A'] != 0:
            self.ip = operand
            self.jump_flag = True

    def bxl(self, operand: int):
        self.registers['B'] = self.registers['B'] ^ operand

    def bxc(self, operand: int):
        self.registers['B'] = self.registers['B'] ^ self.registers['C']

    _instruction_map = {
        0: adv,
        1: bxl,
        2: bst,
        3: jnz,
        4: bxc,
        5: out,
        6: bdv,
        7: cdv,
    }

    def run(self, program: list[int]):
        size = len(program)
        while self.ip < size:
            instruction_code, operand = program[self.ip: self.ip + 2]
            instruction = self._instruction_map[instruction_code]
            instruction(self, operand)
            if self.jump_flag:
                self.jump_flag = False
            else:
                self.ip += 2

    @property
    def output(self) -> str:
        return ",".join(self.outputs)



register_re = re.compile(r"^Register (?P<register>[A-C]): (?P<contents>[0-9]+)$")

registers = {}
with open(sys.argv[1]) as file:
    for _ in range(3):
        register, contents = register_re.match(file.readline().strip()).groups()
        registers[register] = int(contents)
    file.readline()
    program = [int(item) for item in file.readline()[8:].strip().split(",")]

computer = Computer(registers, program)
result = computer.output
print(result)