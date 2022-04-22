from collections import defaultdict, deque
from itertools import permutations, islice
from typing import List, Iterable, Iterator, Dict, Tuple

import numpy as np
from matplotlib import pyplot as plt

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


def run_program(program: Dict[int, int], p_input: deque[int]):
    program_final = program.copy()
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

    yield False


def add_direction(point: Tuple[int, int], direction: Tuple[int, int]):
    return (point[0] + direction[0], point[1] + direction[1])


TURN_RIGHT = {
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
    (-1, 0): (0, 1)
}
TURN_LEFT = {v: k for k, v in TURN_RIGHT.items()}
TURN = [TURN_LEFT, TURN_RIGHT]


def paint_hull(hull, position, direction, program) -> None:
    p_input = deque()
    p = run_program(program, p_input)
    while True:
        p_input.append(hull[position])
        color = next(p, False)
        turn_out = next(p, False)
        if turn_out is False or color is False:
            break
        hull[position] = color
        direction = TURN[turn_out][direction]
        position = add_direction(position, direction)


# part 1
hull_part1 = defaultdict(lambda: 0)
paint_hull(hull_part1, (0, 0), (0, 1), program_start)
print(len(hull_part1))

# part 2
hull_part2 = defaultdict(lambda: 0)
hull_part2[(0, 0)] = 1
paint_hull(hull_part2, (0, 0), (0, 1), program_start)

# graphics
a = np.array(list(hull_part2.keys()))
col = a[:, 0].max() - a[:, 0].min() + 1
row = a[:, 1].max() - a[:, 1].min() + 1
result = np.zeros((row, col), dtype=int)
for k, v in hull_part2.items():
    result[-k[1], k[0]] = v

# KBUEGZBK
plt.imshow(result, interpolation='none')
plt.savefig('output.png')
plt.show()
plt.close()
