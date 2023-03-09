from z3 import *

if __name__ == "__main__":
    d, a, t, v_i, v_f = Reals('d a t v__i v__f')
    equations = [
        d == v_i * t + (a * t ** 2) / 2,
        v_f == v_i + a * t,
    ]
    print("Kinematic equations:")
    print(equations)  # [d == v__i*t + (a*t**2)/2, v__f == v__i + a*t]

    # Given v_i, v_f and a, find d
    problem = [
        v_i == 30,
        v_f == 0,
        a == -8
    ]
    print("Problem:")
    print(problem)  # [v__i == 30, v__f == 0, a == -8]

    print("Solution:")
    solve(equations + problem)  # [a = -8, v__f = 0, v__i = 30, t = 15/4, d = 225/4]
