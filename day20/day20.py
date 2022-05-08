import string
from collections import defaultdict
from typing import Tuple

import networkx as nx

with open('input_test.txt') as file:
    maze = [list(s.rstrip('\n')) for s in file.readlines()]

POINT_TYPE = Tuple[int, int]

next_tiles = [(1, 0), (-1, 0), (0, 1), (0, -1)]
max_width = max(len(x) for x in maze)
max_height = len(maze)
start = 'AA'
end = 'ZZ'


def add_tuple(t1: POINT_TYPE, t2: POINT_TYPE):
    return (t1[0] + t2[0], t1[1] + t2[1])


passages = set()
portal_letter_points = {}

for i, row in enumerate(maze):
    for j, char in enumerate(row):
        if char == '.':
            passages.add((i, j))
        elif char in string.ascii_uppercase:
            portal_letter_points[(i, j)] = char

portals = defaultdict(list)
for position, letter in portal_letter_points.items():
    for n in next_tiles:
        test_point = add_tuple(position, n)
        if test_point in passages:
            other_letter_position = add_tuple(position, (-1 * n[0], -1 * n[1]))
            other_letter = portal_letter_points[other_letter_position]
            if other_letter_position < position:
                portals[f'{other_letter}{letter}'].append((test_point))
            else:
                portals[f'{letter}{other_letter}'].append((test_point))

# Build Graph
G = nx.Graph()

for p in passages:
    for n in next_tiles:
        test_point = add_tuple(p, n)
        if test_point in passages:
            G.add_edge(p, test_point)

inner_portals = set()
outer_portals = set()
for portal, connections in portals.items():
    if portal not in ['AA', 'ZZ']:
        #G.add_edge(connections[0], connections[1], label=portal)
        for connection in connections:
            c1, c2 = connection
            if c1 not in (max_height - 3, 2) and c2 not in (max_width - 3, 2):
                inner_portals.add((c1, c2))
            else:
                outer_portals.add((c1, c2))

G_compressed = nx.Graph()
for portal1, connections1 in portals.items():
    for portal2, connections2 in portals.items():
        if portal1 != portal2 and (portal2, portal1) not in G_compressed.edges:
            for c1 in connections1:
                for c2 in connections2:
                    try:
                        shortest_path_length = nx.shortest_path_length(G, c1, c2)
                        if portal1 != end and portal2 != end:
                            shortest_path_length += 1
                        G_compressed.add_edge(portal1, portal2, weight=shortest_path_length)
                    except nx.exception.NetworkXNoPath:
                        continue

all_portals = inner_portals.union(outer_portals)

print(nx.shortest_path_length(G_compressed, start, end, weight='weight'))

# part2
possible_paths = {}

for i, path in enumerate(nx.all_simple_paths(G_compressed, start, end)):
    #print(path)
    level = 0
    last_tile = start
    for e in path:
        if last_tile not in all_portals:
            if e in outer_portals:
                level += 1
            elif e in inner_portals:
                level -= 1
                just_passed_portal = True
        last_tile = e
    if level == 0:
        possible_paths[i] = len(path) - 1

#print(min(possible_paths.values()))
