from z3 import *

if __name__ == "__main__":
    x = Real('x')
    y = Real('y')
    solve(x ** 2 + y ** 2 == 3, x ** 3 == 2)  # [y = -1.1885280594?, x = 1.2599210498?]

    set_option(precision=30)  # 设置精度
    print("Solving, and displaying result with 30 decimal places")
    solve(x ** 2 + y ** 2 == 3, x ** 3 == 2)
    # [y = -1.188528059421316533710369365015?,
    #  x = 1.259921049894873164767210607278?]
