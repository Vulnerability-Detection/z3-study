from z3 import *

if __name__ == "__main__":
    x = Real('x')
    s = Solver()
    s.add(2 ** x == 3)
    print(s.check())  # unknown
