from HintParser import HintParser
from NonogramSolver import NonogramSolver

import sys

if len(sys.argv) < 2:
    print("Usage: %s hints" % sys.argv[0])
    sys.exit(-1)

n = NonogramSolver(HintParser.parseFile(sys.argv[1]))
n.solve()
print(n)