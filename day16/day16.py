from itertools import cycle, islice, chain

import numpy as np

with open('input_test.txt') as file:
    signal_start = np.array([int(x) for x in file.readline().strip()]).astype(np.byte)

BASE_PATTERN = (0, 1, 0, -1)
PHASES = 100


def pattern(position: int, length: int):
    pattern = chain.from_iterable([n] * (position + 1) for n in BASE_PATTERN)
    return np.fromiter(islice(cycle(pattern), 1, None), dtype=np.byte, count=length)


def get_patterns(signal_length):
    return {i: pattern(i, signal_length) for i in range(signal_length)}


def transform_signal(start_signal, start_out_signal, length_output_signal=8):
    signal = start_signal.copy()
    signal_length = len(start_signal)
    patterns = get_patterns(signal_length)
    for p in range(PHASES):
        # print(p)
        signal_new = np.zeros(signal_length, dtype=np.byte)
        for s in range(signal_length):
            if start_out_signal <= s:
                # print(s)
                transform = patterns[s]
                signal_new[s] = abs(np.multiply(signal, transform, dtype=np.byte).sum()) % 10
        signal = signal_new
    return signal


# part1
# patterns_part1 = get_patterns(len(signal_start))
print(''.join(str(x) for x in transform_signal(signal_start, start_out_signal=0)[:8]))

# part2
output_position = int(''.join(str(x) for x in signal_start[:7]))
signal_start_part2 = np.tile(signal_start, 10000)


# len_part2 = len(signal_start_part2)
# #patterns_part2 = get_patterns(len_part2)
#

def transform_signal_part2(start_signal, start_out_signal):
    signal = start_signal.copy()
    signal_length = len(start_signal)
    for p in range(PHASES):
        signal_new = np.zeros(signal_length, dtype=np.uint)
        signal_new[-1] = start_signal[-1]
        for s in range(signal_length - 2, start_out_signal - 2, -1):
            signal_new[s] = (signal[s] + signal_new[s + 1])
        signal = (signal_new % 10).astype(np.byte)
    return signal


def transform_signal_part2_v2(start_signal, start_out_signal):
    signal = start_signal[-1:-(len(start_signal)-start_out_signal) - 1:-1]
    for _ in range(PHASES):
        signal = np.cumsum(signal, dtype=np.uint)
        signal = (signal % 10).astype(np.byte)
    return signal


s2 = transform_signal_part2(signal_start_part2, output_position)
print(''.join(str(x) for x in s2[output_position:output_position + 8]))

s3 = transform_signal_part2_v2(signal_start_part2, output_position)
print(''.join(str(x) for x in s3[-1:-9:-1]))
