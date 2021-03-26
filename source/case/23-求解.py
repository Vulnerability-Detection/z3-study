from z3 import *

if __name__ == "__main__":
    a, b, c = Ints('a b c')
    d, e = Reals('d e')
    solve(a > b + 2, a == 2 * c + 10, c + b <= 1000, d >= e)  # [d = 0, c = 0, b = 0, e = 0, a = 10]
