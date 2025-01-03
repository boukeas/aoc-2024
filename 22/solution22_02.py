from collections import deque, Counter
from itertools import pairwise, islice
import sys
from typing import Iterable


def mix(number1: int, number2: int) -> int:
    return number1 ^ number2


def prune(number: int) -> int:
    return number % 16777216


def next_secret(number: int) -> int:
    number = prune(mix(number * 64, number))
    number = prune(mix(number // 32, number))
    number = prune(mix(number * 2048, number))
    return number


def secrets(initial_secret: int, n: int):
    secret = initial_secret
    yield secret
    for _ in range(n):
        secret = next_secret(secret)
        yield secret


def prices(initial_secret: int):
    yield from (
        int(str(secret)[-1])
        for secret in secrets(initial_secret, 2000)
    )


def diffs(prices: Iterable[int]):
    yield from (
        next_price - price
        for price, next_price in pairwise(prices)
    )


def history(initial_secret: int):
    """
    Generate a sequence of 1996 prices, each price accompanied by the window
    of four diffs that precedes it 
    """
    prices_iter = list(prices(initial_secret))
    diffs_iter = diffs(prices_iter)
    window = deque(islice(diffs_iter, 4))
    for price, diff in zip(prices_iter[4:], diffs_iter):
        yield price, tuple(window)
        window.popleft()
        window.append(diff)
    yield prices_iter[-1], tuple(window)


with open(sys.argv[1]) as file:
    initial_secrets = [int(line.strip()) for line in file]

# the "cumulative record" maps each window of four diffs to the accumulated
# price that window can achieve *for all initial secrets* (and over all
# corresponding sequences of prices)
cumulative_record = Counter()
for initial_secret in initial_secrets:
    # the "record" maps each window of four diffs to the price that window
    # can achieve *for a specific initial secret* (and over the
    # corresponding sequences of prices)
    record = {}
    for price, window in history(initial_secret):
        # only record the first price for a specific window
        # (because that's when a sale takes place)
        if window not in record:
            record[window] = price
    cumulative_record.update(record)

print(cumulative_record.most_common(1))
