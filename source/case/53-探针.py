from z3 import *

if __name__ == "__main__":
    x, y, z = Reals('x y z')
    g = Goal()
    g.add(x + y + z > 0)

    p = Probe('num-consts')
    print("num-consts:", p(g))  # num-consts: 3.0

    t = FailIf(p > 2)
    try:
        t(g)
    except Z3Exception:
        print("tactic failed")  # tactic failed

    print("trying again...")  # trying again...
    g = Goal()
    g.add(x + y > 0)
    print(t(g))  # [[x + y > 0]]
