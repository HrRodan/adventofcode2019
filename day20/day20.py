import heapq
import string
from collections import defaultdict
from typing import Tuple, Set

import networkx as nx

with open('input.txt') as file:
    maze = [list(s.rstrip('\n')) for s in file.readlines()]

POINT_TYPE = Tuple[int, int]

next_tiles = [(1, 0), (-1, 0), (0, 1), (0, -1)]
max_width = max(len(x) for x in maze)
max_height = len(maze)
start = ('AA', 'out')
end = ('ZZ', 'out')


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

portals_inner_outer = {}
for portal, connections in portals.items():
    for connection in connections:
        c1, c2 = connection
        if c1 not in (max_height - 3, 2) and c2 not in (max_width - 3, 2):
            portals_inner_outer[(portal, 'in')] = (c1, c2)
        else:
            portals_inner_outer[(portal, 'out')] = (c1, c2)

# generate compressed graph connecting all portals
G_compressed = nx.Graph()
for (portal1, io1), pos1 in portals_inner_outer.items():
    for (portal2, io2), pos2 in portals_inner_outer.items():
        if ((portal2, io2), (portal1, io1)) not in G_compressed.edges:
            if portal1 != portal2:
                try:
                    shortest_path_length = nx.shortest_path_length(G, pos1, pos2)
                    G_compressed.add_edge((portal1, io1), (portal2, io2), weight=shortest_path_length)
                except nx.exception.NetworkXNoPath:
                    continue
            elif io1 != io2:
                G_compressed.add_edge((portal1, io1), (portal2, io2), weight=1)

print(nx.shortest_path_length(G_compressed, start, end, weight='weight'))

# part2

# key is always portal, in/out and level
shortest_path_length = {(start, 0): 0, (end, 0): float("inf")}
portals_to_visit = []
# priority -> Tuple [ level, path_length ] to force upward search
heapq.heappush(portals_to_visit, ((0, 0), start))
start_end = {start, end}

# Dijkstra's algorithm
while portals_to_visit:
    (level_current, length_current), portal_current = heapq.heappop(portals_to_visit)
    portal_current_letter, io_current = portal_current
    for portal_next, edge_dict in G_compressed[portal_current].items():
        portal_next_letter, io_next = portal_next
        path_length_next = edge_dict['weight'] + length_current
        level_diff = 0
        if portal_next_letter == portal_current_letter:
            level_diff = 1 if io_current == 'in' else -1
        level_next = level_current + level_diff
        portal_level_key_next = (portal_next, level_next)
        if path_length_next < shortest_path_length[(end, 0)] \
                and (portal_next not in start_end or level_next == 0) \
                and (io_next != 'out' or level_next != 0 or portal_next == end) \
                and (portal_level_key_next not in shortest_path_length
                     or path_length_next < shortest_path_length[portal_level_key_next]):
            shortest_path_length[portal_level_key_next] = path_length_next
            heapq.heappush(portals_to_visit, ((level_next, path_length_next), portal_next))

print(shortest_path_length[((end), 0)])
