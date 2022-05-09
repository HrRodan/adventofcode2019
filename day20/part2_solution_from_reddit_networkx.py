# Source : https://github.com/matnad/aoc19/blob/master/day20/day20b.py

from collections import defaultdict
from string import ascii_uppercase

import networkx as nx
from aocd.models import Puzzle


def get_nbs(point):
    """Get all four neighbouring points."""
    return [(point[0] + dx, point[1] + dy) for dx, dy in zip([0, 1, 0, -1], [-1, 0, 1, 0])]


puzzle = Puzzle(year=2019, day=20)
in1 = puzzle.input_data.split('\n')

grid = defaultdict(lambda: '#')
W, H = len(in1[0]), len(in1)

for y in range(H):
    for x in range(W):
        grid[(x, y)] = in1[y][x] if in1[y][x] != ' ' else '#'

portals = defaultdict(list)  # matches the portal names to their coordinates like portals['XY'] = [(x1,y1), (x2, y2)]
G = nx.Graph()
levels = 30  # maximum allowed recursion depth
start = end = None
for y in range(1, H - 1):
    for x in range(1, W - 1):
        symbol = grid[(x, y)]
        if symbol in ascii_uppercase:
            nbs = [(a, b) for a, b in get_nbs((x, y)) if grid[(a, b)] != '#']
            if len(nbs) == 2:
                # letter and pathway found
                if grid[nbs[0]] in ascii_uppercase:
                    letter, pad = nbs
                else:
                    pad, letter = nbs
                key = ''.join(sorted(symbol + grid[letter]))  # sort portal name
                portals[key].append(pad)
                if key == 'AA':
                    start = pad
                elif key == 'ZZ':
                    end = pad
        elif symbol == '.':
            for i in range(levels):
                G.add_node((x, y, i))  # create the node on each level
            nbs = [(a, b) for a, b in get_nbs((x, y)) if grid[(a, b)] == '.']
            for nb in nbs:
                for i in range(levels):
                    G.add_edge((x, y, i), (*nb, i))  # connect the pathways on each level

for pads in portals.values():
    if len(pads) == 2:
        if pads[0][0] in [2, W - 3] or pads[0][1] in [2, H - 3]:
            outer, inner = pads
        else:
            inner, outer = pads
        for i in range(levels - 1):
            # inner portals lead to the outer portals on the next level and outer to inner on the previous level
            G.add_edge((*inner, i), (*outer, i + 1))
            G.add_edge((*outer, i + 1), (*inner, i))


ansb = nx.shortest_path_length(G, (*start, 0), (*end, 0))  # specify that we want to start and end on level 0
print("Number of steps to get from AA to ZZ on level 0:", ansb)
# puzzle.answer_b = ansb