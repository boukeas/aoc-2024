from collections import defaultdict
from enum import Enum
import sys
from typing import Tuple


class Direction(Enum):
    North = (-1, 0)
    Northeast = (-1, 1)
    East = (0, 1)
    Southeast = (1, 1)
    South = (1, 0)
    Southwest = (1, -1)
    West = (0, -1)
    Northwest = (-1, -1)


Position = Tuple[int, int]


def move(position: Position, direction: Direction) -> Position:
    """
    Return the position you find yourself if you move from `position`
    towards `direction`
    """
    row, column = position
    row_offset, column_offset = direction.value
    return (row + row_offset, column + column_offset)


def turn_right(direction: Direction) -> Direction:
    return {
        Direction.North: Direction.East,
        Direction.East: Direction.South,
        Direction.South: Direction.West,
        Direction.West: Direction.North
    }[direction]


def tour(position: Position, direction: Direction) -> Tuple[Position, Direction]:
    """
    Generate the position, direction pairs you encounter on a tour that starts
    from `position`, facing towards `direction`
    """
    while True:
        new_position = move(position, direction)
        try:
            if data[new_position] != '#':
                position = new_position
            else:
                direction = turn_right(direction)
            yield position, direction
        except KeyError:
            break


# read the input as a dict mapping (row, column) coordinates to their contents
with open(sys.argv[1]) as file:
    data = {}
    start_position = None
    for row, line in enumerate(file):
        for column, letter in enumerate(line.strip()):
            if letter == '^':
                data[(row, column)] = '.'
                start_position = (row, column)
            else:
                data[(row, column)] = letter

visited = {start_position}
for position, direction in tour(start_position, Direction.North):
    if position in visited:
        continue
    visited.add(position)

result = len(visited)
print(result)
