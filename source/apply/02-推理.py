from z3 import *

# 源地址: https://www.7forz.com/3255/
# 某大型煤矿发生了一起重大事故，事发现场的人有以下的断定：
#
# 矿工甲：发生事故的原因是设备问题；
# 矿工乙：有人违反了操作规程，但发生事故的原因不是设备问题；
# 矿工丙：如果发生事故的原因是设备问题，那么有人违反操作规程；
# 矿工丁：发生事故的原因是设备问题，但没有人违反操作规程。
#
# 如果上述四人的断定中只有一个人为真，则以下可能为真的一项是（ ）。
#
# A.矿工甲的断定为真
# B.矿工乙的断定为真
# C.矿工丁的断定为真
# D.矿工丙的断定为真，有人违反了操作规程
# E.矿工丙的断定为真，没有人违反操作规程

# 由运行结果可见选项 E 是正确的。

equipment = Bool('shebei')  # 设备是否有问题
violation = Bool('weifan')  # 是否违反操作规程

s1 = equipment  # 甲：发生事故的原因是设备问题
s2 = And(violation, Not(equipment))  # 乙：违反了操作规程，但不是设备问题
s3 = Implies(equipment, violation)  # 丙：如果事故的原因是设备问题，那么违反操作规程
s4 = And(equipment, Not(violation))  # 丁：发生事故的原因是设备问题，但没有人违反操作规程


def build_solver():
    solver = Solver()
    solver.add(If(s1, 1, 0) + If(s2, 1, 0) + If(s3, 1, 0) + If(s4, 1, 0) == 1)  # 四人的断定中只有一个人为真
    return solver


if __name__ == '__main__':
    solver = build_solver()
    # 采用反证法 把各选项的 *否定* 添加进solver中 若冲突将返回unsat 原选项正确
    solver.add(Not(s1))  # 甲的断定为真
    print(solver.check())  # sat

    solver = build_solver()
    solver.add(Not(s2))  # 乙的断定为真
    print(solver.check())  # sat

    solver = build_solver()
    solver.add(Not(s4))  # 丁的断定为真
    print(solver.check())  # sat

    solver = build_solver()
    solver.add(Not(And(s3, violation)))  # 丙的断定为真 并且有人违反了操作规程
    print(solver.check())  # sat

    solver = build_solver()
    solver.add(Not(And(s3, Not(violation))))  # 丙的断定为真 并且没有人违反操作规程
    print(solver.check())  # unsat
