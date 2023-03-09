from z3 import *

if __name__ == "__main__":
    p = Bool('p')
    q = Bool('q')
    r = Bool('r')
    solve(Implies(p, q), r == Not(q), Or(Not(p), r))  # [q = True, p = False, r = False]
