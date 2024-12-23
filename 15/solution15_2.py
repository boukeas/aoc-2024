from enum import Enum
import sys


class Direction(Enum):
    North = complex(-1, 0)
    East = complex(0, 1)
    South = complex(1, 0)
    West = complex(0, -1)


def input_map(file):
    """
    Parse input file and create a mapping of coordinates to contents
    (coordinates are represented with complex numbers)
    """
    map = {}
    for row, line in enumerate(file):
        if not line.strip():
            break
        for column, contents in enumerate(line):
            if contents != '.':
                if contents == '@':
                    robot = complex(row, column * 2)
                elif contents == "#":
                    map[complex(row, 2 * column)] = "#"
                    map[complex(row, 2 * column + 1)] = "#"
                elif contents == "O":
                    map[complex(row, 2 * column)] = "["
                    map[complex(row, 2 * column + 1)] = "]"
    return robot, map, row, 2 * column


def input_moves(file):
    """
    Parse input file and generate a sequence of moves (i.e. directions)
    """
    for line in file:
        line = line.strip()
        yield from (
            {
                "^": Direction.North,
                ">": Direction.East,
                "v": Direction.South,
                "<": Direction.West
            }[symbol]
            for symbol in line
        )


def display(robot, map, nb_rows, nb_columns):
    for row in range(nb_rows):
        for column in range(nb_columns):
            position = complex(row, column)
            if position == robot:
                print("@", end="")
                continue
            try:
                print(map[position], end="")
            except KeyError:
                print(".", end="")
        print()


def perform_move(robot: complex, direction: Direction, map: dict[complex, str]) -> complex:
    """
    Modify `map` and return the new robot position after a move
    towards `direction`
    """
    adjacent_position = robot + direction.value
    # differentiate between East/West and North/South moves
    if direction in {Direction.East, Direction.West}:
        # probe in the direction of movement and keep a record of probed positions
        # (in this case it is one position per probe-step)
        free_to_move = None
        probe_position = adjacent_position
        record = []
        while free_to_move is None:
            try:
                probe = map[probe_position]
                if probe == "#":
                    # the probe has hit a wall: there will be no movement
                    free_to_move = False
                else:
                    # keep probing in the direction of movement
                    probe_position += direction.value
                    record.append(probe_position)
            except KeyError:
                # the probe has discovered an empty space:
                # the robot (and possibly boxes) are free to move
                free_to_move = True
        if not free_to_move:
            return robot
        # shift all probed positions towards the direction of movement
        for probe_position in reversed(record):
            map[probe_position] = map[probe_position - direction.value]
            del map[probe_position - direction.value]
    else:
        # probe towards the direction of movement, and keep a record of probed positions
        # (in this case, it is a *set* of positions per probe-step, as the probe spreads
        # across a frontier of boxes that might push each other)
        free_to_move = None
        probe_positions = {adjacent_position}
        record = []
        while free_to_move is None:
            next_probe_positions = set()
            for probe_position in probe_positions:
                try:
                    probe = map[probe_position]
                    if probe == "#":
                        # the probe has hit a wall: there will be no movement
                        free_to_move = False
                    else:
                        # add to the set of positions that will need to be probed in the next step
                        if probe == "[":
                            next_probe_positions.add(probe_position + direction.value)
                            next_probe_positions.add(probe_position + direction.value  + direction.East.value)
                        else:
                            next_probe_positions.add(probe_position + direction.value)
                            next_probe_positions.add(probe_position + direction.value  + direction.West.value)
                except KeyError:
                    pass
            if free_to_move is None and not next_probe_positions:
                # all probed positions in the latest step are empty:
                # the robot (and possibly boxes) are free to move
                free_to_move = True
            else:
                # keep probing in the direction of movement
                record.append(next_probe_positions)
                probe_positions = next_probe_positions
        if not free_to_move:
            return robot
        # shift all probed positions towards the direction of movement
        for probe_positions in reversed(record):
            for probe_position in probe_positions:
                map[probe_position] = map[probe_position - direction.value]
                del map[probe_position - direction.value]
    # return the new robot position
    return adjacent_position


with open(sys.argv[1]) as file:
    robot, map, nb_rows, nb_columns = input_map(file)
    # display(robot, map, nb_rows, nb_columns)
    for move in input_moves(file):
        robot = perform_move(robot, move, map)
        # print(move)

result = sum(
    int(position.real * 100 + position.imag)
    for position, content in map.items()
    if content == "["
)
print(result)
