from z3 import *

if __name__ == "__main__":
    x = Real('x')
    solve(3 * x == 1)  # [x = 1/3]

    set_option(rational_to_decimal=True)
    solve(3 * x == 1)  # [x = 0.3333333333?]

    set_option(precision=30)
    solve(3 * x == 1)  # [x = 0.333333333333333333333333333333?]
