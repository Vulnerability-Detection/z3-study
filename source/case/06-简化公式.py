from z3 import *

if __name__ == "__main__":
    x = Int('x')
    y = Int('y')
    print(simplify(x + y + 2 * x + 3))  # 3 + 3*x + y
    print(simplify(x < y + x + 2))  # Not(y <= -2)
    print(simplify(And(x + 1 >= 3, x ** 2 + x ** 2 + y ** 2 + 2 >= 5)))  # And(x >= 2, 2*x**2 + y**2 >= 3)
