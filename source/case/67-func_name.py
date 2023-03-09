from z3 import *

if __name__ == "__main__":
    x = Int('x')
    x_d = x.decl()
    print("is_expr(x_d):     ", is_expr(x_d))  # is_expr(x_d):      False
    print("is_func_decl(x_d):", is_func_decl(x_d))  # is_func_decl(x_d): True
    print("x_d.name():       ", x_d.name())  # x_d.name():        x
    print("x_d.range():      ", x_d.range())  # x_d.range():       Int
    print("x_d.arity():      ", x_d.arity())  # x_d.arity():       0
    # x_d() creates an application with 0 arguments using x_d.
    # x_d（）使用x_d创建带有0个参数的应用程序。
    print("eq(x_d(), x):     ", eq(x_d(), x))  # eq(x_d(), x):      True
    print("\n")

    # f is a function from (Int, Real) to Bool
    # f是从（Int，Real）到Bool的函数
    f = Function('f', IntSort(), RealSort(), BoolSort())
    print("f.name():         ", f.name())  # f.name():          f
    print("f.range():        ", f.range())  # f.range():         Bool
    print("f.arity():        ", f.arity())  # f.arity():         2
    for i in range(f.arity()):
        print("domain(", i, "): ", f.domain(i))

    # f(x, x) creates an application with 2 arguments using f.
    # f（x，x）使用f创建带有2个参数的应用程序。
    print(f(x, x))  # f(x, ToReal(x))
    print(eq(f(x, x).decl(), f))  # True
