from z3 import *

if __name__ == "__main__":
    x = Real('x')
    y = Int('y')
    a, b, c = Reals('a b c')
    s, r = Ints('s r')
    print(x + y + 1 + (a + s))  # x + ToReal(y) + 1 + a + ToReal(s)
    print(ToReal(y) + c)  # ToReal(y) + c
