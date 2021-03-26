from z3 import *

if __name__ == "__main__":
    X = IntVector('x', 5)
    Y = RealVector('y', 5)
    P = BoolVector('p', 5)
    print(X)  # [x__0, x__1, x__2, x__3, x__4]
    print(Y)  # [y__0, y__1, y__2, y__3, y__4]
    print(P)  # [p__0, p__1, p__2, p__3, p__4]

    print([y ** 2 for y in Y])  # [y__0**2, y__1**2, y__2**2, y__3**2, y__4**2]
    print(Sum([y ** 2 for y in Y]))  # y__0**2 + y__1**2 + y__2**2 + y__3**2 + y__4**2

