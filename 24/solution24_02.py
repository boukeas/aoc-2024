import re
import sys


class Component:

    # class attribute for mapping component names to component instances
    components = {}

    def __init__(self, name: str):
        self.components[name] = self

    def activate(self) -> bool:
        raise NotImplementedError


class Constant(Component):

    def __init__(self, name: str, value: bool):
        super().__init__(name)
        self.value = value

    def activate(self) -> bool:
        return self.value


class Gate(Component):

    def __init__(self, name: str, inputs: list[str]):
        super().__init__(name)
        self.inputs = inputs

    @staticmethod
    def gate_function(a: bool, b: bool) -> bool:
        raise NotImplementedError

    def activate(self) -> bool:
        return self.gate_function(
            *(
                self.components[component_name].activate()
                for component_name in self.inputs
            )
        )


class AndGate(Gate):
    @staticmethod
    def gate_function(a: bool, b: bool) -> bool:
        return a and b


class OrGate(Gate):
    @staticmethod
    def gate_function(a: bool, b: bool) -> bool:
        return a or b


class XorGate(Gate):
    @staticmethod
    def gate_function(a: bool, b: bool) -> bool:
        return a ^ b


def decimal_to_digits(decimal: int, length: int = None) -> int:
    """
    Return a list of boolean values corresponding to the binary
    representation of `decimal`. Pad to `length` if necessary.
    """
    digits = [
        bool(int(digit)) for digit in bin(decimal)[2:]
    ]
    if length:
        length_difference = length - len(digits)
        if length_difference > 0:
            return [False] * length_difference + digits
    return digits


def digits_to_decimal(digits: list[bool]) -> int:
    """
    Return the decimal number corresponding to the binary number
    represented by `digits`
    """
    binary_str = "".join(str(int(digit)) for digit in digits)
    return int(binary_str, base=2)


def get_component_names(prefix: str):
    """
    Return a sorted list of component names starting with `prefix`
    """
    return sorted(
        (
            component_name
            for component_name in Component.components
            if component_name.startswith(prefix)
        ),
        reverse=True
    )


def activate(prefix: str = "z") -> int:
    """
    Return the list of results collected by calling the `activate` method
    for all components starting with a specific prefix
    """
    return [
        Component.components[component_name].activate()
        for component_name in get_component_names(prefix)
    ]


wire_re = re.compile(r"^(?P<input>.+): (?P<value>[0|1])$")
gate_re = re.compile(r"^(?P<input1>.+) (?P<gate>AND|OR|XOR) (?P<input2>.+) -> (?P<output>.+)$")

gate_map = {
    "OR": OrGate,
    "AND": AndGate,
    "XOR": XorGate
}

with open(sys.argv[1]) as file:
    # ignore the first part of the input
    for line in file:
        if not line.strip():
            break

    # read second part of the input as different types of Gate components
    for line in file:
        line = line.strip()
        match = gate_re.match(line)
        input1, gate, input2, name = match.groups()
        gate_cls = gate_map[gate]
        gate_cls(name, [input1, input2])

for i in range(45):

    # in each iteration, add two identical numbers with just one bit
    # at position i: this should highlight where the wires have been crossed

    number_x = number_y = 2 ** i
    for index, digit in enumerate(reversed(decimal_to_digits(number_x, 45))):
        Constant(f"x{index:02}", digit)
        Constant(f"y{index:02}", digit)

    result = digits_to_decimal(activate("z"))

    print(f"{i=}")
    if number_x + number_y != result:
        print(f"{bin(number_x)[2:]:0>45}")
        print(f"{bin(number_y)[2:]:0>45}")
        print(f"{bin(result)[2:]:0>45}")

"""
Using this program to investigate yields:

i=9
000000000000000000000000000000000001000000000
000000000000000000000000000000000001000000000
000000000000000000000000000000000001000000000

-> because qwf <-> cnk have been swapped

i=13 8192 + 8192 = 32768
000000000000000000000000000000010000000000000
000000000000000000000000000000010000000000000
000000000000000000000000000001000000000000000
i=14 16384 + 16384 = 16384
000000000000000000000000000000100000000000000
000000000000000000000000000000100000000000000
000000000000000000000000000000100000000000000

-> because vhm <-> z14 have been swapped

i=26 67108864 + 67108864 = 268435456
000000000000000000100000000000000000000000000
000000000000000000100000000000000000000000000
000000000000000010000000000000000000000000000
i=27
000000000000000001000000000000000000000000000
000000000000000001000000000000000000000000000
000000000000000001000000000000000000000000000

-> because mps <-> z27 have been swapped

i=38
000000100000000000000000000000000000000000000
000000100000000000000000000000000000000000000
000010000000000000000000000000000000000000000

because z39 <-> msq have been swapped

$ python3
>>> ",".join(sorted(["qwf", "cnk", "vhm", "z14", "mps", "z27", "z39", "msq"]))
'cnk,mps,msq,qwf,vhm,z14,z27,z39'

Running the same program on the corrected input file input24_fix.txt
confirms there are no inconsistencies.

The initial solution to part 1 can be used to confirm the result of the
addition on the fixed input file is correct:

$ python3 solution24_01.py input24.txt
26495111766585
18168650014383
45213383376616

$ python3 solution24_01.py input24_fix.txt
26495111766585
18168650014383
44663761780968
"""