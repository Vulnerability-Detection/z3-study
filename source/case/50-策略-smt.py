from z3 import *

if __name__ == "__main__":
    x, y = Ints('x y')
    s = Tactic('smt').solver()
    s.add(x > y + 1)
    print(s.check())  # sat
    print(s.model())  # [y = -2, x = 0]
