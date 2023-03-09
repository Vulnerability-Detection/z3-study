from z3 import *

if __name__ == "__main__":
    A = DeclareSort('A')
    x, y = Consts('x y', A)
    f = Function('f', A, A)

    s = Solver()
    s.add(f(f(x)) == x, f(x) == y, x != y)

    print(s.check())  # sat
    m = s.model()
    print(m)
    # [x = A!val!0,
    # y = A!val!1,
    # f = [A!val!1 -> A!val!0, else -> A!val!1]]
    print("interpretation assigned to A:")
    print(m[A])  # [A!val!0, A!val!1]
