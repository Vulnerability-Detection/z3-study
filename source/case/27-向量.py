from z3 import *

if __name__ == "__main__":
    x = BitVec('x', 16)
    y = BitVec('y', 16)
    print(x + 2)  # x + 2
    # Internal representation
    # 内部表示
    print((x + 2).sexpr())  # (bvadd x #x0002)

    # -1 is equal to 65535 for 16-bit integers
    # 对于16位整数，-1等于65535
    print(simplify(x + y - 1))  # 65535 + x + y

    # Creating bit-vector constants
    # 创建位向量常数
    a = BitVecVal(-1, 16)
    b = BitVecVal(65535, 16)
    print(simplify(a == b))  # True

    a = BitVecVal(-1, 32)
    b = BitVecVal(65535, 32)
    # -1 is not equal to 65535 for 32-bit integers
    # 对于32位整数，-1不等于65535
    print(simplify(a == b))  # False
