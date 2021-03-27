from z3 import *

if __name__ == "__main__":
    f = Function('f', IntSort(), IntSort())
    g = Function('g', IntSort(), IntSort())
    a, b, c = Ints('a b c')
    x = Int('x')

    s = Solver()
    s.set(auto_config=False, mbqi=False)
    s.add(ForAll(x, f(g(x)) == x, patterns=[f(g(x))]), g(a) == c, g(b) == c, a != b)

    # Display solver state using internal format
    # 使用内部格式显示求解器状态
    print(s.sexpr())
    # (declare - fun f (Int) Int)
    # (declare - fun g (Int) Int)
    # (declare - fun c () Int)
    # (declare - fun a () Int)
    # (declare - fun b () Int)
    # (assert (forall ((x Int)) (! (= (f (g x)) x):pattern((f(g x))))))
    # (assert (= (g a) c))
    # (assert (= (g b) c))
    # (assert (distinct a b))
    print(s.check())  # unknown
