from z3 import *

if __name__ == "__main__":
    x = Int('x')
    print((x + 1).hash())  # 1880882057
    print((1 + x).hash())  # 3655631788
    print(eq(x + 1, 1 + x))  # False
    print(x.sort().hash())  # 2867189042
