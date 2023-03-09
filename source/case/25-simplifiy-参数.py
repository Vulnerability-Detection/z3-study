from z3 import *

if __name__ == "__main__":
    x, y = Reals('x y')
    # Using Z3 native option names
    # 使用Z3本地选项名称
    print(simplify(x == y + 2, ':arith-lhs', True))  # x + -1*y == 2
    # Using Z3Py option names
    # 使用Z3Py选项名称
    print(simplify(x == y + 2, arith_lhs=True))  # x + -1*y == 2

    print("\nAll available options:")
    help_simplify()
