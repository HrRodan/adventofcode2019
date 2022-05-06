from collections import deque, defaultdict

import numpy as np

from intcode import read_program, run_program

start_program = read_program('input.txt')

SIZE = 50

area = np.zeros((50, 50), dtype=np.ubyte)

for i in range(SIZE):
    for j in range(SIZE):
        area[j, i] = next(run_program(start_program, deque([i, j])))

print(np.sum(area))

# part2

SIZE_PART2 = 1300
SIZE_SHIP = 100
area2 = np.zeros([SIZE_PART2] * 2, dtype=np.ubyte)
area2[0, 0] = 1
area2[4, 3] = 1
start_end = defaultdict(list)

for k in range(2, SIZE_PART2):
    last_row = area2[k - 1, :].nonzero()[0]
    len_last_row = len(last_row)
    if len_last_row == 0:
        continue
    start_last_row = last_row[0]

    o = start_last_row
    value = 0
    while True:
        prev_value = value
        value = area2[k, o] = next(run_program(start_program, deque([o, k])))
        if value == 1 and prev_value == 0:
            start_end[k].append(o)
            area2[k, o:o + len_last_row - 1] = 1
            o += len_last_row - 1
        else:
            if prev_value == 1 and value == 0:
                start_end[k].append(o - 1)
                break
            o += 1


def eval():
    for row, (c1, c2) in start_end.items():
        try:
            c1_2, c2_2 = start_end[row + SIZE_SHIP - 1]
        except KeyError:
            return False
        if c1_2 + SIZE_SHIP - 1 == c2:
            return row, c1_2


x = eval()
print(x[1] * 10000 + x[0])
