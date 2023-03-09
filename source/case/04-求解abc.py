from z3 import *

if __name__ == "__main__":
    a = Int('a')
    b = Int('b')
    s = Solver()

    s.add(a * b == 0x24)  # 求解 a * b == 36
    s.add(a == 2)  # a限制为2
    if s.check() == sat:
        m = s.model()
        print(m)  # [b = 18, a = 2]
    else:
        print("no sat")
