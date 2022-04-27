from collections import deque

import numpy as np
from scipy.ndimage import generic_filter

from intcode import run_program, read_program

start_program = read_program('input.txt')

p_input = deque([])
output = list(run_program(start_program, p_input))
output_to_print = ''.join(chr(x) for x in output)

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
scaffold_intersections = generic_filter(scaffolds, function=lambda x: np.sum(x) == 5,
                                        footprint=((0, 1, 0), (1, 1, 1), (0, 1, 0)), mode='constant', cval=False)

scaffold_intersections_points = np.transpose(np.nonzero(scaffold_intersections))
result = np.prod(scaffold_intersections_points, axis=1).sum()
print(result)
