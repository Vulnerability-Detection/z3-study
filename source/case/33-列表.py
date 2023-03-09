
from z3 import *

if __name__ == "__main__":
    # Create list [1, ..., 5]
    # 创建列表[1，...，5]
    print([x + 1 for x in range(5)])  # [1, 2, 3, 4, 5]

    # Create two lists containing 5 integer variables
    # 创建两个包含5个整数变量的列表
    X = [Int('x%s' % i) for i in range(5)]
    Y = [Int('y%s' % i) for i in range(5)]
    print(X)  # [x0, x1, x2, x3, x4]

    # Create a list containing X[i]+Y[i]
    # 创建一个包含X [i] + Y [i]的列表
    X_plus_Y = [X[i] + Y[i] for i in range(5)]
    print(X_plus_Y)  # [x0 + y0, x1 + y1, x2 + y2, x3 + y3, x4 + y4]

    # Create a list containing X[i] > Y[i]
    # 创建一个包含X [i]> Y [i]的列表
    X_gt_Y = [X[i] > Y[i] for i in range(5)]
    print(X_gt_Y)  # [x0 > y0, x1 > y1, x2 > y2, x3 > y3, x4 > y4]

    print(And(X_gt_Y))  # And(x0 > y0, x1 > y1, x2 > y2, x3 > y3, x4 > y4)

    # Create a 3x3 "matrix" (list of lists) of integer variables
    # 创建一个3x3的“矩阵”（列表列表）整数变量
    X = [[Int("x_%s_%s" % (i + 1, j + 1)) for j in range(3)]
         for i in range(3)]
    pp(X)
