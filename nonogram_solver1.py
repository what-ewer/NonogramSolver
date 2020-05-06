from HintParser import HintParser
from NonogramSolver import NonogramSolver

n = NonogramSolver(HintParser.parseFile("hints/statek"))
n.solve()
print(n)