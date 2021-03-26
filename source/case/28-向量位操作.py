from z3 import *

if __name__ == "__main__":
    # Create to bit-vectors of size 32
    x, y = BitVecs('x y', 32)

    solve(x + y == 2, x > 0, y > 0)  # [y = 1, x = 1]

    # Bit-wise operators
    # & bit-wise and
    # | bit-wise or
    # ~ bit-wise not
    solve(x & y == ~y)  # [x = 0, y = 4294967295]

    solve(x < 0)  # [x = 4294967295]

    # using unsigned version of <
    # 使用<
    solve(ULT(x, 0))  # no solution
