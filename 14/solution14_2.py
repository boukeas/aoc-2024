from collections import Counter
from functools import reduce
from operator import mul as product
import re
import sys
from time import sleep


# $ python3 solution14_2.py input14.txt 101 103


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


def display(robots):
    # display the area with the robots as asterisks
    positions = {position for position, _ in robots}
    for x in range(dim_x):
        for y in range(dim_y):
            if complex(x, y) in positions:
                print("*", end="")
            else:
                print(".", end="")
        print()


# command-line arguments: dimensions and number of simulation steps
dim_x = int(sys.argv[2])
dim_y = int(sys.argv[3])


robots = [robot for robot in input_robots()]

# starting step
offset = 8006
robots = [simulate(robot, steps=offset) for robot in robots]

# step-by-step display of the robots
# (in order to visually detect the tree)
step = offset
while step < 8007:
    display(robots)
    print(step)
    robots = [simulate(robot, steps=1) for robot in robots]
    step += 1
    sleep(0.01)
