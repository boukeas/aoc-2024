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
        self.outputs.append(self.combo(operand) % 8)

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
        return ",".join(str(number) for number in self.outputs)



register_re = re.compile(r"^Register (?P<register>[A-C]): (?P<contents>[0-9]+)$")

registers = {}
with open(sys.argv[1]) as file:
    for _ in range(3):
        register, contents = register_re.match(file.readline().strip()).groups()
        registers[register] = int(contents)
    file.readline()
    program = [int(item) for item in file.readline()[8:].strip().split(",")]


"""
This is the program and what it does in every iteration, until A equals 0:

2,4 -> bst 4 -> B = A % 8   
1,5 -> bxl 5 -> B = B ^ 5
7,5 -> cdv 5 -> C = A // (2 ** B)
4,1 -> bxc 1 -> B = B ^ C
1,6 -> bxl 6 -> B = B ^ 6
5,5 -> out 5 -> print(B % 8)
0,3 -> adv 3 -> A = A // (2 ** 3)

In every iteration, values for B and C are derived in terms of A and then
A is divided by 8.

This algorithm works backwards from the final iteration, where A equals 0.
In each iteration it works out a set of candidate As for the previous
iteration (they are all the As that lead to the current candidate As when
they are divided by 8), executes a single pass of the program and only keeps
the As that would produce the required output.
"""

candidate_As = {0}
for i in range(len(program)):
    # this is what the program should output in this iteration
    # (the i-th instruction from the end of the program)
    target = program[-(i+1)]
    new_candidate_As = set()
    for candidate_A in candidate_As:
        # for all the A that could lead to this A when divided by 8...
        for A in range(candidate_A * 8, (candidate_A + 1) * 8):
            # replay a single pass
            B = A % 8
            B = B ^ 5
            C = A // (2**B)
            B = B ^ C
            B = B ^ 6
            # only keep this A as a candidate A if it would produce
            # the required output
            if B % 8 == target:
                new_candidate_As.add(A)
    candidate_As = new_candidate_As

A = min(candidate_As)
print(f"{A=}")

# verify that this A actually outputs the program
computer = Computer(registers={"A": A, "B": 0, "C": 0}, program=program)
target_output = program
actual_output = computer.outputs
print(f"{actual_output=} {target_output=} {actual_output==target_output}")