from z3 import *

if __name__ == "__main__":
    x, y, z = Reals('x y z')
    g = Goal()
    g.add(x ** 2 - y ** 2 >= 0)

    p = Probe('num-consts')
    t = If(p > 2, 'simplify', 'factor')
    print(t(g))  # [[(y + -1*x)*(y + x) <= 0]]

    g = Goal()
    g.add(x + x + y + z >= 0, x ** 2 - y ** 2 >= 0)
    print(t(g))  # [[2*x + y + z >= 0, x**2 + -1*y**2 >= 0]]
