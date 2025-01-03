import sys


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


def nth_secret(initial_number: int, n: int) -> int:
    for secret in secrets(initial_number, n):
        pass
    return secret


with open(sys.argv[1]) as file:
    result = sum(
        nth_secret(int(line.strip()), 2000)
        for line in file

    )
print(result)
