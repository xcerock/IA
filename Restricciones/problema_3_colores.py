""" [0, 1, 1, 0, 0, 0, 0],  # WA
    [1, 0, 1, 1, 0, 0, 0],  # NT
    [1, 1, 0, 1, 1, 1, 0],  # SA
    [0, 1, 1, 0, 1, 0, 0],  # QLD
    [0, 0, 1, 1, 0, 1, 0],  # NSW
    [0, 0, 1, 0, 1, 0, 0],  # VIC
    [0, 0, 0, 0, 0, 0, 0]   # T"""

from constraint import *
from rich import print

links = [
    ['WA', 'NT'],
    ['WA', 'SA'],
    ['NT', 'SA'],
    ['NT', 'QLD'],
    ['SA', 'QLD'],
    ['SA', 'NSW'],
    ['SA', 'VIC'],
    ['QLD', 'NSW'],
    ['NSW', 'VIC']
]

prob = Problem()

prob.addVariables(['WA', 'NT', 'SA', 'QLD', 'NSW', 'VIC','T' ], ['RED', 'GREEN', 'BLUE'])

#prob.addConstraint(AllDifferentConstraint())
for X, Y in links:
    prob.addConstraint(lambda x,y: x != y, (X,Y))

print(prob.getSolutions())