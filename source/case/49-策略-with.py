from z3 import *

if __name__ == "__main__":
    bv_solver = Then(With('simplify', mul2concat=True),
                     'solve-eqs',
                     'bit-blast',
                     'aig',
                     'sat').solver()
    x, y = BitVecs('x y', 16)
    bv_solver.add(x * 32 + y == 13, x & y < 10, y > -100)
    print(bv_solver.check())  # sat
    m = bv_solver.model()
    print(m)  # [y = 10509, x = 1720]
    print(x * 32 + y, "==", m.evaluate(x * 32 + y))  # x*32 + y == 13
    print(x & y, "==", m.evaluate(x & y))  # x & y == 8
