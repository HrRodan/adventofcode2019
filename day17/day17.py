import collections
from collections import deque
from itertools import product, islice
import re

import numpy as np
from scipy.ndimage import generic_filter

from intcode import run_program, read_program

start_program = read_program('input.txt')

p_input = deque([])
output = list(run_program(start_program.copy(), p_input))
output_to_print = ''.join(chr(x) for x in output)

# convert to array
output_ascii_list = []
temp_output = []
for o in output:
    if o == 10 and temp_output:
        output_ascii_list.append(temp_output)
        temp_output = []
    else:
        temp_output.append(o)

char_to_num = {
    '#': ord('#'),
    '.': ord('.'),
    '^': ord('^'),
    'v': ord('v'),
    '<': ord('<'),
    '>': ord('>')
}

scaffold_nums = [v for k, v in char_to_num.items() if k != '.']

num_to_char = {v: k for k, v in char_to_num.items()}

output_array = np.array(output_ascii_list).astype(np.ubyte)
scaffolds = np.isin(output_array, scaffold_nums)
scaffold_intersections = generic_filter(scaffolds, function=np.all,
                                        footprint=((0, 1, 0), (1, 1, 1), (0, 1, 0)), mode='constant', cval=False)

scaffold_intersections_points = np.transpose(np.nonzero(scaffold_intersections))
result = np.prod(scaffold_intersections_points, axis=1).sum()
print(result)

# %%part 2
TURN_RIGHT = {
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
    (-1, 0): (0, 1)
}
directions = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1)
}
TURN_LEFT = {v: k for k, v in TURN_RIGHT.items()}
robot_nums = [v for k, v in char_to_num.items() if k not in ['.', '#']]
scaffold_points = {tuple(x) for x in np.transpose(np.nonzero(scaffolds))}

# starting position and direction
position = np.transpose(np.nonzero(np.isin(output_array, robot_nums)))[0]
direction = directions[num_to_char[output_array[tuple(position)]]]

path = []
while True:
    next_step = position + direction
    count = 0
    # move forward until outside of scaffold
    while tuple(next_step) in scaffold_points:
        count += 1
        position = next_step
        next_step = position + direction
    if count > 0:
        path.append(str(count))
    left = TURN_LEFT[direction]
    right = TURN_RIGHT[direction]
    if tuple(position + left) in scaffold_points:
        direction = left
        path.append('L')
    elif tuple(position + right) in scaffold_points:
        direction = right
        path.append('R')
    else:
        break

# find functions by looking at the complete path
path_str = ','.join(path)
path_str_raw = path_str
functionA = ['L', '12', 'L', '12', 'L', '6', 'L', '6']
functionA_str = ','.join(functionA)
path_str = path_str.replace(functionA_str, 'A')
functionB = ['R', '8', 'R', '4', 'L', '12']
functionB_str = ','.join(functionB)
path_str = path_str.replace(functionB_str, 'B')
functionC = ['L', '12', 'L', '6', 'R', '12', 'R', '8']
functionC_str = ','.join(functionC)
path_str = path_str.replace(functionC_str, 'C')

# build input
mmr = [ord(x) for x in path_str] + [10]
functionA_ascii = [ord(x) for x in functionA_str] + [10]
functionB_ascii = [ord(x) for x in functionB_str] + [10]
functionC_ascii = [ord(x) for x in functionC_str] + [10]

start_program_part2 = start_program.copy()
start_program_part2[0] = 2
p_input_part2 = deque(mmr + functionA_ascii + functionB_ascii + functionC_ascii + [ord('n'), 10])

output_part2 = list(run_program(start_program_part2, p_input_part2))
print(output_part2[-1])


# %% generate Functions by brute Force
def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) -> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def eval():
    for i, j, k in product(range(2, 11, 2), repeat=3):
        for x in sliding_window(path, i):
            for y in sliding_window(path, j):
                for z in sliding_window(path, k):
                    path_test_str = path_str_raw
                    for f, letter in zip([x, y, z], ['A', 'B', 'C']):
                        txt = ','.join(f)
                        path_test_str = path_test_str.replace(txt, letter)
                    if re.match(r'^[ABC,]*$', path_test_str):
                        return (x, y, z, path_test_str)


#funcA_gen, funcB_gen, funcC_gen, path_final = eval()
