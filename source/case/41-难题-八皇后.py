from z3 import *

if __name__ == "__main__":
    # We know each queen must be in a different row.
    # So, we represent each queen by a single integer: the column position
    # 我们知道每个女王都必须在不同的行中。
    # 因此，我们用一个整数表示每个皇后：列位置
    Q = [Int('Q_%i' % (i + 1)) for i in range(8)]

    # Each queen is in a column {1, ... 8 }
    # 每个女王都在{1，... 8}列中
    val_c = [And(1 <= Q[i], Q[i] <= 8) for i in range(8)]

    # At most one queen per column
    # 每列最多一位皇后
    col_c = [Distinct(Q)]

    # Diagonal constraint
    # 对角约束
    diag_c = [If(i == j, True, And(Q[i] - Q[j] != i - j, Q[i] - Q[j] != j - i))
              for i in range(8) for j in range(i)]

    solve(val_c + col_c + diag_c)

# [Q_5 = 1,
#  Q_8 = 7,
#  Q_3 = 8,
#  Q_2 = 2,
#  Q_6 = 3,
#  Q_4 = 6,
#  Q_7 = 5,
#  Q_1 = 4]
