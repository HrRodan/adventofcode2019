import math

with open('input.txt') as file:
    masses = [int(line.strip()) for line in file.readlines()]


def get_fuel(mass: int) -> int:
    return max(math.floor(mass / 3) - 2, 0)


# part 1
print(sum(get_fuel(m) for m in masses))


# part 2
def get_fuel_recursive(start_mass: int):
    fuel = get_fuel(start_mass)
    return 0 if fuel == 0 else fuel + get_fuel_recursive(fuel)


print(sum(get_fuel_recursive(m) for m in masses))
