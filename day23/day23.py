from collections import deque
from itertools import islice
from typing import Dict, Tuple, Iterator

from intcode import read_program, run_program

start_program = read_program('input.txt')

# initialize with adress 0...49
message_q = [deque([i]) for i in range(50)]
computers: Dict[int, Tuple[Iterator, deque]] = \
    {i: (run_program(start_program, message_q[i], wait_for_input=True, use_default=True), message_q[i]) for i in
     range(50)}

# initialize
for n, (p, m) in computers.items():
    next(p)

def network():
    part1 = False
    NAT = None
    idle_stat = [False for _ in range(50)]
    seen_nat_y = set()
    for k in range(100):
        # print(k)
        for n, (p, m) in computers.items():
            # consume que
            # print(n)
            while ((message := next(p)) == 'waiting for input'):
                if not m:
                    idle_stat[n] = True
                    break

            while message != 'waiting for input':
                idle_stat[n] = False
                x, y = islice(p, 2)
                if message == 255:
                    if not part1:
                        print(y)
                        part1 = True
                    NAT = [x, y]
                else:
                    message_q[message].extend([x, y])
                message = next(p)

        if all(idle_stat):
            message_q[0].extend(NAT)
            y = NAT[1]
            if y in seen_nat_y:
                return y
            else:
                seen_nat_y.add(y)

print(network())

