from z3 import *

if __name__ == "__main__":
    x, y, z = Reals('x y z')
    s = Solver()
    s.add(x > 1, y > 1, x + y > 3, z - x < 10)
    print(s.check())  # sat
    print(s.model())  # [z = 0, y = 2, x = 3/2]
    m = s.model()
    print("x = %s" % m[x])  # x = 3/2

    print("traversing model...")
    for d in m.decls():
        print("%s = %s" % (d.name(), m[d]))
# z = 0
# y = 2
# x = 3/2
