from collections import defaultdict, deque
from typing import Dict, Iterator


def string_to_program(program_raw: str):
    program = (int(n) for n in program_raw.strip().split(','))
    program_dict = defaultdict(lambda: 0)
    for i, c in enumerate(program):
        program_dict[i] = c

    return program_dict


def read_program(path: str):
    with open(path) as file:
        program_raw = file.readline().strip()
    return string_to_program(program_raw)


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


def run_program(program_start: Dict[int, int], p_input: deque[int], wait_for_input=False, use_default=False,
                default_value=-1) -> Iterator[int]:
    program_final = program_start.copy()
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
            if wait_for_input:
                yield 'waiting for input'
            if use_default and not p_input:
                program_final[out_value] = default_value
            else:
                program_final[out_value] = p_input.popleft()
            i += 2
        elif opcode == 4:
            p = program_final[i + 1]
            yield get_value(mode[-1], p, program_final, relative_base)
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
