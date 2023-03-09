from z3 import *

if __name__ == "__main__":
    d, a, t, v_i, v_f = Reals('d a t v__i v__f')

    equations = [
        d == v_i * t + (a * t ** 2) / 2,
        v_f == v_i + a * t,
    ]

    # Given v_i, t and a, find d
    problem = [
        v_i == 0,
        t == 4.10,
        a == 6
    ]

    solve(equations + problem)  # [a = 6, t = 41/10, v__i = 0, v__f = 123/5, d = 5043/100]

    # Display rationals in decimal notation
    # 用十进制表示法显示有理数
    set_option(rational_to_decimal=True)

    solve(equations + problem)  # [a = 6, t = 4.1, v__i = 0, v__f = 24.6, d = 50.43]
