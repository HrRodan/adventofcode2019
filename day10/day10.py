import math
from collections import Counter, defaultdict
from typing import Tuple

import numpy as np

with open('input.txt') as file:
    asteroid_map_raw = [list(line.strip()) for line in file.readlines()]

ASTEROID_MAP = np.where(np.array(asteroid_map_raw) == '#', 1, 0).astype(np.ubyte)

ALL_ASTEROIDS = np.transpose(ASTEROID_MAP.nonzero())


def xy_to_unique_value(point: Tuple[int, int]):
    # normalize vector with mahatten metric to avoid numerical rounding problems
    y, x = point
    if x == y == 0:
        return (0, 0)
    abs_r = abs(x) + abs(y)
    return (y / abs_r, x / abs_r)


def get_number_of_visible_asteroids(position: Tuple[int, int]):
    diff_map = ALL_ASTEROIDS - position
    count_map = Counter(xy_to_unique_value(a) for a in diff_map)
    # minus 1 to remove the asteroid itself
    return len(count_map) - 1


count_per_asteroid = {tuple(p): get_number_of_visible_asteroids(p) for p in ALL_ASTEROIDS}
best_position = max(count_per_asteroid.items(), key=lambda x: x[1])
print(best_position[1])


# part2
def sort_atan(point: Tuple[int, int]):
    y, x = point
    return -math.atan2(x, y)


to_destroy = ALL_ASTEROIDS - best_position[0]

# build list of asteroids for all directions
all_directions = defaultdict(list)
for p in to_destroy:
    all_directions[xy_to_unique_value(p)].append(p)

# sort asteriods per direction with ascending distance
for p, l in all_directions.items():
    all_directions[p] = sorted(l, key=lambda x: abs(x[0]) + abs(x[1]))

# sort all directions by angle
all_directions = dict(sorted(all_directions.items(), key=lambda x: sort_atan(x[0])))


def iterate(end=200):
    i = 0
    while True:
        for p, l in all_directions.items():
            if l:
                a = l.pop(0)
                i += 1
            if i == end + 1:
                print(a + best_position[0])
                break


iterate()

# print(to_destroy_sorted[:4])
