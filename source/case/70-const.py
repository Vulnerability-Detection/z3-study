from z3 import *

if __name__ == "__main__":
    x = Const('x', IntSort())
    print(eq(x, Int('x')))  # True

    a, b = Consts('a b', BoolSort())
    print(And(a, b))  # And(a, b)
