from z3 import *

if __name__ == "__main__":
    x, y = Ints('x y')
    print(eq(x + y, x + y))  # True
    print(eq(x + y, y + x))  # False
    n = x + y
    print(eq(n, x + y))  # True
    # x2 is eq to x
    x2 = Int('x')
    print(eq(x, x2))  # True
    # the integer variable x is not equal to
    # the real variable x
    print(eq(Int('x'), Real('x')))  # False
