import sys
from typing import NamedTuple


class File(NamedTuple):
    id: int
    size: int
    gap: int


# read the input as a single long string
with open(sys.argv[1]) as file:
    filemap = file.read().strip()

# iterate over the pairs of numbers in the input "filemap" and create
# a list of File objects, storing each file's id, size and succeeding gap
id = 0
files = []
numbers = iter(filemap)
while True:
    size = int(next(numbers))
    try:
        gap = int(next(numbers))
        files.append(File(id, size, gap))
    except StopIteration:
        files.append(File(id, size, 0))
        break
    id += 1

# the "source" is the file to be moved
source = files.pop()
remaining_size = source.size
# the "target" is the file after which the "source" will be moved
target_index = 0
target = files[target_index]
while True:
    if remaining_size > target.gap:
        # the gap is smaller than the remaining part of the source
        remaining_size -= target.gap
        # insert part of the source file that fits in the gap after the target
        files[target_index] = files[target_index]._replace(gap=0)
        files.insert(
            target_index + 1, source._replace(size=target.gap, gap=0)
        )
    else:
        # insert the last remaining part of the source file in the gap after
        # the target (updating the gap that succeeds it)
        files[target_index] = files[target_index]._replace(gap=0)
        files.insert(
            target_index + 1,
            source._replace(size=remaining_size, gap=target.gap - remaining_size)
        )
        # get a new source file to move from the end of the file list
        source = files.pop()
        remaining_size = source.size
    # seek the next available gap (and target)
    while target_index < len(files) and (target := files[target_index]).gap == 0:
        target_index += 1
    if target_index == len(files):
        files.append(source._replace(size=remaining_size))
        break

checksum = 0
index = 0
for (id, size, gap) in files:
    for position in range(size):
        checksum += index * id
        index += 1
    index += gap
print(checksum)
