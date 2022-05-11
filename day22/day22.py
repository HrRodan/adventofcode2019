import re

with open('input.txt') as file:
    shuffles = [(st[0].strip(), int(st[1] or 0)) for line in file.readlines()
                for st in [re.match(r'([a-zA-Z ]+)(-?[\d]*)', line.strip()).groups()]]

DECK_SIZE = 10007

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

deal_into_new_stack_state = 1
cut_count = 0
deal_with_increment_count = 1
start_count = 0
for s, n in shuffles:
    if s == 'deal into new stack':
        deck = deal_into_new_stack(deck)
        deal_into_new_stack_state *= -1
    elif s == 'deal with increment':
        deck = deal_with_increment(deck, n)
        deal_with_increment_count = (deal_with_increment_count * n) % DECK_SIZE
    elif s == 'cut':
        deck = cut(deck, n)
        cut_count += deal_into_new_stack_state * n

print(deck.index(2019))

# part 2
# deck_part_2 = DECK_START.copy()
# for k in range(100):
#     for s, n in shuffles:
#         if s == 'deal into new stack':
#             deck_part_2 = deal_into_new_stack(deck_part_2)
#         elif s == 'deal with increment':
#             deck_part_2 = deal_with_increment(deck_part_2, n)
#         elif s == 'cut':
#             deck_part_2 = cut(deck_part_2, n)
#     print(deck_part_2[2020])
