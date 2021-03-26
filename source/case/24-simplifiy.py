from z3 import *

if __name__ == "__main__":
    x, y = Reals('x y')
    # Put expression in sum-of-monomials form
    # 将表达式以总和形式表示
    t = simplify((x + y) ** 3, som=True)  # x*x*x + 3*x*x*y + 3*x*y*y + y*y*y
    print(t)
    # Use power operator
    # 使用power运算符
    t = simplify(t, mul_to_power=True)  # x**3 + 3*x**2*y + 3*x*y**2 + y**3
    print(t)
