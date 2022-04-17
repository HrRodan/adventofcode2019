import networkx as nx
import matplotlib.pyplot as plt

with open('input.txt') as file:
    orbits = [x.strip().split(')')[::-1] for x in file.readlines()]

G = nx.Graph(orbits)

print(sum(nx.shortest_path_length(G, n, 'COM') for n in G.nodes))
print(nx.shortest_path_length(G, 'YOU', 'SAN')-2)
