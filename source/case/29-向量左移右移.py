from z3 import *

if __name__ == "__main__":
    # Create to bit-vectors of size 32
    x, y = BitVecs('x y', 32)

    solve(x >> 2 == 3)  # [x = 12]

    solve(x << 2 == 3)  # no solution

    solve(x << 2 == 24)  # [x = 6]
