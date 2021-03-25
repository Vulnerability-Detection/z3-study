from z3 import *

if __name__ == "__main__":
    x = Int('x')
    s = Solver()
    a = 65537
    b = 64834
    c = 41958
    s.add(x > 0)
    s.add(x % a == b)
    s.add(x % b == c)

    print(s.check())  # sat
    print(s.model())  # [x = 227609298]