from collections import defaultdict
import sys
from itertools import combinations


Position = complex


def out_of_bounds(position: Position) -> bool:
    return (
        position.real < 0 or position.imag < 0 or
        position.real >= nb_rows or position.imag >= nb_columns
    )


def get_directed_antinode(antenna1: Position, antenna2: Position):
    """
    Generate the antinode created from `antenna1` towards the direction
    of `antenna2`
    """
    return antenna1 + (antenna1 - antenna2)


def get_antinodes(antenna1: Position, antenna2: Position):
    """
    Generate the antinodes created from a pair of antennas --
    calls `get_directed_antinode` in both directions
    """
    antinode = get_directed_antinode(antenna1, antenna2)
    if not out_of_bounds(antinode):
        yield antinode
    antinode = get_directed_antinode(antenna2, antenna1)
    if not out_of_bounds(antinode):
        yield antinode


# read the input as a map from antenna families to the coordinates of each
# family's individual antennas
with open(sys.argv[1]) as file:
    antennas = defaultdict(set)
    start_position = None
    for row, line in enumerate(file):
        for column, symbol in enumerate(line.strip()):
            if symbol != ".":
                # store the coordinates as a complex number to allow for
                # vector operations
                antennas[symbol].add(complex(row, column))

# global variables for the size of the grid
nb_rows, nb_columns = row + 1, column + 1

# generate antinodes for each pair of antennas in the same family
antinodes = {
    antinode
    for family in antennas.values()
    for antenna1, antenna2 in combinations(family, r=2)
    for antinode in get_antinodes(antenna1, antenna2)
}

result = len(antinodes)
print(result)
