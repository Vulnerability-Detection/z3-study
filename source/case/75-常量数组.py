from z3 import *

if __name__ == "__main__":
    AllOne = K(IntSort(), 1)
    a, i = Ints('a i')
    solve(a == AllOne[i])  # [a = 1]
    # The following constraints do not have a solution
    # 以下约束没有解决方案
    solve(a == AllOne[i], a != 1)  # no solution
