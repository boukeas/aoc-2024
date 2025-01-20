from collections import Counter
from itertools import product
import sys


def fit(lock, key) -> bool:
    return all(height + depth <= 5 for height, depth in zip(lock, key))


locks = []
keys = []
with open(sys.argv[1]) as file:
    lines = iter(file)
    while True:
        line = next(lines).strip()
        lock = (line == "#####")

        counter = Counter()
        for i in range(5):
            line = next(lines).strip()
            counter.update(
                {
                    column
                    for column, content in enumerate(line)
                    if content == "#"
                }
            )

        signature = tuple(counter[column] for column in range(5))
        if lock:
            locks.append(signature)
        else:
            keys.append(signature)

        line = next(lines).strip()
        try:
            line = next(lines).strip()
        except StopIteration:
            break

result = sum(1 for lock, key in product(locks, keys) if fit(lock, key))
print(result)
