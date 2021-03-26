from z3 import *

if __name__ == "__main__":
    x = Real('x')
    solve(x > 4, x < 0)  # no solution
