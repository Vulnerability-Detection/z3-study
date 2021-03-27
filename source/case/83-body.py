from z3 import *

if __name__ == "__main__":
    f = Function('f', IntSort(), IntSort(), IntSort())
    x, y = Ints('x y')
    f = ForAll([x, y], f(x, y) == 0)
    print(f.body())  # f(Var(1), Var(0)) == 0

    v1 = f.body().arg(0).arg(0)  # Var(1)
    print(v1)
    print(eq(v1, Var(1, IntSort())))  # True
