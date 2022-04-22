import numpy as np
import re
import math

with open('input.txt') as file:
    positions = np.array([[int(x) for x in re.findall(r'-?\d+', s.strip())] for s in file.readlines()]).astype(np.short)

start = positions.copy()
velocity = np.zeros(positions.shape, dtype=np.short)
velocity_start = velocity.copy()
steps_part1 = 1000

repeatv = {x: False for x in range(3)}
j = 0
while True:
    j += 1
    for i in range(1, 4):
        compare_positions = np.roll(positions, i, axis=0)
        velocity += np.where(np.equal(positions, compare_positions), 0,
                             np.where(np.greater(positions, compare_positions), -1, 1)
                             )
    positions += velocity
    # part 1
    if j == steps_part1:
        energy = np.sum(np.sum(np.abs(positions), axis=1) * np.sum(np.abs(velocity), axis=1))
        print(energy)
    # part 2
    for k in range(3):
        # get frequency of velocity as difference between to times where velocity is zero (beginning - x)
        if not repeatv[k] and np.all(velocity[:, k] == 0):
            repeatv[k] = j
    if all(repeatv.values()) and j >= steps_part1:
        break

# velocity period is only half of complete period -> multiply with 2
print(math.lcm(*list(repeatv.values())) * 2)
