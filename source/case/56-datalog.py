from z3 import *

if __name__ == "__main__":
    fp = Fixedpoint()
    a, b, c = Bools('a b c')

    fp.register_relation(a.decl(), b.decl(), c.decl())
    fp.rule(a, b)
    fp.rule(b, c)
    fp.fact(c)
    # 会报错=> "unknown parameter 'generate_explanations'
    # fp.set(generate_explanations=True, engine='datalog')
    fp.set(engine='datalog')

    print(fp.query(a))  # sat
    print(fp.get_answer())  # True
