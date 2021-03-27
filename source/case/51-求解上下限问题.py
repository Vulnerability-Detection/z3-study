from z3 import *

if __name__ == "__main__":
    s = Then(With('simplify', arith_lhs=True, som=True),
             'normalize-bounds', 'lia2pb', 'pb2bv',
             'bit-blast', 'sat').solver()
    x, y, z = Ints('x y z')
    solve_using(s,
                x > 0, x < 10,
                y > 0, y < 10,
                z > 0, z < 10,
                3 * y + 2 * x == z)  # [x = 3, y = 1, z = 9]
    # It fails on the next example (it is unbounded)
    # 在下一个示例中失败（它是无界的）
    print()
    s.reset()
    solve_using(s, 3 * y + 2 * x == z)  # failed to solve
