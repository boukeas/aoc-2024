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
    # read first part of the input as Constant components
    for line in file:
        line = line.strip()
        if not line:
            break
        match = wire_re.match(line)
        name, value = match.groups()
        Constant(name, value=bool(int(value)))

    # read second part of the input as different types of Gate components
    for line in file:
        line = line.strip()
        match = gate_re.match(line)
        input1, gate, input2, name = match.groups()
        gate_cls = gate_map[gate]
        gate_cls(name, [input1, input2])

number_x = digits_to_decimal(activate("x"))
number_y = digits_to_decimal(activate("y"))
result = digits_to_decimal(activate("z"))
print(number_x)
print(number_y)
print(result)
