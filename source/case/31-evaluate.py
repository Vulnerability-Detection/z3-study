from z3 import *

if __name__ == "__main__":
    x = Int('x')
    y = Int('y')
    f = Function('f', IntSort(), IntSort())
    s = Solver()
    s.add(f(f(x)) == x, f(x) == y, x != y)
    print(s.check())  # sat
    m = s.model()
    print("f(f(x)) =", m.evaluate(f(f(x))))  # f(f(x)) = 0
    print("f(x)    =", m.evaluate(f(x)))  # f(x)    = 1
    print(m)  # [x = 0, y = 1, f = [1 -> 0, else -> 1]]
