from z3 import *

if __name__ == "__main__":
    def DeclareList(sort):
        List = Datatype('List_of_%s' % sort.name())
        List.declare('cons', ('car', sort), ('cdr', List))
        List.declare('nil')
        return List.create()


    IntList = DeclareList(IntSort())
    RealList = DeclareList(RealSort())
    IntListList = DeclareList(IntList)

    l1 = IntList.cons(10, IntList.nil)
    print(l1)  # cons(10, nil)
    print(IntListList.cons(l1, IntListList.cons(l1, IntListList.nil)))  # cons(cons(10, nil), cons(cons(10, nil), nil))
    print(RealList.cons("1/3", RealList.nil))  # cons(1/3, nil)

    print(l1.sort())  # List_of_Int
