import re
import sys

# patterns to match:
# - "instructions like mul(X,Y), where X and Y are each 1-3 digit numbers"
# - do()
# - don't()
pattern = re.compile(
    r"mul\((?P<num1>\d{1,3}),(?P<num2>\d{1,3})\)|"
    r"(?P<enable>do\(\))|"
    r"(?P<disable>don't\(\))"
)

# read the input file as a single string
with open(sys.argv[1]) as file:
    data = file.read()

# iterate of all pattern matches in the input string
result = 0
enabled = True
for match in pattern.finditer(data):
    if match.group("enable"):
        enabled = True
    elif match.group("disable"):
        enabled = False
    elif enabled:
        # the pair of numbers in the match
        num1, num2 = int(match.group("num1")), int(match.group("num2"))
        result += num1 * num2

print(result)
