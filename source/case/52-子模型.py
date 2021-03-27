from z3 import *

if __name__ == "__main__":
    t = Then('simplify','normalize-bounds','solve-eqs')
    x, y, z = Ints('x y z')
    g = Goal()
    g.add(x > 10, y == x + 3, z > y)

    r = t(g)
    # r contains only one subgoal
    # r仅包含一个子目标
    print(r)  # [[Not(k!0 <= -1), Not(z <= 14 + k!0)]]

    s = Solver()
    s.add(r[0])
    print(s.check())  # sat
    # Model for the subgoal
    # 子目标模型
    print(s.model())  # [z = 15]
    # Model for the original goal
    # 最初目标的模型
    # 会报错=> AttributeError: 'ApplyResult' object has no attribute 'convert_model'
    # print(r.convert_model(s.model()))
