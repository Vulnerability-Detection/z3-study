from z3 import *

if __name__ == "__main__":
    x, y, z = Reals('x y z')
    g = Goal()
    g.add(Or(x == 0, x == 1),
          Or(y == 0, y == 1),
          Or(z == 0, z == 1),
          x + y + z > 2)
    # Split all clauses
    # 拆分所有子句
    split_all = Repeat(OrElse(Tactic('split-clause'), Tactic('skip')))
    print(split_all(g))
    # [[x == 0, y == 0, z == 0, x + y + z > 2],
    #  [x == 0, y == 0, z == 1, x + y + z > 2],
    #  [x == 0, y == 1, z == 0, x + y + z > 2],
    #  [x == 0, y == 1, z == 1, x + y + z > 2],
    #  [x == 1, y == 0, z == 0, x + y + z > 2],
    #  [x == 1, y == 0, z == 1, x + y + z > 2],
    #  [x == 1, y == 1, z == 0, x + y + z > 2],
    #  [x == 1, y == 1, z == 1, x + y + z > 2]]
    print()

    split_at_most_2 = Repeat(OrElse(Tactic('split-clause'), Tactic('skip')), 1)
    print(split_at_most_2(g))
    # [[x == 0, y == 0, Or(z == 0, z == 1), x + y + z > 2],
    #  [x == 0, y == 1, Or(z == 0, z == 1), x + y + z > 2],
    #  [x == 1, y == 0, Or(z == 0, z == 1), x + y + z > 2],
    #  [x == 1, y == 1, Or(z == 0, z == 1), x + y + z > 2]]
    print()

    # Split all clauses and solve equations
    # 拆分所有子句并求解方程式
    split_solve = Then(Repeat(OrElse(Tactic('split-clause'), Tactic('skip'))),Tactic('solve-eqs'))
    print(split_solve(g))  # [[]]
