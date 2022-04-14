from itertools import product
from typing import List

with open('input.txt') as file:
    program_start = [int(n) for n in file.readline().strip().split(',')]


def run_program(program: List[int], p1: int, p2: int):
    program_final = program.copy()
    program_final[1] = p1
    program_final[2] = p2
    for i in range(0, len(program_final), 4):
        opcode = program_final[i]
        if opcode == 99:
            break
        if opcode not in [1, 2]:
            raise Exception('Something went wrong!')
        position_1, position_2, postion_out = program_final[i + 1: i + 4]
        value1 = program_final[position_1]
        value2 = program_final[position_2]
        result = value1 + value2 if opcode == 1 else value1 * value2
        program_final[postion_out] = result
    return program_final[0]


# part1
print(run_program(program_start, 12, 2))

# part2
for i, j in product(*[range(100)] * 2):
    if run_program(program_start, i, j) == 19690720:
        print(100 * i + j)
        break
