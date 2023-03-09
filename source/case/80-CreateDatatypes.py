from z3 import *

if __name__ == "__main__":
    TreeList = Datatype('TreeList')
    Tree = Datatype('Tree')
    Tree.declare('leaf', ('val', IntSort()))
    Tree.declare('node', ('left', TreeList), ('right', TreeList))
    TreeList.declare('nil')
    TreeList.declare('cons', ('car', Tree), ('cdr', TreeList))

    Tree, TreeList = CreateDatatypes(Tree, TreeList)

    t1 = Tree.leaf(10)
    tl1 = TreeList.cons(t1, TreeList.nil)
    t2 = Tree.node(tl1, TreeList.nil)
    print(t2)  # node(cons(leaf(10), nil), nil)
    print(simplify(Tree.val(t1)))  # 10

    t1, t2, t3 = Consts('t1 t2 t3', TreeList)
    solve(Distinct(t1, t2, t3))  # [t2 = cons(leaf(1), nil), t1 = nil, t3 = cons(leaf(2), nil)]
