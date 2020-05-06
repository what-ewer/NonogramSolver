from HintParser import HintParser
from NonogramSolver import NonogramSolver

n = NonogramSolver(HintParser.parseFile("hints/AGH"))
n.solve()
print(n)