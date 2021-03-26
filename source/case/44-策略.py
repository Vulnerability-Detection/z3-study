from z3 import *

if __name__ == "__main__":
    x, y = Reals('x y')
    g = Goal()
    g.add(x > 0, y > 0, x == y + 2)
    print(g)  # [x > 0, y > 0, x == y + 2]

    t1 = Tactic('simplify')
    t2 = Tactic('solve-eqs')
    t = Then(t1, t2)
    print(t(g))  # [[Not(y <= -2), Not(y <= 0)]]
