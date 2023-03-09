from z3 import *

if __name__ == "__main__":
    a = Int('a')
    b = Int('b')
    s = Solver()

    s.add(a * b == 0x24)  # 求解 a * b == 36
    if s.check() == sat:
        m = s.model()
        print(m)  # [a = 36, b = 1]
    else:
        print("no sat")
