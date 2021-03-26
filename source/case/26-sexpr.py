from z3 import *

if __name__ == "__main__":
    x, y = Reals('x y')
    solve(x + 10000000000000000000000 == y, y > 20000000000000000)
    # [y = 20000000000000001, x = -9999979999999999999999]

    print(Sqrt(2) + Sqrt(3))  # 2**(1/2) + 3**(1/2)
    print(simplify(Sqrt(2) + Sqrt(3)))  # 3.1462643699?
    print(simplify(Sqrt(2) + Sqrt(3)).sexpr())  # (root-obj (+ (^ x 4) (* (- 10) (^ x 2)) 1) 4)
    # The sexpr() method is available for any Z3 expression
    # sexpr（）方法可用于任何Z3表达式
    print((x + Sqrt(y) * 2).sexpr())  # (+ x (* (^ y (/ 1.0 2.0)) 2.0))
