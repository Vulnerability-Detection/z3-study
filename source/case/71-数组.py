from z3 import *

if __name__ == "__main__":
    # Use I as an alias for IntSort()
    # 使用I作为IntSort（）的别名
    I = IntSort()
    # A is an array from integer to integer
    # A是一个从整数到整数的数组
    A = Array('A', I, I)
    x = Int('x')

    print(A[x])  # A[x]
    print(Select(A, x))  # A[x]
    print(Store(A, x, 10))  # Store(A, x, 10)
    print(simplify(Select(Store(A, 2, x + 1), 2)))  # 1 + x
