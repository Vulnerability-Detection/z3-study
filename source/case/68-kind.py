from z3 import *

if __name__ == "__main__":
    x, y = Ints('x y')
    print((x + y).decl().kind())  # 518
    print((x + y).decl().kind() == Z3_OP_ADD)  # True
    print((x + y).decl().kind() == Z3_OP_SUB)  # False
