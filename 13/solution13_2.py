from fractions import Fraction
import re
import sys


def solve_2x2(a1, b1, c1, a2, b2, c2) -> tuple[int, int]:
    """
    Solves a 2x2 system of linear equations with integer solutions:
    a1x + b1y = c1
    a2x + b2y = c2
    ref: https://en.wikipedia.org/wiki/Cramer%27s_rule#Explicit_formulas_for_small_systems
    """
    # determinant
    det = a1 * b2 - a2 * b1
    if det == 0:
        return None
    # use Cramer's rule with fractions for simplification and exact arithmetic
    x = Fraction(c1 * b2 - b1 * c2, det)
    y = Fraction(a1 * c2 - c1 * a2, det)
    if x.denominator != 1 or y.denominator != 1:
        return None
    return (int(x), int(y))


# regular expressions to parse the button an prize input lines
button_re = re.compile(r"^.*: X\+(?P<x>[0-9]+), Y\+(?P<y>[0-9]+)$")
prize_re = re.compile(r"^.*: X=(?P<x>[0-9]+), Y=(?P<y>[0-9]+)$")

tokens = 0
with open(sys.argv[1]) as file:
    lines = iter(file)
    while True:
        # button A: get constant x and y offsets (cx_A and cy_A)
        line = next(lines)
        match = button_re.match(line)
        cx_A, cy_A = (int(num_str) for num_str in match.groups())
        # button B: get constant x and y offsets (cx_B and cy_B)
        line = next(lines)
        match = button_re.match(line)
        cx_B, cy_B = (int(num_str) for num_str in match.groups())
        # prize: get x and y coordinates
        line = next(lines)
        match = prize_re.match(line)
        x, y = (int(num_str) for num_str in match.groups())
        # part two: add constant offset
        x += 10000000000000
        y += 10000000000000
        # we have a 2x2 linear system to which we seek integer solutions,
        # i.e. the number of button presses for buttons A and B
        # cx_A * A + cx_B * B = x
        # cy_A * A + cy_B * B = y
        solution = solve_2x2(cx_A, cx_B, x, cy_A, cy_B, y)
        if solution is not None:
            A, B = solution
            tokens += 3*A + B
        try:
            line = next(lines)
        except StopIteration:
            break

print(tokens)
