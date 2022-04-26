from collections import defaultdict, deque
from typing import Tuple

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from intcode import read_program, run_program

POINT_TYP = Tuple[int, int]

start_program = read_program('input.txt')

cmd = {
    (0, 1): 1,
    (0, -1): 2,
    (1, 0): 4,
    (-1, 0): 3
}

area = defaultdict(lambda: -1)
area[(0, 0)] = 1


def move(start, direction):
    return (start[0] + direction[0], start[1] + direction[1])


def get_direction(start: POINT_TYP, end: POINT_TYP):
    return cmd[(end[0] - start[0], end[1] - start[1])]


def get_possible_places_and_update_graph(G: nx.Graph, to_vist : set):
    possible_places = set()
    for point in to_vist:
        for c in cmd.keys():
            target = move(point, c)
            if target not in area:
                G.add_edge(point, target)
                possible_places.add(target)

    return possible_places


current_position = (0, 0)
p_input = deque()
p = run_program(start_program.copy(), p_input)
G = nx.Graph()
G.add_node(current_position)
oxygen_location = 0
to_visit = {current_position}

while True:
    possible_places = get_possible_places_and_update_graph(G, to_visit)
    to_visit = set()
    for pp in possible_places:
        path = nx.shortest_path(G, current_position, pp)
        for current_element, next_element in zip(path[:-1], path[1:]):
            d = get_direction(current_element, next_element)
            p_input.append(d)
            output = next(p)
            area[next_element] = output
            if output in {1, 2}:
                to_visit.add(next_element)
                G.add_edge(current_element, next_element)
                current_position = next_element
                if output == 2:
                    oxygen_location = next_element
            elif output == 0:
                G.remove_node(next_element)
                break

    if not possible_places:
        break

print(nx.shortest_path_length(G, (0, 0), oxygen_location))
print(max(nx.single_source_shortest_path_length(G, oxygen_location).values()))

# graphics
area_graphics = area.copy()
area_graphics[(0, 0)] = 3
a = np.array(list(area_graphics.keys()))
min_col, min_row = np.min(a, axis=0)
col, row = np.max(a, axis=0) - np.min(a, axis=0) + 1
result = np.zeros((row, col), dtype=int)
for k, v in area_graphics.items():
    result[k[1] - min_row, k[0] - min_col] = v

plt.imshow(result, interpolation='none')
plt.colorbar()
plt.savefig('output.png')
plt.show()
plt.close()
