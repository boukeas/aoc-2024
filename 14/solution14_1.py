from collections import Counter
from functools import reduce
from operator import mul as product
import re
import sys


# $ python3 solution14_1.py input14_test.txt 11 7 100
# 12
# $ python3 solution14_1.py input14.txt 101 103 100
# 209409792


def input_robots():
    # generate the robot's position, velocity tuples from the input
    # (position and velocity are represented as complex numbers)
    robot_re = re.compile(r"^p=(?P<px>[0-9]+),(?P<py>[0-9]+) v=(?P<vx>-?[0-9]+),(?P<vy>-?[0-9]+)$")
    with open(sys.argv[1]) as file:
        for line in file:
            px, py, vx, vy = tuple(
                int(number) for number in robot_re.match(line).groups()
            )
            yield complex(px, py), complex(vx, vy)


def simulate(robot: tuple[complex, complex], steps: int):
    # return the robot's position and velocity after `steps` iterations
    # (the velocity remains unchanged but returning it allows for chaining)
    position, velocity = robot
    new_position = position + steps * velocity
    # wrap around the area using the modulos of its dimensions
    return complex(new_position.real % dim_x, new_position.imag % dim_y), velocity


def quadrant(position: complex):
    # return the quadrant that the `position` belongs to
    # (or None if the position is in the middle of the area)
    result = 0
    mid_x = dim_x // 2
    if position.real > mid_x:
        result += 1
    elif position.real == mid_x:
        return None
    mid_y = dim_y // 2
    if position.imag > mid_y:
        result += 2
    elif position.imag == mid_y:
        return None
    return result


# command-line arguments: dimensions and number of simulation steps
dim_x = int(sys.argv[2])
dim_y = int(sys.argv[3])
steps = int(sys.argv[4])

# count the robots in each quadrant after the simulation
quadrants = Counter(
    quadrant(simulate(robot, steps)[0])
    for robot in input_robots()
)
quadrants.pop(None)

# multiply the number of robots in each quadrant to get the result
result = reduce(product, quadrants.values())
print(result)
