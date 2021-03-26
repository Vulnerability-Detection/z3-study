from z3 import *

if __name__ == "__main__":
    p = Bool('p')
    x = Real('x')
    solve(Or(x < 5, x > 10), Or(p, x ** 2 == 2), Not(p))  # [x = -1.4142135623?, p = False]
