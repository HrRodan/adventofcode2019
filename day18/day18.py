import string
from typing import Tuple

import networkx as nx

with open('input_test.txt') as file:
    cave = [list(line.strip()) for line in file.readlines()]

POINT_TYP = Tuple[int, int]

spaces = set()
keys = {}
doors = {}
for i, row in enumerate(cave):
    for j, value in enumerate(row):
        if value != '#':
            spaces.add((i, j))
        if value == '@':
            start = (i, j)
        if value in string.ascii_lowercase:
            keys[value] = (i, j)
        if value in string.ascii_uppercase:
            doors[value] = (i, j)

key_points = {value: key for key, value in keys.items()}
key_points[start] = '@'
neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def add_tuple(t1: POINT_TYP, t2: POINT_TYP):
    return (t1[0] + t2[0], t1[1] + t2[1])


G_spaces = nx.Graph()
for p in spaces:
    for n in neighbors:
        if (x := add_tuple(p, n)) in spaces:
            G_spaces.add_edge(p, x)
            G_spaces.nodes[x]['label'] = cave[x[0]][x[1]]

G_walk = G_spaces.copy()
# close all doors in Graph
G_walk.remove_nodes_from(doors.values())

collected_keys = {}
G_compressed = nx.Graph()
G_compressed.add_node(start)
key_points_set = set(key_points.keys())

for _ in range(2):
    for k1 in list(G_compressed.nodes):
        for k2, value in key_points.items():
            if k1 != k2 and nx.has_path(G_walk, k1, k2):
                G_compressed.add_node(k2, label=value)
                shortest_path = nx.shortest_path(G_walk, k1, k2)
                if not key_points_set.intersection(shortest_path[1:-1]):
                    G_compressed.add_edge(k1, k2, weight=len(shortest_path) - 1)
    collected_keys = {z for x, y in G_compressed.nodes if (z := cave[x][y]) in keys}
    for k in collected_keys:
        if d := k.upper() in doors:
            door_point = doors[d]
            G_walk.add_node(door_point, label=d)
            for n in neighbors:
                if (x := add_tuple(door_point, n)) in spaces:
                    G_walk.add_edge(x, door_point)
            for n in list(G_compressed.nodes):
                shortest_path = nx.shortest_path(G_walk, n, door_point)
                G_compressed.add_edge(n, door_point, weight=len(shortest_path) - 1)
