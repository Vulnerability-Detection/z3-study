from z3 import *

if __name__ == "__main__":
    fp = Fixedpoint()
    fp.set(engine='datalog')

    s = BitVecSort(3)
    edge = Function('edge', s, s, BoolSort())
    path = Function('path', s, s, BoolSort())
    a = Const('a', s)
    b = Const('b', s)
    c = Const('c', s)

    fp.register_relation(path, edge)
    fp.declare_var(a, b, c)
    fp.rule(path(a, b), edge(a, b))
    fp.rule(path(a, c), [edge(a, b), path(b, c)])

    v1 = BitVecVal(1, s)
    v2 = BitVecVal(2, s)
    v3 = BitVecVal(3, s)
    v4 = BitVecVal(4, s)

    fp.fact(edge(v1, v2))
    fp.fact(edge(v1, v3))
    fp.fact(edge(v2, v4))

    print("current set of rules")
    print(fp)
    # (declare - rel path ((_ BitVec 3)(_ BitVec 3)))
    # (declare - rel edge ((_ BitVec 3)(_ BitVec 3)))
    # (declare - var A (_ BitVec 3))
    # (declare - var B (_ BitVec 3))
    # (declare - var C (_ BitVec 3))
    # (rule(= > ( and (edge C B)) (path C B)))
    # (rule(= > ( and (edge C B)(path B A)) (path C A)))
    # (rule(edge  # b001 #b010))
    # (rule(edge  # b001 #b011))
    # (rule(edge  # b010 #b100))
    print()

    print(fp.query(path(v1, v4)), "yes we can reach v4 from v1")  # sat yes we can reach v4 from v1
    print(fp.query(path(v3, v4)), "no we cannot reach v4 from v3")  # unsat no we cannot reach v4 from v3
