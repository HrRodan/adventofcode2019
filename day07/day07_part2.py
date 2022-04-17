from collections import deque
from itertools import permutations
from typing import List, Iterable

with open('input.txt') as file:
    program_start = [int(n) for n in file.readline().strip().split(',')]


def run_program(program: List[int], p_input: deque[int]):
    program_final = program.copy()
    i = 0
    while True:
        mode_opcode_str = str(program_final[i])
        mode, opcode = mode_opcode_str[:-2], int(mode_opcode_str[-2:])
        mode = f'0000{mode}'
        if opcode == 99:
            break
        elif opcode in {1, 2}:
            p1, p2, postion_out = program_final[i + 1: i + 4]
            value1 = p1 if mode[-1] == '1' else program_final[p1]
            value2 = p2 if mode[-2] == '1' else program_final[p2]
            result = value1 + value2 if opcode == 1 else value1 * value2
            program_final[postion_out] = result
            i += 4
        elif opcode == 3:
            p = program_final[i + 1]
            program_final[p] = p_input.popleft()
            i += 2
        elif opcode == 4:
            p = program_final[i + 1]
            yield p if mode[-1] == '1' else program_final[p]
            i += 2
        elif opcode in {5, 6}:
            p1, p2 = program_final[i + 1: i + 3]
            value1 = p1 if mode[-1] == '1' else program_final[p1]
            value2 = p2 if mode[-2] == '1' else program_final[p2]
            if (opcode == 5 and value1 != 0) or (opcode == 6 and value1 == 0):
                i = value2
            else:
                i = i + 3
        elif opcode in {7, 8}:
            p1, p2, postion_out = program_final[i + 1: i + 4]
            value1 = p1 if mode[-1] == '1' else program_final[p1]
            value2 = p2 if mode[-2] == '1' else program_final[p2]
            if (opcode == 7 and value1 < value2) or (opcode == 8 and value1 == value2):
                program_final[postion_out] = 1
            else:
                program_final[postion_out] = 0
            i = i + 4
        else:
            raise ValueError('Something went wrong.')

    yield False


# part 2
# sourcery skip: simplify-boolean-comparison
phase_outputs = {}
final_output = 0
for phases in permutations(range(5, 10)):
    input_values = [deque([p]) for p in phases]
    input_values[0].append(0)
    amps = [run_program(program_start, inputs) for inputs in input_values]
    output = True
    while output is not False:
        for i, amp in enumerate(amps):
            output = next(amp)
            if i < 4:
                input_values[i + 1].append(output)
            elif i == 4:
                input_values[0].append(output)
                if output:
                    phase_outputs[phases] = output

print(max(phase_outputs.values()))

#alternative Solution: Intcode as own object/class
