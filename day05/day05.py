from typing import List

with open('input.txt') as file:
    program_start = [int(n) for n in file.readline().strip().split(',')]


def run_program(program: List[int], p_input: int):
    program_final = program.copy()
    output = []
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
            program_final[p] = p_input
            i += 2
        elif opcode == 4:
            p = program_final[i + 1]
            value = p if mode[-1] == '1' else program_final[p]
            output.append(value)
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

    return output


# part1
o = run_program(program_start, 1)
assert all(x == 0 for x in o[:-1])
print(o[-1])

# part 2
o2 = run_program(program_start, 5)
assert len(o2) == 1
print(o2[-1])
