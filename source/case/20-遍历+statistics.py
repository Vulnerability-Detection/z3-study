from z3 import *

if __name__ == "__main__":
    x = Real('x')
    y = Real('y')
    s = Solver()
    s.add(x > 1, y > 1, Or(x + y > 3, x - y < 2))
    print("asserted constraints...")
    for c in s.assertions():
        print(c)

    print()
    print(s.check())  # sat
    print("statistics for the last check method...")
    print(s.statistics())
    # Traversing statistics
    print()
    for k, v in s.statistics():
        print("%s : %s" % (k, v))

# decisions : 2
# final checks : 1
# num checks : 1
# mk bool var : 4
# arith-lower : 1
# arith-upper : 3
# arith-make-feasible : 3
# arith-max-columns : 8
# arith-max-rows : 2
# num allocs : 284913
# rlimit count : 355
# max memory : 2.92
# memory : 2.6
# time : 0.01
