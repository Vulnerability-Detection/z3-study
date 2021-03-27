from z3 import *

if __name__ == "__main__":
    x = Int('x')
    print("is expression: ", is_expr(x))  # is expression:  True
    n = x + 1
    print("is application:", is_app(n))  # is application: True
    print("decl:          ", n.decl())  # decl:           +
    print("num args:      ", n.num_args())  # num args:       2
    for i in range(n.num_args()):
        print("arg(", i, ") ->", n.arg(i))
        # arg( 0 ) -> x
        # arg(1) -> 1
