from z3 import *

if __name__ == "__main__":
    x = Int('x')
    y = Int('y')

    s = Solver()
    print(s)  # []

    s.add(x > 10, y == x + 2)
    print(s)  # [x > 10, y == x + 2]
    print("Solving constraints in the solver s ...")
    print(s.check())  # sat

    print("Create a new scope...")
    s.push()
    s.add(y < 11)
    print(s)  # [x > 10, y == x + 2, y < 11]
    print("Solving updated set of constraints...")
    print(s.check())  # unsat

    print("Restoring state...")
    s.pop()
    print(s)  # [x > 10, y == x + 2]
    print("Solving restored set of constraints...")
    print(s.check())  # sat
