from z3 import *

if __name__ == "__main__":
    A = Array('A', IntSort(), IntSort())
    x, y = Ints('x y')
    solve(A[x] == x, Store(A, x, y) == A, x != y)  # no solution
