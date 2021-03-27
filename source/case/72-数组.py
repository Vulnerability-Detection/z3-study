from z3 import *

if __name__ == "__main__":
    # We want an array with 3 elements.
    # 1. Bad solution
    X = Array('x', IntSort(), IntSort())
    # Example using the array
    print(X[0] + X[1] + X[2] >= 0)  # x[0] + x[1] + x[2] >= 0

    # 2. More efficient solution
    X = IntVector('x', 3)
    print(X[0] + X[1] + X[2] >= 0)  # x__0 + x__1 + x__2 >= 0
    print(Sum(X) >= 0)  # x__0 + x__1 + x__2 >= 0
