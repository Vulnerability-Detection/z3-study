from z3 import *

if __name__ == "__main__":
    f = Function('f', IntSort(), IntSort(), IntSort())
    x, y = Ints('x y')
    print(ForAll([x, y], f(x, y) == 0))  # ForAll([x, y], f(x, y) == 0)
    print(Exists(x, f(x, x) >= 0))  # Exists(x, f(x, x) >= 0)

    a, b = Ints('a b')
    solve(ForAll(x, f(x, x) == 0), f(a, b) == 1)  # [b = 2, a = 0, f = [(0, 2) -> 1, else -> 0]]
