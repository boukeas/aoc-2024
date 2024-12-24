from functools import cache
import sys


@cache
def feasible(design: str) -> int:
    if not design:
        return 1
    return sum(
        feasible(design[len(pattern):])
        for pattern in patterns
        if design.startswith(pattern)
    )


with open(sys.argv[1]) as file:
    patterns = file.readline().strip().split(", ")
    file.readline()
    designs = [line.strip() for line in file]

result = sum(feasible(design) for design in designs)
print(result)
