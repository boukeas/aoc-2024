import sys


def check(numbers, target) -> bool:
    """
    Check (recursively) if the `numbers` can be combined from left to right
    using multiplication, addition or concatenation to produce the `target`.
    """
    if numbers[0] > target:
        return False
    if len(numbers) == 1:
        return numbers[0] == target
    return (
        check([numbers[0] * numbers[1]] + numbers[2:], target) or
        check([numbers[0] + numbers[1]] + numbers[2:], target) or
        check([int(f"{numbers[0]}{numbers[1]}")] + numbers[2:], target)
    )


# read the input line by line, breaking it down into the target and operands
result = 0
with open(sys.argv[1]) as file:
    for line in file:
        # parsing
        target_str, operands_str = line.strip().split(":")
        target = int(target_str)
        operands = [int(operand) for operand in operands_str.strip().split(" ")]
        # call `check` to compute the result
        if check(operands, target):
            result += target

print(result)
