import re
import sys

# pattern to match: "instructions like mul(X,Y), where X and Y are each 1-3 digit numbers"
pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

# read the input file as a single string
with open(sys.argv[1]) as file:
    data = file.read()

# iterate of all pattern matches in the input string and
# generate the pairs of numbers in each match
data_iter = (
    (int(number_str) for number_str in match.groups())
    for match in pattern.finditer(data)
)
result = sum(num1 * num2 for num1, num2 in data_iter)
print(result)
