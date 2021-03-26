from z3 import *

if __name__ == "__main__":
    x = Real('x')  # 实数
    y = Real('y')
    print(simplify(And(x ** 2 + y ** 2 > 3, x ** 3 + y < 5)))  # And(Not(x**2 + y**2 <= 3), Not(5 <= x**3 + y))
    solve(x ** 2 + y ** 2 > 3, x ** 3 + y < 5)  # [y = 2, x = 1/8]
