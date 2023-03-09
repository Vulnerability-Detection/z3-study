from z3 import *

if __name__ == "__main__":
    p1, p2, p3 = Bools('p1 p2 p3')
    x, y = Ints('x y')
    # We assert Implies(p, C) to track constraint C using p
    # 我们断言Implies（p，C）使用p跟踪约束C
    s = Solver()
    s.add(Implies(p1, x > 10),
          Implies(p1, y > x),
          Implies(p2, y < 5),
          Implies(p3, y > 0))
    print(s)
    print()
    # Check satisfiability assuming p1, p2, p3 are true
    # 假设p1，p2，p3为真，则检查可满足性
    print(s.check(p1, p2, p3))  # unsat
    print(s.unsat_core())  # [p1, p2]

    # Try again retracting p2
    # 再试一次收回p2
    print(s.check(p1, p3))  # sat
    print(s.model())  # [p3 = True, y = 12, p1 = True, p2 = False, x = 11]
