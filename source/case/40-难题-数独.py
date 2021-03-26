from z3 import *

if __name__ == "__main__":
    # 9x9 matrix of integer variables
    # 9x9整数变量矩阵
    X = [[Int("x_%s_%s" % (i + 1, j + 1)) for j in range(9)]
         for i in range(9)]

    # each cell contains a value in {1, ..., 9}
    # 每个单元格都包含{1，...，9}中的值
    cells_c = [And(1 <= X[i][j], X[i][j] <= 9) for i in range(9) for j in range(9)]

    # each row contains a digit at most once
    # 每行最多包含一个数字
    rows_c = [Distinct(X[i]) for i in range(9)]

    # each column contains a digit at most once
    # 每列最多包含一个数字
    cols_c = [Distinct([X[i][j] for i in range(9)]) for j in range(9)]

    # each 3x3 square contains a digit at most once
    # 每个3x3正方形最多包含一个数字
    sq_c = [Distinct([X[3 * i0 + i][3 * j0 + j]
                      for i in range(3) for j in range(3)])
            for i0 in range(3) for j0 in range(3)]

    sudoku_c = cells_c + rows_c + cols_c + sq_c

    # sudoku instance, we use '0' for empty cells
    # 数独实例，我们对空单元格使用“ 0”
    instance = ((0, 0, 0, 0, 9, 4, 0, 3, 0),
                (0, 0, 0, 5, 1, 0, 0, 0, 7),
                (0, 8, 9, 0, 0, 0, 0, 4, 0),
                (0, 0, 0, 0, 0, 0, 2, 0, 8),
                (0, 6, 0, 2, 0, 1, 0, 5, 0),
                (1, 0, 2, 0, 0, 0, 0, 0, 0),
                (0, 7, 0, 0, 0, 0, 5, 2, 0),
                (9, 0, 0, 0, 6, 5, 0, 0, 0),
                (0, 4, 0, 9, 7, 0, 0, 0, 0))

    instance_c = [If(instance[i][j] == 0, True, X[i][j] == instance[i][j])
                  for i in range(9) for j in range(9)]
    s = Solver()
    s.add(sudoku_c + instance_c)
    if s.check() == sat:
        m = s.model()
        r = [[m.evaluate(X[i][j]) for j in range(9)]
             for i in range(9)]
        print_matrix(r)
    else:
        print("failed to solve")
