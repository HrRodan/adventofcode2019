from collections import defaultdict
from itertools import permutations
from typing import List, Iterable, Iterator, Dict

with open('input.txt') as file:
    program_raw = file.readline().strip()


def string_to_program(program_raw: str):
    program = (int(n) for n in program_raw.strip().split(','))
    program_dict = defaultdict(lambda: 0)
    for i, c in enumerate(program):
        program_dict[i] = c

    return program_dict


program_start = string_to_program(program_raw)


def get_value(mode: str, p_value: int, program: Dict[int, int], relative_base):
    if mode == '0':
        return program[p_value]
    elif mode == '1':
        return p_value
    elif mode == '2':
        return program[p_value + relative_base]
    else:
        raise ValueError('Something went wrong!')


def get_set_position(mode: str, out: int, relative_base: int):
    return out if mode != '2' else out + relative_base


def run_program(program: Dict[int, int], p_input: Iterator[int]):
    program_final = program.copy()
    output = []
    i = 0
    relative_base = 0
    while True:
        mode_opcode_str = str(program_final[i])
        mode, opcode = mode_opcode_str[:-2], int(mode_opcode_str[-2:])
        mode = f'0000{mode}'
        if opcode == 99:
            break
        elif opcode in {1, 2}:
            p1, p2, out = [program_final[x] for x in range(i + 1, i + 4)]
            value1 = get_value(mode[-1], p1, program_final, relative_base)
            value2 = get_value(mode[-2], p2, program_final, relative_base)
            out_value = get_set_position(mode[-3], out, relative_base)
            result = value1 + value2 if opcode == 1 else value1 * value2
            program_final[out_value] = result
            i += 4
        elif opcode == 3:
            out = program_final[i + 1]
            out_value = get_set_position(mode[-1], out, relative_base)
            program_final[out_value] = next(p_input)
            i += 2
        elif opcode == 4:
            p = program_final[i + 1]
            value = get_value(mode[-1], p, program_final, relative_base)
            output.append(value)
            i += 2
        elif opcode in {5, 6}:
            p1, p2 = [program_final[x] for x in range(i + 1, i + 3)]
            value1 = get_value(mode[-1], p1, program_final, relative_base)
            value2 = get_value(mode[-2], p2, program_final, relative_base)
            if (opcode == 5 and value1 != 0) or (opcode == 6 and value1 == 0):
                i = value2
            else:
                i = i + 3
        elif opcode in {7, 8}:
            p1, p2, out = [program_final[x] for x in range(i + 1, i + 4)]
            value1 = get_value(mode[-1], p1, program_final, relative_base)
            value2 = get_value(mode[-2], p2, program_final, relative_base)
            out_value = get_set_position(mode[-3], out, relative_base)
            if (opcode == 7 and value1 < value2) or (opcode == 8 and value1 == value2):
                program_final[out_value] = 1
            else:
                program_final[out_value] = 0
            i = i + 4
        elif opcode == 9:
            p = program_final[i + 1]
            relative_base += get_value(mode[-1], p, program_final, relative_base)
            i += 2
        else:
            raise ValueError('Something went wrong.')

    return output


assert run_program(string_to_program('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'), iter([])) == \
       [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]

# part 1
print(run_program(program_start, iter([1]))[0])

# part 2
print(run_program(program_start, iter([2]))[0])
