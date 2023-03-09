from z3 import *

if __name__ == "__main__":
    Type = DeclareSort('Type')
    subtype = Function('subtype', Type, Type, BoolSort())
    array_of = Function('array_of', Type, Type)
    root = Const('root', Type)

    x, y, z = Consts('x y z', Type)

    axioms = [ForAll(x, subtype(x, x)),
              ForAll([x, y, z], Implies(And(subtype(x, y), subtype(y, z)), subtype(x, z))),
              ForAll([x, y], Implies(And(subtype(x, y), subtype(y, x)), x == y)),
              ForAll([x, y, z], Implies(And(subtype(x, y), subtype(x, z)), Or(subtype(y, z), subtype(z, y)))),
              ForAll([x, y], Implies(subtype(x, y), subtype(array_of(x), array_of(y)))),
              ForAll(x, subtype(root, x))]
    s = Solver()
    s.add(axioms)
    # print(s)
    print()
    print(s.check())  # sat
    print("Interpretation for Type:")
    print(s.model()[Type])  # [Type!val!1, Type!val!0]
    print("Model:")
    print(s.model())
