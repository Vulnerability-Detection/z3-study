from z3 import *

if __name__ == "__main__":
    fp = Fixedpoint()
    a, b, c = Bools('a b c')

    fp.register_relation(a.decl(), b.decl(), c.decl())  # 申明关系
    fp.rule(a, b)  # 定义规则
    fp.rule(b, c)
    fp.set(engine='datalog')  # 设置引擎

    print("current set of rules", )
    print(fp)
    # (declare - rel b ())
    # (declare - rel a ())
    # (declare - rel c ())
    # (rule(= > ( and b) a))
    # (rule(= > ( and c) b))

    # 查询规则
    print(fp.query(a))  # unsat

    fp.fact(c)
    print("updated set of rules", )
    print(fp)
    # (declare - rel b ())
    # (declare - rel a ())
    # (declare - rel c ())
    # (rule(= > b a))
    # (rule(= > c b))
    # (rule c)

    print(fp.query(a))  # sat
    print(fp.get_answer())  # True
