from z3 import *

if __name__ == "__main__":
    x = Int('x')
    y = Int('y')
    f = Function('f', IntSort(), IntSort())
    solve(f(f(x)) == x, f(x) == y, x != y)  # [x = 0, y = 1, f = [1 -> 0, else -> 1]]
