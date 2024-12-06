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


def tour_cycle(position, direction) -> bool:
    visited = defaultdict(set)
    visited[position].add(direction)
    for current_position, current_direction in tour(position, direction):
        #print(current_position, current_direction)
        if current_direction in visited[current_position]:
            return True
        visited[current_position].add(current_direction)
    return False


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


result = 0
visited = {start_position}
# for every step of the tour...
for position, direction in tour(start_position, Direction.North):
    if position in visited:
        continue
    visited.add(position)
    # ... place a block at that step and check if the tour that starts
    # from the starting position is a loop
    data[position] = "#"
    if tour_cycle(start_position, Direction.North):
        result += 1
    # remove the block
    data[position] = '.'

print(result)
