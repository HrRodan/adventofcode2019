import math
import re

with open('input.txt') as file:
    shuffles = [(st[0].strip(), int(st[1] or 0)) for line in file.readlines()
                for st in [re.match(r'([a-zA-Z ]+)(-?[\d]*)', line.strip()).groups()]]

DECK_SIZE = 10007
# PRIMZAHLEN!

DECK_START = list(range(DECK_SIZE))


def cut(deck, cut: int):
    return deck[cut:] + deck[:cut]


def deal_into_new_stack(deck):
    return deck[::-1]


def deal_with_increment(deck, inc: int):
    deck_new = deck.copy()
    for i, d in enumerate(deck):
        deck_new[(i * inc) % DECK_SIZE] = d

    return deck_new


deck = DECK_START.copy()


def solve_linear_congruence(a, b, m):
    """ Describe all solutions to ax = b  (mod m), or raise ValueError.
    https://stackoverflow.com/questions/63021828/solving-modular-linear-congruences-for-large-numbers
    ax = b (mod m) """
    g = math.gcd(a, m)
    if b % g:
        raise ValueError("No solutions")
    a, b, m = a // g, b // g, m // g
    return pow(a, -1, m) * b % m


for s, n in shuffles:
    if s == 'deal into new stack':
        deck = deal_into_new_stack(deck)
    elif s == 'deal with increment':
        deck = deal_with_increment(deck, n)
    elif s == 'cut':
        deck = cut(deck, n)
    # print(deck)

r1 = deck.index(2019)
print(r1)

# part 2
DECK_SIZE_PART2 = 119315717514047
number_shuffles = 101741582076661

# polynom f(x) = ax+b
a, b = 1, 0
start_postion = 2020
for s, n in shuffles[::-1]:
    if s == 'cut':
        b = (b + n) % DECK_SIZE_PART2
    elif s == 'deal into new stack':
        a = -a
        b = DECK_SIZE_PART2 - b - 1
    elif s == 'deal with increment':
        z = pow(n, DECK_SIZE_PART2-2, DECK_SIZE_PART2)
        a = a * z % DECK_SIZE_PART2
        b = b * z % DECK_SIZE_PART2
# see solution.md
print((pow(a, number_shuffles, DECK_SIZE_PART2) * start_postion + (pow(a, number_shuffles, DECK_SIZE_PART2) - 1) *
       pow(a-1, DECK_SIZE_PART2-2, DECK_SIZE_PART2) * b) % DECK_SIZE_PART2)
