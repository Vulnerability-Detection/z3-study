from z3 import *

if __name__ == "__main__":
    x = BitVec('x', 32)
    y = BitVec('y', 32)
    # Claim: (x ^ y) < 0 iff x and y have opposite signs
    # 要求：（x ^ y）<0，如果x和y具有相反的符号
    trick = (x ^ y) < 0
    # Naive way to check if x and y have opposite signs
    # 检查x和y是否有相反符号的简单方法
    opposite = Or(And(x < 0, y >= 0), And(x >= 0, y < 0))

    prove(trick == opposite)  # proved
