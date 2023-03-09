from z3 import *

if __name__ == "__main__":
    A = Array('A', IntSort(), IntSort())
    x, y = Ints('x y')
    solve(A[x] == x, Store(A, x, y) == A)  # [A = Store(K(Int, 2), 0, 0), y = 0, x = 0]
