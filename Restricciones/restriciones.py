from constraint import *
from rich import print

links = [
    ['1', '2'],
    ['1', '4'],
    ['1', '7'],
    ['2', '3'],
    ['2', '4'],
    ['2', '5'],
    ['3', '4'],
    ['3', '5'],
    ['3', '6'],
    ['4', '5'],
    ['4', '7'],
    ['4', '8'],
    ['5', '6'],
    ['5', '7'],
    ['5', '8'],
    ['6', '8'],
    ['7', '8']
]

prob = Problem()

prob.addVariables([f'{x}' for x in range(1,9)], [x for x in range(1,9)])

prob.addConstraint(AllDifferentConstraint())
for X, Y in links:
    prob.addConstraint(lambda x,y: abs(x-y) != 1, (X,Y))

print(prob.getSolutions())