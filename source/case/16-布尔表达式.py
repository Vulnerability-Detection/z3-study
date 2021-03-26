from z3 import *

if __name__ == "__main__":
    p = Bool('p')
    q = Bool('q')
    print(And(p, q, True))  # And(p, q, True)
    print(simplify(And(p, q, True)))  # And(p, q)
    print(simplify(And(p, False)))  # False
