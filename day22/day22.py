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


def get_previous_mod_reversed(inc: int, pos):
    # reverse modulo https://en.wikipedia.org/wiki/Modular_multiplicative_inverse
    # solvable for Deck Size = prime
    return pow(inc, DECK_SIZE + pos - 3, DECK_SIZE + pos - 1)


def solve_linear_congruence(a, b, m):
    """ Describe all solutions to ax = b  (mod m), or raise ValueError.
    https://stackoverflow.com/questions/63021828/solving-modular-linear-congruences-for-large-numbers
    ax = b (mod m) """
    g = math.gcd(a, m)
    if b % g:
        raise ValueError("No solutions")
    a, b, m = a // g, b // g, m // g
    return pow(a, -1, m) * b % m


def get_value(count_order: int, offset: int, inc: int, position: int):
    if count_order < 0:
        return ((DECK_SIZE - position - 1 + offset) * inc) % DECK_SIZE
    else:
        return ((position + offset) * inc) % DECK_SIZE


for s, n in shuffles:
    if s == 'deal into new stack':
        deck = deal_into_new_stack(deck)
    elif s == 'deal with increment':
        deck = deal_with_increment(deck, n)
    elif s == 'cut':
        deck = cut(deck, n)
    #print(deck)

r1 = deck.index(2019)
print(r1)

# part 2
DECK_SIZE_PART2 = 119315717514047
position_p2 = 2020
for i in range(100000):
    for s, n in shuffles[::-1]:
        if s == 'deal into new stack':
            position_p2 = DECK_SIZE_PART2 - position_p2 - 1
        elif s == 'deal with increment':
            position_p2 = solve_linear_congruence(n, position_p2, DECK_SIZE_PART2)
        elif s == 'cut':
            position_p2 = position_p2 + n
            if position_p2 < 0:
                position_p2 = DECK_SIZE_PART2 + position_p2
            position_p2 = position_p2 % DECK_SIZE
    #print(position_p2)

print(position_p2)
