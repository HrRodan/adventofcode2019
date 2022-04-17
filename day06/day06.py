with open('input.txt') as file:
    orbits = dict(x.strip().split(')')[::-1] for x in file.readlines())


def count_orbits(orbit: str):
    return 0 if orbit == 'COM' else 1 + count_orbits(orbits[orbit])


result = sum(count_orbits(o) for o in orbits.keys())
print(result)


def traverse_to_com(orbit: str):
    path = [orbit]

    def traverse(o):
        next_orbit = orbits[o]
        path.append(next_orbit)
        if next_orbit == 'COM':
            return
        else:
            traverse(next_orbit)

    traverse(orbit)
    return path

#part 2
result2 = set(traverse_to_com('YOU')).symmetric_difference(traverse_to_com('SAN'))
# first intersection is missing (+1), 'YOU' and 'SAN' are not needed (-2), 'YOU' is already orbiting (-1) -> -2
print(len(result2)-2)
