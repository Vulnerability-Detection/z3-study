from z3 import *

# 源地址: https://www.7forz.com/3255/
# 一军用仓库被窃，公安部门已掌握如下线索：
# ①甲、乙、丙三人至少有一个是窃贼；
# ②如甲是窃贼，则乙一定是同案犯；
# ③盗窃发生时，乙正在影剧院看电影。由此可以推出（ ）。
# A.甲、乙、丙都是窃贼
# B.甲和乙都是窃贼
# C.丙是窃贼
# D.甲是窃贼

# 运行代码后，第3条的结果为 unsat，即对应原选项 C 是正确的。

# a,b,c => 甲乙丙三人， true为盗贼
a = Bool('a')  # 若甲是窃贼 则a为真
b = Bool('b')
c = Bool('c')


def build_solver():
    solver = Solver()
    # 给solver添加约束条件
    solver.add(If(a, 1, 0) + If(b, 1, 0) + If(c, 1, 0) >= 1)  # 条件1：三人至少有一个是窃贼
    solver.add(Implies(a, b))  # 条件2：如甲是窃贼 则乙一定是同案犯
    solver.add(Not(b))  # 条件3：乙一定不是
    return solver


if __name__ == "__main__":
    solver = build_solver()
    # 采用反证法 把各选项的 *否定* 添加进solver中 若冲突将返回unsat 原选项正确
    solver.add(Not(And(a, b, c)))  # 甲、乙、丙都是窃贼
    print(solver.check())  # will output "sat"

    solver = build_solver()
    solver.add(Not(And(a, b)))  # 甲和乙都是窃贼
    print(solver.check())  # will output "sat"

    solver = build_solver()
    solver.add(Not(c))  # 丙是窃贼
    print(solver.check())  # will output "unsat"

    solver = build_solver()
    solver.add(Not(a))  # 甲是窃贼
    print(solver.check())  # will output "sat"
