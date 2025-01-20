from enum import Enum
from functools import cache
from math import inf
import sys
from typing import Callable, Iterable, Optional


def argmin(iterable: Iterable, key: Callable):
    """
    Return a set containing all the elements `element` of `iterable` that
    result in the minimum value for `key(element)`
    """
    elements = iter(iterable)
    try:
        current = next(elements)
    except StopIteration:
        return None
    min_value = key(current)
    result = {current}
    while True:
        try:
            current = next(elements)
        except StopIteration:
            return result
        value = key(current)
        if value < min_value:
            min_value = value
            result = {current}
        elif value == min_value:
            result.add(current)


class Direction(Enum):
    North = complex(-1, 0)
    East = complex(0, 1)
    South = complex(1, 0)
    West = complex(0, -1)

    def opposite(self):
        return Direction(-1 * self.value)


class Map:

    def __init__(self, filename: str):
        with open(filename) as file:
            self.positions = set()
            for row, line in enumerate(file):
                for column, content in enumerate(line.strip()):
                    if content == ".":
                        self.positions.add(complex(row, column))
                    elif content == "S":
                        self.start = complex(row, column)
                        self.positions.add(complex(row, column))
                    elif content == "E":
                        self.end = complex(row, column)
                        self.positions.add(complex(row, column))
            self.size = complex(row, column)

    @cache
    def outgoing(
        self, position: complex, incoming: Optional[Direction] = None
    ) -> tuple[Direction]:
        """
        Return a tuple of directions that would lead from `position` to a
        valid neighbour. If `incoming` is specified, i.e. the opposite of
        `incoming` is left out, i.e. the outgoing direction cannot lead
        back to the previous position.
        """
        if position == self.end:
            return tuple()
        return tuple(
            direction
            for direction in Direction
            if direction.opposite() != incoming
            if position + direction.value in self.positions
        )

    @cache
    def transition(
        self, position: complex, incoming: Direction, outgoing: Direction
    ) -> tuple[complex, Direction, int]:
        """
        Starting from `position`, facing towards `incoming` and moving towards
        `outgoing`, return a tuple that contains the next position that is
        reached (the next junction), the incoming direction and the cost of
        making this transition. Return None if a dead-end is reached instead
        of a junction.
        """
        previous_direction = incoming
        current_position, current_direction = position + outgoing.value, outgoing
        cost = 1 if current_direction == previous_direction else 1001
        while current_position != self.end:
            outgoing = self.outgoing(current_position, current_direction)
            if len(outgoing) == 0:
                return None
            if len(outgoing) > 1:
                return current_position, current_direction, cost
            outgoing = outgoing[0]
            previous_direction = current_direction
            current_position, current_direction = current_position + outgoing.value, outgoing
            cost += 1 if current_direction == previous_direction else 1001
        return current_position, current_direction, cost

    @cache
    def transitions(self, position: complex, incoming: Direction):
        """
        Return a tuple of all the transitions that are possible when
        starting from `position` and facing towards direction `incoming`.
        """
        return tuple(
            transition
            for outgoing in self.outgoing(position, incoming)
            if (transition := self.transition(position, incoming, outgoing))
        )

    def intermediate(
        self, start: complex, outgoing: Direction, end: complex
    ) -> set[complex]:
        """
        Return the set of all positions visited when leaving from `start`,
        facing towards `outgoing`, until position `end'` is reached.
        """
        positions = {start}
        current_position, current_direction = start + outgoing.value, outgoing
        while current_position != end:
            positions.add(current_position)
            outgoing = self.outgoing(current_position, current_direction)[0]
            current_position, current_direction = current_position + outgoing.value, outgoing
        return positions

    def search(self) -> dict[tuple[complex, Direction], int]:
        """
        Return a value map for all (position, direction) combinations.
        The possible positions are the positions of junctions and the value
        of each (position, direction) is the cost of reaching the target
        from that position when facing towards that direction.
        """
        # initial values
        V = {}
        for position in self.positions:
            outgoing = self.outgoing(position)
            if len(outgoing) > 2:
                for direction in outgoing:
                    V[(position, direction.opposite())] = inf
        V[(self.start, Direction.East)] = inf
        for action in Direction:
            V[(self.end, action)] = 0

        # in each iteration, update the value of each (position, direction)
        # with the min value of its neighbouring junctions, plus the cost of
        # reaching each of these junctions
        while True:
            new_V = {}
            for position, incoming in V:
                if position == map.end:
                    new_V[(position, incoming)] = 0
                    continue
                new_V[(position, incoming)] = min(
                    (
                        cost + V[(next_position, next_incoming)]
                        for next_position, next_incoming, cost in self.transitions(position, incoming)
                    ),
                    default=inf
                )
            # the process terminates when the update doesn't result in changes
            if all(
                V[(position, direction)] == new_V[(position, direction)]
                for position, direction in V
            ):
                break
            V = new_V
        return V

    def traverse(self, V):

        def evaluate(transition):
            _, position, direction, cost = transition
            return cost + V[position, direction]

        def _traverse(current_position, current_direction, current_cost):
            """
            Return a set of all the positions visited when following minimum-cost
            paths from the `current_position`, facing towards the `current_direction`
            and having already incurred `current_cost` since the start.
            """
            transitions = argmin(
                (
                    (outgoing, transition[0], transition[1], transition[2] + current_cost)
                    for outgoing in self.outgoing(current_position, current_direction)
                    if (transition := self.transition(current_position, current_direction, outgoing))
                ),
                key=evaluate
            )
            if not transitions:
                return {current_position}
            positions = set()
            for outgoing, next_position, next_direction, next_cost in transitions:
                positions.update(map.intermediate(current_position, outgoing, next_position))
                positions.update(_traverse(next_position, next_direction, next_cost))
            return positions

        return _traverse(map.start, Direction.East, 0)


map = Map(sys.argv[1])
V = map.search()

# result for part I: the minimum cost of reaching the destination
# is the value of being in the starting position facing East
print(V[map.start, Direction.East])

# result for part II: compute the number of positions visited
# when traversing minimum-cost paths
positions = map.traverse(V)
print(len(positions))
