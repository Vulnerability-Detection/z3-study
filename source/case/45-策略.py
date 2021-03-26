from z3 import *

if __name__ == "__main__":
    x, y = Reals('x y')
    g = Goal()
    g.add(Or(x < 0, x > 0), x == y + 1, y < 0)

    t = Tactic('split-clause')
    r = t(g)
    for g in r:
        print(g)

# [x < 0, x == y + 1, y < 0]
# [x > 0, x == y + 1, y < 0]
