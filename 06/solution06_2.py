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


def tour_cycle(position, direction, visited) -> bool:
    """
    Perform a tour starting from `position`, facing towards `direction` and return
    True if a loop is detected or False otherwise. The `visited` argument is a
    record of previously visited positions and directions and is not modified
    when simulating the tour (an additional local record is kept instead).
    """
    local_visited = defaultdict(set)
    local_visited[position].add(direction)
    for current_position, current_direction in tour(position, direction):
        if current_direction in local_visited[current_position] or current_direction in visited:
            return True
        local_visited[current_position].add(current_direction)
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
# map each position to a set of directions in which they have been traversed
# (for cycle detection)
visited = defaultdict(set, {start_position: {Direction.North}})
# perform a tour and, for every step of the tour...
for position, direction in tour(start_position, Direction.North):
    if direction in visited[position]:
        continue
    visited[position].add(direction)
    # ... look ahead one step to the position where the obstacle will be placed
    obstacle_position = move(position, direction)
    try:
        # make sure the obstacle will be in the grid, in a position that doesn't
        # interrupt the current trajectory and no obstacle is already there
        if data[obstacle_position] != "#" and not visited[obstacle_position]:
            # place the obstacle
            data[obstacle_position] = "#"
            # and simulate the rest of the trajectory
            if tour_cycle(position, turn_right(direction), visited):
                result += 1
            # remove the obstacle before continuing
            data[obstacle_position] = "."
    except KeyError:
        pass

print(result)
