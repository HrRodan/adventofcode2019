import random
import re
from collections import deque, defaultdict

from intcode import read_program, run_program

start_program = read_program('input.txt')

north_cmd = [ord(x) for x in list('north')] + [10]
south_cmd = [ord(x) for x in list('south')] + [10]
east_cmd = [ord(x) for x in list('east')] + [10]
west_cmd = [ord(x) for x in list('west')] + [10]
inv_cmd = [ord(x) for x in list('inv')] + [10]

cmd_map = {
    'east': east_cmd,
    'west': west_cmd,
    'north': north_cmd,
    'south': south_cmd
}


def drop_cmd(item: str):
    return [ord(x) for x in list(f'drop {item}')] + [10]


def take_cmd(item: str):
    return [ord(x) for x in list(f'take {item}')] + [10]


p_input = deque()
droid_program = run_program(start_program, p_input, wait_for_input=True)


def move_and_get_output():
    # consume input
    while (x := next(droid_program)) == 'waiting for input':
        pass
    output = [x]
    while (x := next(droid_program)) != 'waiting for input':
        output.append(x)
    return ''.join([chr(o) for o in output])


def get_doors_from_output(output_str: str):
    return re.findall(r'(east|west|north|south)', output_str)


def get_items(output_str: str):
    return set(re.findall(r'(?:- )([a-z ]+)', output_str)) - {'east', 'south', 'west', 'north'}


def get_room(output_str: str):
    return re.search(r'==[ \S]+==', output_str).group()


visited = set()
r = move_and_get_output()
available_moves = defaultdict(set)
done_moves = defaultdict(set)
print(r)
for _ in range(1000):
    doors = get_doors_from_output(r)
    room = get_room(r)
    for d in doors:
        if d not in done_moves[room]:
            available_moves[room].add(d)
    for item in get_items(r) - {'giant electromagnet', 'escape pod', 'photons', 'molten lava', 'infinite loop'}:
        p_input.extend(take_cmd(item))
        move_and_get_output()
    next_door = random.choice(doors)
    done_moves[room].add(next_door)
    available_moves[room].discard(next_door)
    p_input.extend(cmd_map[next_door])
    r_temp = move_and_get_output()
    if r_temp == "\nYou can't go that way.\n\nCommand?\n":
        continue
    r = r_temp
    print(room)
    #print(r)

p_input.extend(inv_cmd)
print(move_and_get_output())
