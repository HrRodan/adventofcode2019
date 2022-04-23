from collections import deque
from itertools import islice
from typing import Iterator

import matplotlib
import matplotlib.animation as animation
import numpy as np
from matplotlib import pyplot as plt

from intcode import run_program, read_program

matplotlib.use("TkAgg")
ANIMATE = False

program_start = read_program('input.txt')

# %% part1
p_input = deque()
output = run_program(program_start.copy(), p_input)

game = []
while True:
    try:
        x, y, tile_id = islice(output, 3)
    except ValueError:
        break
    game.append(((y, x), tile_id))

a, _ = zip(*game)
a = np.array(a)
row = a[:, 0].max() + 1
col = a[:, 1].max() + 1
result = np.zeros((row, col), dtype=np.byte)
for (y, x), v in game:
    result[y, x] = v

print(np.sum(result == 2))

# %% part 2
program_start_part2 = program_start.copy()
program_start_part2[0] = 2
result_part2 = np.zeros((row, col), dtype=np.byte)

if ANIMATE:
    ims = []
    fig, ax = plt.subplots()

p_input = deque([0])
p = run_program(program_start_part2, p_input)
for _ in range(len(game) + 1):
    x, y, tile_id = islice(p, 3)
    result_part2[y, x] = tile_id

score = 0

finished = False
while not finished:
    p_input.clear()
    move = -(result_part2 == 3).nonzero()[1] + (result_part2 == 4).nonzero()[1]
    p_input.append(move[0])
    for k in range(2):
        try:
            x, y, tile_id = islice(p, 3)
        except ValueError:
            finished = True
            break
        if x == -1 and y == 0:
            score = tile_id
        else:
            result_part2[y, x] = tile_id
            if ANIMATE and k == 1:
                im = ax.imshow(result_part2, animated=True)
                ims.append([im])

print(score)
if ANIMATE:
    ani = animation.ArtistAnimation(fig, ims, interval=5, blit=True,
                                    repeat_delay=1000)
    writer = animation.FFMpegWriter(
        fps=15, metadata=dict(artist='Me'), bitrate=100)
    ani.save("movie.mp4", writer=writer)
