from enum import Enum
from itertools import pairwise
import sys


class Direction(Enum):
    North = complex(-1, 0)
    East = complex(0, 1)
    South = complex(1, 0)
    West = complex(0, -1)



def get_neighbours(position: complex):
    """
    Generate the neighbouring coordinates of a `position`
    """
    for direction in Direction:
        yield position + direction.value



def get_rows(group: set[complex]):
    """
    For each row of coordinates in the `group` yield a list of the columns
    that the row contains
    """
    # sort the coordinates first by row, then by column
    group = sorted(group, key=lambda position: (position.real, position.imag))
    # the current row
    row = group[0].real
    # the index where the elements of the current row begin
    start = 0
    for end, element in enumerate(group):
        if element.real > row:
            # the first element of the next row has been encountered
            row += 1
            # slice the coordinates [start, end) for the row that ended
            # and yield the columns
            yield [int(position.imag) for position in group[start: end]]
            # mark the start of the new row
            start = end
    # the slice of columns for the final row
    yield [int(position.imag) for position in group[start:]]


def nb_groups(columns: list[int]) -> int:
    """
    Return the number of separate groups of consequtive `columns`
    """
    return 1 + sum(
        1 for previous_column, column in pairwise(columns)
        if column != previous_column + 1
    )


def trace_row_pair(top_row_columns: list[complex], bottom_row_columns: list[complex]):
    """
    Compare the columns of two consecutive rows and determine the number of
    new vertical and horizontal sides the new "bottom" row contributes 
    """
    new_vertical = 0
    new_horizontal = 0

    top_row_columns_set = set(top_row_columns)
    bottom_row_columns_set = set(bottom_row_columns)

    # check the first column in the bottom row: add a (left) vertical side if
    # it is not an extension of a side just above it
    first_bottom_column = bottom_row_columns[0]
    if (
        first_bottom_column not in top_row_columns_set or
        first_bottom_column - 1 in top_row_columns_set
    ):
        new_vertical += 1

    # traverse every pair of columns in the bottom row
    # (to check for new vertical sides)
    for previous_bottom_column, bottom_column in pairwise(bottom_row_columns):
        if bottom_column != previous_bottom_column + 1:
            # the two columns are not consecutive:
            # - add a (right) vertical side if the left column is
            #   not an extension of the side just above it
            # - add a (left) vertical side if the right column is
            #   not an extension of the side just above it
            if (
                previous_bottom_column not in top_row_columns_set or
                previous_bottom_column + 1 in top_row_columns_set
            ):
                new_vertical += 1
            if (
                bottom_column not in top_row_columns_set or
                bottom_column - 1 in top_row_columns_set
            ):
                new_vertical += 1

    # traverse every pair of columns in the bottom row
    # (to check for new horizontal sides)
    for previous_bottom_column, bottom_column in pairwise([-2] + bottom_row_columns):
        if bottom_column not in top_row_columns_set:
            # there is no block above the current column:
            # add a horizontal side if this is the first such column
            if (
                bottom_column != previous_bottom_column + 1 or
                previous_bottom_column in top_row_columns_set
            ):
                new_horizontal += 1

    # traverse every pair of columns in the top row
    # (to check for new horizontal sides)
    for previous_top_column, top_column in pairwise([-2] + top_row_columns):
        if top_column not in bottom_row_columns_set:
            # there is no block below the current column:
            # add a horizontal side if this is the first such column
            if (
                top_column != previous_top_column + 1 or
                previous_top_column in bottom_row_columns_set
            ):
                new_horizontal += 1

    # check the last column in the bottom row: add a (right) vertical side if
    # it is not an extension of a side just above it
    last_bottom_column = bottom_row_columns[-1]
    if (
        last_bottom_column not in top_row_columns_set or
        last_bottom_column + 1 in top_row_columns_set
    ):
        new_vertical += 1

    return new_vertical, new_horizontal


def trace(group: set[complex]) -> int:
    """
    Scan a group row-by-row and, for each row, determine the number of
    new vertical and horizontal sides it contributes.
    """
    rows = list(get_rows(group))
    # first line: one horizontal and two vertical sides for each separate
    # group of blocks
    nb_contiguous_first = nb_groups(rows[0])
    nb_horizontal = nb_contiguous_first
    nb_vertical = 2 * nb_contiguous_first
    if len(rows) > 1:
        # trace pairs of rows
        for previous, current in pairwise(rows):
            new_vertical, new_horizontal = trace_row_pair(previous, current)
            nb_vertical += new_vertical
            nb_horizontal += new_horizontal
    # last line: one horizontal side for each separate group of blocks
    nb_horizontal += nb_groups(rows[-1])
    return nb_vertical + nb_horizontal


def flood(position: complex, map: dict[complex, str]) -> tuple[set[complex], int]:
    """
    Starting from a specific `position` in the `map`, flood the area with the
    same content as the `position`. Return the set of all the coordinates this
    area contains, along with the number of its sides.
    """
    # the starting symbol
    symbol = map[position]
    # the set of coordinates in the area
    visited = set()
    # the frontier of the flood
    frontier = {position}
    while frontier:
        current = frontier.pop()
        visited.add(current)
        # extend the frontier with all the neighbours of the current position
        # with the same content, that have not already been visited
        neighbours = {
            neighbour
            for neighbour in get_neighbours(current)
            if map.get(neighbour) == symbol and neighbour not in frontier
        }
        frontier.update(neighbours - visited)
    return visited, trace(visited)


# read the input into a mapping of each coordinate to the symbol it contains
with open(sys.argv[1]) as file:
    map = {}
    for row, line in enumerate(file):
        for column, symbol in enumerate(line.strip()):
            map[complex(row, column)] = symbol

result = 0
# gather all the coordinates found in the map into a set
unprocessed = set(map.keys())
while unprocessed:
    # pick one coordinate
    current = unprocessed.pop()
    # start flooding from the current coordinate and gather
    # the group of coordinates with the same symbol and the
    # number of sides for the group
    group, sides = flood(current, map)
    unprocessed.difference_update(group)
    result += len(group) * sides
print(result)
