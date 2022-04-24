import math
import re
from collections import defaultdict
from typing import Tuple

from scipy import optimize

with open('input.txt') as file:
    reactions_raw = [re.findall(r'(\d+) ([A-Z]+)', line.strip()) for line in file.readlines()]

reactions = defaultdict(list)

for r in reactions_raw:
    number, out = r[-1]
    reactions[out].append(int(number))
    for r_in in r[:-1]:
        reactions[out].append((r_in[1], int(r_in[0])))


def get_products(chemcial: str):
    products = set()
    for product, educts in reactions.items():
        for educt in educts[1:]:
            if educt[0] == chemcial:
                products.update([product])
    return products


def get_educts(product: Tuple[str, int]):
    p, count_in = product
    count_out, *educts = reactions[p]
    relation = math.ceil(count_in / count_out)
    return [(e, count * relation) for e, count in educts]


# The reaction layers define layers in which reactants are allowed to react at the same time
# This is necessary to collect all necessary educts before continuing and optimize the amount of reactants
reaction_layers = defaultdict(set)
i = 0
reaction_layers[i] = {'ORE'}
while True:
    i += 1
    previous = reaction_layers[i - 1]
    if len(previous) == 1 and 'FUEL' in previous:
        break
    for c in previous:
        if c != 'FUEL':
            reaction_layers[i].update(get_products(c))


max_layers = max(reaction_layers.keys())


def get_ore_amount(fuel: int = 1):
    current_reactants = defaultdict(lambda: 0)
    current_reactants['FUEL'] = fuel

    for i in range(max_layers, 0, -1):
        for r in current_reactants.copy().items():
            if r[0] in reaction_layers[i]:
                current_reactants.pop(r[0])
                for e, c in get_educts(r):
                    current_reactants[e] += c

    return current_reactants['ORE']


print(get_ore_amount(1))

# part 2
final = 1000000000000
print(round(optimize.newton(lambda x: get_ore_amount(x) - final, 100000, rtol=0.1, maxiter=100000)))
