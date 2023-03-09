from z3 import *

if __name__ == "__main__":
    x = Int('x')
    y = Int('y')
    solve(x > 2, y < 10, x + 2 * y == 7) # [y = 0, x = 7]
