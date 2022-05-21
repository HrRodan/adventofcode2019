from copy import deepcopy
from typing import Dict, List, Tuple

import numpy as np
from scipy.ndimage import generic_filter

with open('input.txt') as file:
    bugs_raw = np.array([list(x.strip()) for x in file.readlines()])

bugs_start = (bugs_raw == '#')


def grow_bugs(x: np.array):
    this_bug = x[2]
    sum_bugs = x.sum() - this_bug
    if this_bug and sum_bugs != 1:
        return False
    elif not this_bug and sum_bugs in (1, 2):
        return True
    else:
        return this_bug


seen_bugs = set()
bugs = bugs_start.copy()
while True:
    bugs = generic_filter(bugs, function=grow_bugs, footprint=((0, 1, 0), (1, 1, 1), (0, 1, 0)),
                          mode='constant', cval=False)
    bugs_flat = tuple(bugs.flatten())
    if bugs_flat not in seen_bugs:
        seen_bugs.add(bugs_flat)
    else:
        # print('repetition found')
        break

biodiversity_rating = sum(2 ** i for i, x in enumerate(bugs.flatten()) if x)
print(biodiversity_rating)

bug_layers = {i: np.full(shape=(5, 5), fill_value=False, dtype=bool) for i in range(-201, 202)}
bug_layers[0] = bugs_start

all_points = {(y, x) for x in range(5) for y in range(5)} - {(2, 2)}
adjacent = [(1, 0), (-1, 0), (0, 1), (0, -1)]

neighbors: Dict[Tuple[int, int], List[Tuple[int, Tuple[int, int]]]] = {a: [] for a in all_points}
for y, x in all_points:
    for a in adjacent:
        y_n, x_n = y + a[0], x + a[1]
        if (y_n, x_n) in all_points:
            neighbors[(y, x)].append((0, (y_n, x_n)))
    if (y, x) == (2, 1):
        neighbors[(y, x)].extend([(-1, (a, 0)) for a in range(5)])
    if (y, x) == (3, 2):
        neighbors[(y, x)].extend([(-1, (4, a)) for a in range(5)])
    if (y, x) == (1, 2):
        neighbors[(y, x)].extend([(-1, (0, a)) for a in range(5)])
    if (y, x) == (2, 3):
        neighbors[(y, x)].extend([(-1, (a, 4)) for a in range(5)])

    if x == 0:
        neighbors[(y, x)].append((1, (2, 1)))
    if y == 4:
        neighbors[(y, x)].append((1, (3, 2)))
    if y == 0:
        neighbors[(y, x)].append((1, (1, 2)))
    if x == 4:
        neighbors[(y, x)].append((1, (2, 3)))


def grow_bugs_p2(this_bug: bool, sum_bugs: int):
    if this_bug and sum_bugs != 1:
        return False
    elif not this_bug and sum_bugs in {1, 2}:
        return True
    else:
        return this_bug


for r in range(1, 201):
    bug_layers_new = deepcopy(bug_layers)
    for l in range(-r, r + 1):
        bug_layer = bug_layers[l]
        for p in all_points:
            sum_bugs = sum(bug_layers[l + l_diff][p_n] for l_diff, p_n in neighbors[p])
            bug_layers_new[l][p] = grow_bugs_p2(bug_layer[p], sum_bugs)
    bug_layers = bug_layers_new

result = sum(np.sum(b) for b in bug_layers.values())
print(result)