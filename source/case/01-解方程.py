from z3 import *

if __name__ == "__main__":
    x, y, z = Ints('x y z')
    s = Solver()
    s.add(2 * x + 3 * y + z == 6)
    s.add(x - y + 2 * z == -1)
    s.add(x + 2 * y - z == 5)
    # 解方程=>  x = 2, y = 1, z = -1
    # 2x + 3y + z = 6
    # x - y + 2z = -1
    # x + 2y - z = 5
    print(s.check())  # sat
    print(s.model())  # [z = -1, y = 1, x = 2]