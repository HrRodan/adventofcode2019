import numpy as np

with open('input.txt') as f:
    wires = [line.strip() for line in f.readlines()]

wires_movements = [[(x[0], int(x[1:])) for x in wire.split(',')] for wire in wires]


def find_path(wire_movement):
    path = [(0, 0)]
    for d, c in wire_movement:
        y0, x0 = path[-1]
        for i in range(1, c + 1):
            if d == 'D':
                path.append((y0 + i, x0))
            elif d == 'L':
                path.append((y0, x0 - i))
            elif d == 'R':
                path.append((y0, x0 + i))
            elif d == 'U':
                path.append((y0 - i, x0))
    return path


wires_path = [find_path(w) for w in wires_movements]

intersections = set.intersection(*(set(x) for x in wires_path))
intersections.remove((0, 0))

# part 1
print(np.min(np.sum(np.abs(list(intersections)), axis=1)))

# part 2

intersection_points_length = []
for pe in wires_path:
    intersection_points_length_dict = {}
    for length, point in enumerate(pe):
        if point in intersections and point not in intersection_points_length_dict:
            intersection_points_length_dict[point] = length
    intersection_points_length.append(intersection_points_length_dict)

print(min((sum(x[p] for x in intersection_points_length)) for p in intersections))
