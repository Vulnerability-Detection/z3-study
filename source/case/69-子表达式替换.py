from z3 import *

if __name__ == "__main__":
    x, y = Ints('x y')
    f = Function('f', IntSort(), IntSort(), IntSort())
    g = Function('g', IntSort(), IntSort())
    n = f(f(g(x), g(g(x))), g(g(y)))
    print(n)  # f(f(g(x), g(g(x))), g(g(y)))

    # substitute g(g(x)) with y and g(y) with x + 1
    # 用y替换g（g（x））并用x + 1替换g（y）
    print(substitute(n, (g(g(x)), y), (g(y), x + 1)))  # f(f(g(x), y), g(x + 1))
