from z3 import *

if __name__ == "__main__":
    # Declare a List of integers
    # 声明一个整数列表
    List = Datatype('List')
    # Constructor cons: (Int, List) -> List
    # 构造方法：（Int，List）-> List
    List.declare('cons', ('car', IntSort()), ('cdr', List))
    # Constructor nil: List
    # 构造函数nil：列表
    List.declare('nil')
    # Create the datatype
    # 创建数据类型
    List = List.create()
    print(is_sort(List))  # True
    print()
    cons = List.cons
    car = List.car
    cdr = List.cdr
    nil = List.nil
    # cons, car and cdr are function declarations, and nil a constant
    print(is_func_decl(cons))  # True
    print(is_expr(nil))  # True

    l1 = cons(10, cons(20, nil))
    print(l1)  # cons(10, cons(20, nil))
    print(simplify(cdr(l1)))  # cons(20, nil)
    print(simplify(car(l1)))  # 10
    print(simplify(l1 == nil))  # False
