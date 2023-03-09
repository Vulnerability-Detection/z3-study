from z3 import *

if __name__ == "__main__":
    print(1 / 3)  # 0.3333333333333333
    print(RealVal(1) / 3)  # 1/3
    print(Q(1, 3))  # 1/3

    x = Real('x')
    print(x + 1 / 3)  # x + 3333333333333333/10000000000000000
    print(x + Q(1, 3))  # x + 1/3
    print(x + "1/3")  # x + 1/3
    print(x + 0.25)  # x + 1/4
