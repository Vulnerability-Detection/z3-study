from z3 import *

if __name__ == "__main__":
    # This is a comment
    x = Real('x')  # comment: creating x
    print(x ** 2 + 2 * x + 2)  # x**2 + 2*x + 2 comment: 输出多项式
