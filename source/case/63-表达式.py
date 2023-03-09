from z3 import *

if __name__ == "__main__":
    x = Int('x')
    y = Real('y')
    print((x + 1).sort())  # Int
    print((y + 1).sort())  # Real
    print((x >= 2).sort())  # Bool
