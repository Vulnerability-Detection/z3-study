from z3 import *

if __name__ == "__main__":
    x = Int('x')
    y = Int('y')
    n = x + y >= 3
    print("num args: ", n.num_args())  # num args:  2
    print("children: ", n.children())  # children:  [x + y, 3]
    print("1st child:", n.arg(0))  # 1st child: x + y
    print("2nd child:", n.arg(1))  # 2nd child: 3
    print("operator: ", n.decl())  # operator:  >=
    print("op name:  ", n.decl().name())  # op name:   >=
