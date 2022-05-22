import random
import re
from collections import deque, defaultdict
from itertools import combinations

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

opposite_direction = {
    'east': 'west',
    'north': 'south',
    'south': 'north',
    'west': 'east'
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


def get_inventory():
    p_input.clear()
    p_input.extend(inv_cmd)
    output_str = move_and_get_output()
    return get_items(output_str)


def get_room(output_str: str):
    return re.search(r'==[ \S]+==', output_str).group()


def move_to(target: str, r):
    room = get_room(r)
    while room != target:
        # print(room)
        doors = get_doors_from_output(r)
        next_door = random.choice(doors)
        p_input.extend(cmd_map[next_door])
        r_temp = move_and_get_output()
        if r_temp == "\nYou can't go that way.\n\nCommand?\n":
            continue
        r = r_temp
        room = get_room(r)

    return r


r = move_and_get_output()
moves = {}
rooms = defaultdict(set)

# generate map by randomness
for i in range(10000):
    doors = get_doors_from_output(r)
    room = get_room(r)
    for d in doors:
        moves.setdefault((room, d), 'not visited')
    if 'not visited' not in moves.values():
        print(i)
        break
    # take all items
    room_items = get_items(r)
    rooms[room].update(room_items)

    for item in room_items - {'giant electromagnet', 'escape pod', 'photons', 'molten lava', 'infinite loop'}:
        p_input.extend(take_cmd(item))
        move_and_get_output()

    # choose next door
    not_visited = {(room, d) for d in doors} - {k for k, v in moves.items() if v != 'not visited'}
    if not_visited:
        _, next_door = random.choice(tuple(not_visited))
    else:
        next_door = random.choice(doors)

    p_input.extend(cmd_map[next_door])

    r_temp = move_and_get_output()
    if r_temp == "\nYou can't go that way.\n\nCommand?\n":
        moves[(room, next_door)] = 'Cant go that way!'
        continue
    next_room = get_room(r_temp)
    moves[(room, next_door)] = next_room
    moves[(next_room, opposite_direction[next_door])] = room
    # if room == '== Pressure-Sensitive Floor ==':
    #     print(r)
    r = r_temp

inv_all = get_inventory()
r = move_to('== Security Checkpoint ==', r)
for k in range(1, 5):
    for c in combinations(inv_all, k):
        p_input.clear()
        current_inv = get_inventory()
        # drop all
        for item in current_inv:
            p_input.extend(drop_cmd(item))
            move_and_get_output()
        # take necessary
        for item in c:
            p_input.extend(take_cmd(item))
            move_and_get_output()

        p_input.clear()
        p_input.extend(south_cmd)
        pressure_plate = move_and_get_output()
        print(get_room(pressure_plate))
        #('easter egg', 'mug', 'space heater', 'sand')
        if 'Alert!' not in pressure_plate and get_room(pressure_plate) != '== Security Checkpoint ==':
            print(get_inventory())
            print(pressure_plate)

# G = nx.MultiDiGraph()
# for (room, direction), next_room in moves.items():
#     G.add_edge(room, next_room, attr={'label':direction})
#
# net = Network(height='750px', width='100%')
# net.from_nx(G)
# net.show_buttons()
# net.show('example.html')
