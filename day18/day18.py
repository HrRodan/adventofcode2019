import string
from collections import defaultdict
from typing import Tuple, Dict, Set

import networkx as nx

with open('input_part2.txt') as file:
    cave = [list(line.strip()) for line in file.readlines()]

POINT_TYP = Tuple[int, int]

spaces = set()
keys = {}
doors = {}
start = set()
for i, row in enumerate(cave):
    for j, value2 in enumerate(row):
        if value2 != '#':
            spaces.add((i, j))
        if value2 == '@':
            start.update({(i, j)})
        if value2 in string.ascii_lowercase:
            keys[value2] = (i, j)
        if value2 in string.ascii_uppercase:
            doors[value2] = (i, j)

key_points = {value: key for key, value in keys.items()}
door_points = {value: key for key, value in doors.items()}
start_points = {s: f'@{i}' for i, s in enumerate(start)}
key_and_start = key_points | start_points
neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
all_keys = set(keys.keys())


def add_tuple(t1: POINT_TYP, t2: POINT_TYP):
    return (t1[0] + t2[0], t1[1] + t2[1])


G_spaces = nx.Graph()
for p in spaces:
    for n in neighbors:
        if (x := add_tuple(p, n)) in spaces:
            G_spaces.add_edge(p, x)
            G_spaces.nodes[x]['label'] = cave[x[0]][x[1]]

links: Dict[str, Dict[str, Tuple[int, set]]] = defaultdict(dict)
for k1, value1 in key_and_start.items():
    for k2, value2 in key_and_start.items():
        if k1 != k2:
            # avoid calculating the same path twice
            try:
                links[value1][value2] = links[value2][value1]
                continue
            except KeyError:
                pass
            # continue if no path exists (different quadrant)
            try:
                shortest_path = nx.shortest_path(G_spaces, k1, k2)
            except nx.exception.NetworkXNoPath:
                continue
            # make doors lowercase to enable list compare
            doors_on_path = {cave[x][y] for x, y in shortest_path}.intersection(doors.keys())
            links[value1][value2] = (len(shortest_path) - 1, {x.lower() for x in doors_on_path})

cache = {}


def walk(start_point: Set[str], needed_keys: set):
    if not needed_keys:
        return 0
    # tuple is faster than string join
    cache_tuple = (tuple(sorted(start_point)), tuple(needed_keys))
    if cache_tuple in cache:
        return cache[cache_tuple]
    min_length = float("inf")
    for key in needed_keys:
        for s in start_point:
            link = links[s]
            if key in link:
                shortest_path_length, doors_on_path = link[key]
                if shortest_path_length < min_length and doors_on_path.isdisjoint(needed_keys):
                    length_full = shortest_path_length + walk((start_point - {s}).union(key), needed_keys - {key})
                    min_length = min(length_full, min_length)
    cache[cache_tuple] = min_length
    return min_length


a = walk(set(start_points.values()), all_keys)
print(a)
