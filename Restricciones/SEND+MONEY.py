from constraint import *
from rich import print

prob = Problem()

prob.addVariables(['t', 'w', 'o', 'f', 'u', 'r'], list(range(10)))

prob.addConstraint(lambda t: t != 0, ('t'))
prob.addConstraint(lambda f: f != 0, ('f'))

prob.addConstraint(AllDifferentConstraint())

prob.addConstraint(lambda t,w,o,f,u,r: 100*t + 10*w + o + 100*t + 10*w + o == 1000*f + 100*o + 10*u + r, ('t', 'w', 'o', 'f', 'u', 'r'))
print(prob.getSolutions())