# Python中的z3 api-Advanced

- 源地址：https://ericpony.github.io/z3py-tutorial/advanced-examples.htm

## 1、进阶主题

请向leonardo@microsoft.com发送反馈，评论和/或更正。 您的评论非常有价值。

## 2、表达式，排序和声明

**在Z3中，表达式，排序和声明称为AST。** 
**AST是有向无环图。** 
每个表达式都有一个排序（aka类型）。 
方法sort（）检索表达式的排序。

```python
# 示例63
from z3 import *

if __name__ == "__main__":
    x = Int('x')
    y = Real('y')
    print((x + 1).sort())  # Int
    print((y + 1).sort())  # Real
    print((x >= 2).sort())  # Bool

```

如果n1和n2是相同的AST，则**函数eq（n1，n2）返回True**。 这是一个结构测试。

```python
# 示例64
from z3 import *

if __name__ == "__main__":
    x, y = Ints('x y')
    print(eq(x + y, x + y))  # True
    print(eq(x + y, y + x))  # False
    n = x + y
    print(eq(n, x + y))  # True
    # x2 is eq to x
    x2 = Int('x')
    print(eq(x, x2))  # True
    # the integer variable x is not equal to
    # the real variable x
    print(eq(Int('x'), Real('x')))  # False

```

方法hash（）返回AST节点的哈希码。 
**如果eq（n1，n2）返回True，则n1.hash（）等于n2.hash（）。**

```python
# 示例65
from z3 import *

if __name__ == "__main__":
    x = Int('x')
    print((x + 1).hash())  # 1880882057
    print((1 + x).hash())  # 3655631788
    print(eq(x + 1, 1 + x))  # False
    print(x.sort().hash())  # 2867189042

```

Z3表达式可分为**三个基本组：应用程序，量词和有界/自由变量。** 
如果您的问题不包含通用/现有量词，则只需要应用程序。 
尽管我们说Int（'x'）是一个整数“变量”，但从技术上讲它是一个整数常数，并且内部表示为具有0个参数的函数应用程序。 
每个应用程序都与一个声明关联，并包含0个或多个参数。 
**方法decl（）返回与应用程序关联的声明。** 
**方法num_args（）返回应用程序的参数数量，并返回arg（i）参数之一。** 
**如果n是一个表达式，则函数is_expr（n）返回True。** 
**同样，如果n是应用程序（声明），则is_app（n）（is_func_decl（n））返回True。**

```python
# 示例66
from z3 import *

if __name__ == "__main__":
    x = Int('x')
    print("is expression: ", is_expr(x))  # is expression:  True
    n = x + 1
    print("is application:", is_app(n))  # is application: True
    print("decl:          ", n.decl())  # decl:           +
    print("num args:      ", n.num_args())  # num args:       2
    for i in range(n.num_args()):
        print("arg(", i, ") ->", n.arg(i))
        # arg( 0 ) -> x
        # arg(1) -> 1

```

声明有名称，可以使用name（）方法检索它们。 
（函数）声明具有Arity，域和范围排序。

```python
# 示例67
from z3 import *

if __name__ == "__main__":
    x = Int('x')
    x_d = x.decl()
    print("is_expr(x_d):     ", is_expr(x_d))  # is_expr(x_d):      False
    print("is_func_decl(x_d):", is_func_decl(x_d))  # is_func_decl(x_d): True
    print("x_d.name():       ", x_d.name())  # x_d.name():        x
    print("x_d.range():      ", x_d.range())  # x_d.range():       Int
    print("x_d.arity():      ", x_d.arity())  # x_d.arity():       0
    # x_d() creates an application with 0 arguments using x_d.
    # x_d（）使用x_d创建带有0个参数的应用程序。
    print("eq(x_d(), x):     ", eq(x_d(), x))  # eq(x_d(), x):      True
    print("\n")
    
    # f is a function from (Int, Real) to Bool
    # f是从（Int，Real）到Bool的函数
    f = Function('f', IntSort(), RealSort(), BoolSort())
    print("f.name():         ", f.name())  # f.name():          f
    print("f.range():        ", f.range())  # f.range():         Bool
    print("f.arity():        ", f.arity())  # f.arity():         2
    for i in range(f.arity()):
        print("domain(", i, "): ", f.domain(i))
        
    # f(x, x) creates an application with 2 arguments using f.
    # f（x，x）使用f创建带有2个参数的应用程序。
    print(f(x, x))  # f(x, ToReal(x))
    print(eq(f(x, x).decl(), f))  # True

```

内置声明使用其种类进行标识。 **使用方法kind（）检索种类。** 
内置声明的完整列表可以在Z3发行版的文件z3consts.py（z3_api.h）中找到。

```python
# 示例68
from z3 import *

if __name__ == "__main__":
    x, y = Ints('x y')
    print((x + y).decl().kind())  # 518
    print((x + y).decl().kind() == Z3_OP_ADD)  # True
    print((x + y).decl().kind() == Z3_OP_SUB)  # False

```

下面的示例演示如何在Z3表达式中替换子表达式。

```python
# 示例69
from z3 import *

if __name__ == "__main__":
    x, y = Ints('x y')
    f = Function('f', IntSort(), IntSort(), IntSort())
    g = Function('g', IntSort(), IntSort())
    n = f(f(g(x), g(g(x))), g(g(y)))
    print(n)  # f(f(g(x), g(g(x))), g(g(y)))

    # substitute g(g(x)) with y and g(y) with x + 1
    # 用y替换g（g（x））并用x + 1替换g（y）
    print(substitute(n, (g(g(x)), y), (g(y), x + 1)))  # f(f(g(x), y), g(x + 1))

```

函数Const（name，sort）声明给定排序的常量（即变量）。 
例如，**函数Int（name）和Real（name）是Const（name，IntSort（））和Const（name，RealSort（））的简写。**

```python
# 示例70
from z3 import *

if __name__ == "__main__":
    x = Const('x', IntSort())
    print(eq(x, Int('x')))  # True

    a, b = Consts('a b', BoolSort())
    print(And(a, b))  # And(a, b)

```

## 3、数组

作为制定数学计算理论程序的一部分，McCarthy提出了一种以**选择存储公理为特征的阵列基本理论**。 
表达式**Select（a，i）返回存储在数组a的位置i处的值**； 然后**Store（a，i，v）返回一个与a相同的新数组，但是在位置i上包含值v。**
在Z3Py中，我们还可以将Select（a，i）编写为a [i]。

```python
# 示例71
from z3 import *

if __name__ == "__main__":
    # Use I as an alias for IntSort()
    # 使用I作为IntSort（）的别名
    I = IntSort()
    # A is an array from integer to integer
    # A是一个从整数到整数的数组
    A = Array('A', I, I)
    x = Int('x')

    print(A[x])  # A[x]
    print(Select(A, x))  # A[x]
    print(Store(A, x, 10))  # Store(A, x, 10)
    print(simplify(Select(Store(A, 2, x + 1), 2)))  # 1 + x

```

默认情况下，Z3假定数组在select之上是可扩展的。 
换句话说，Z3还强制要求，如果两个数组在所有位置上都一致，则数组相等。

Z3还包含对阵列操作的各种扩展，这些扩展仍可确定并适用于有效的饱和过程
（此处为有效手段，具有NP完全可满足性的复杂性）。 
我们在下面使用示例集合来描述这些扩展。 有关这些扩展的其他背景信息，
请参见通用和高效阵列决策程序。

**Z3中的数组用于建模无边界或非常大的数组。**
数组不应用于对值的有限有限集合进行建模。 
使用列表推导创建不同的变量通常会更有效。

```python
# 示例72
from z3 import *

if __name__ == "__main__":
    # We want an array with 3 elements.
    # 1. Bad solution
    X = Array('x', IntSort(), IntSort())
    # Example using the array
    print(X[0] + X[1] + X[2] >= 0)  # x[0] + x[1] + x[2] >= 0

    # 2. More efficient solution
    X = IntVector('x', 3)
    print(X[0] + X[1] + X[2] >= 0)  # x__0 + x__1 + x__2 >= 0
    print(Sum(X) >= 0)  # x__0 + x__1 + x__2 >= 0

```

### 1、Select and Store

让我们首先检查数组的基本属性。 
假设A是一个整数数组，则约束A [x] == x，Store（A，x，y）== A对于包含映射到x的索引x的数组是可满足的，并且当x == y。 
我们可以解决这些约束。

```python
# 示例73
from z3 import *

if __name__ == "__main__":
    A = Array('A', IntSort(), IntSort())
    x, y = Ints('x y')
    solve(A[x] == x, Store(A, x, y) == A)  # [A = Store(K(Int, 2), 0, 0), y = 0, x = 0]

```

数组变量的解释/解决方案与用于函数的解释/解决方案非常相似。

如果添加约束x！= y，问题将变得无法解决/无法实现。

```python
# 示例74
from z3 import *

if __name__ == "__main__":
    A = Array('A', IntSort(), IntSort())
    x, y = Ints('x y')
    solve(A[x] == x, Store(A, x, y) == A, x != y)  # no solution

```

### 2、常量数组

可以使用K（s，v）构造在Z3Py中指定将所有索引映射到某个固定值的数组，其中s是排序/类型，v是表达式。 
K（s，v）返回一个数组，该数组将s的任何值映射到v。
下面的示例定义一个仅包含1的常量数组。

```python
# 示例75
from z3 import *

if __name__ == "__main__":
    AllOne = K(IntSort(), 1)
    a, i = Ints('a i')
    solve(a == AllOne[i])  # [a = 1]
    # The following constraints do not have a solution
    # 以下约束没有解决方案
    solve(a == AllOne[i], a != 1)  # no solution

```

## 4、Datatypes

从诸如ML之类的编程语言中已知的代数数据类型为指定通用数据结构提供了一种方便的方法。
记录和元组是**代数数据**类型的特例，标量（枚举类型）也是如此。
但是**代数数据类型更为通用**。它们可用于指定有限列表，树和其他递归结构。

下面的示例演示如何在Z3Py中声明列表。它比使用SMT 2.0前端更为冗长，但比使用Z3 C API简单得多。
它包括两个阶段。首先，我们必须声明新的数据类型，其构造函数和访问器。
函数Datatype（'List'）声明一个“占位符”，它将包含构造函数和访问器声明。
方法clarify（cname，（aname，sort）+）声明一个具有给定访问器的名为cname的构造函数。
每个访问器都有一个关联的排序或对要声明的数据类型的引用。
例如，clarify（'cons'，（'car'，IntSort（）），（'cdr'，List））声明名为cons的构造函数，该构造函数使用整数和List来构建新的List。
它还声明了accessor car和cdr。访问车提取cons单元的整数，并cdr cons单元的列表。
声明所有构造函数后，我们使用create（）方法在Z3中创建实际的数据类型。 
Z3Py使新的Z3声明和常量可用作新对象的插槽。

```python
# 示例76
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

```

以下示例演示如何定义给定排序的Python函数创建给定排序的列表。

```python
# 示例77
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

```

上面的示例演示Z3支持运算符重载。 
有几个名为cons的函数，但是它们不同，因为它们接收和/或返回不同种类的值。 
请注意，不必为排序列表的每个实例使用不同的排序名称。 
也就是说，表达式'List_of_％s'％sort.name（）是不必要的，我们仅使用它来提供更有意义的名称。

如上所述，枚举类型是代数数据类型的特殊情况。 
下面的示例声明一个枚举类型，该枚举类型由三个值组成：红色，绿色和蓝色。

```python
# 示例78
from z3 import *

if __name__ == "__main__":
    Color = Datatype('Color')
    Color.declare('red')
    Color.declare('green')
    Color.declare('blue')
    Color = Color.create()

    print(is_expr(Color.green))  # True
    print(Color.green == Color.blue)  # green == blue
    print(simplify(Color.green == Color.blue))  # False

    # Let c be a constant of sort Color
    # 令c为排序常数Color
    c = Const('c', Color)
    # Then, c must be red, green or blue
    # 然后，c必须是红色，绿色或蓝色
    prove(Or(c == Color.green, c == Color.blue, c == Color.red))  # proved

```

Z3Py还提供了以下快捷方式来声明枚举排序。

```python
# 示例79
from z3 import *

if __name__ == "__main__":
    Color, (red, green, blue) = EnumSort('Color', ('red', 'green', 'blue'))

    print(green == blue)  # green == blue
    print(simplify(green == blue))  # False

    c = Const('c', Color)
    solve(c != green, c != blue)  # [c = red]

```

也可以声明相互递归的数据类型。 
唯一的区别是我们使用函数CreateDatatypes而不是方法create（）来创建相互递归的数据类型。

```python
# 示例80
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

```

## 5、未解释的排序（Uninterpreted Sorts）

纯一阶逻辑中的功能和常数符号未解释或自由表示，这意味着没有附加先验解释。 
这与算术运算符（例如+和-）具有固定的标准解释相反。 
未解释的函数和常量具有最大的灵活性； 它们允许进行任何与函数或常量约束一致的解释。

为了说明未解释的函数和常量，让我们引入一个（未解释的）排序A，常量x，y遍及A。
最后，使f为一个未解释的函数，它接受一个A类型的参数，并得出A值。 
该示例说明了如何强制解释，其中对x两次应用f会再次导致x，但是对x一次应用f与x不同。

```python
# 示例81
from z3 import *

if __name__ == "__main__":
    A = DeclareSort('A')
    x, y = Consts('x y', A)
    f = Function('f', A, A)

    s = Solver()
    s.add(f(f(x)) == x, f(x) == y, x != y)

    print(s.check())  # sat
    m = s.model()
    print(m)
    # [x = A!val!0,
    # y = A!val!1,
    # f = [A!val!1 -> A!val!0, else -> A!val!1]]
    print("interpretation assigned to A:")
    print(m[A])  # [A!val!0, A!val!1]

```

最终的模型为A中的元素引入了抽象值，因为未解释排序A。 
模型中对f的解释在x和y的两个值之间切换，这两个值是不同的。 
**表达式m [A]返回模型m中未解释的类别A的解释（Universe）。**

## 6、量词

Z3可以解决包含算术，位向量，布尔值，数组，函数和数据类型在内的**无量纲问题。**
Z3还接受并可以使用**使用量词的公式**。 
一般而言，它不再是此类公式的决策程序（并且由于充分的原因，因为一阶逻辑可能没有决策程序）。

```python
# 示例82
from z3 import *

if __name__ == "__main__":
    f = Function('f', IntSort(), IntSort(), IntSort())
    x, y = Ints('x y')
    print(ForAll([x, y], f(x, y) == 0))  # ForAll([x, y], f(x, y) == 0)
    print(Exists(x, f(x, x) >= 0))  # Exists(x, f(x, x) >= 0)

    a, b = Ints('a b')
    solve(ForAll(x, f(x, x) == 0), f(a, b) == 1)  # [b = 2, a = 0, f = [(0, 2) -> 1, else -> 0]]

```

尽管如此，Z3通常能够处理涉及量词的公式。
它使用多种方法来处理量词。
最丰富的方法是使用**基于模式的量词实例化。**
这种方法允许根据**量词上的模式注释，使用出现在当前搜索上下文中的基本术语实例化量化公式。** 
Z3还包含一个基于模型的量词实例化组件，该组件使用模型构造来找到用于实例化量词的良好条件。 
Z3还处理许多可确定的片段。

请注意，在前面的示例中，常数x和y用于创建量化公式。
这是简化Z3Py中量化公式的构造的“技巧”。
在内部，这些常量将替换为有界变量。下一个示例说明了这一点。
**方法body（）检索量化的表达式。**
在所得公式中，有界变量是自由的。
函数Var（index，sort）使用给定的index和sort创建一个有界/自由变量。

```python
# 示例83
from z3 import *

if __name__ == "__main__":
    f = Function('f', IntSort(), IntSort(), IntSort())
    x, y = Ints('x y')
    f = ForAll([x, y], f(x, y) == 0)
    print(f.body())  # f(Var(1), Var(0)) == 0

    v1 = f.body().arg(0).arg(0)  # Var(1)
    print(v1)
    print(eq(v1, Var(1, IntSort())))  # True

```

### 1、用量词建模

假设我们要为具有单一继承的面向对象的类型系统建模。 
我们将需要一个谓词来进行子类型输入。 
子类型化应该是部分顺序，并尊重单一继承。 
对于某些内置类型构造函数，例如array_of，子类型应该是单调的。

```python
# 示例84
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

```

### 2、模式

Stanford **Pascal验证器**和随后的**Simplify定理证明器**率先使用基于模式的量词实例化。 
基于模式的量词实例化的基本思想在某种意义上是直截了当的：使用包含所有绑定变量的模式对量化公式进行注释。 
因此，模式是一个表达式（不包含绑定操作，例如量词），它包含一个由量词绑定的变量。 
然后，只要在搜索过程中创建了与模式匹配的术语，就实例化量词。 
从概念上讲，这是一个简单的起点，但是有一些重要的微妙之处。

在以下示例中，前两个选项确保禁用基于模型的量词实例化引擎。 
我们还用模式f（g（x））注释了量化公式。 
由于没有该模式的基本实例，因此无法实例化量词，并且Z3无法显示该公式不满足要求。

```python
# 示例85
from z3 import *

if __name__ == "__main__":
    f = Function('f', IntSort(), IntSort())
    g = Function('g', IntSort(), IntSort())
    a, b, c = Ints('a b c')
    x = Int('x')

    s = Solver()
    s.set(auto_config=False, mbqi=False)
    s.add(ForAll(x, f(g(x)) == x, patterns=[f(g(x))]), g(a) == c, g(b) == c, a != b)

    # Display solver state using internal format
    # 使用内部格式显示求解器状态
    print(s.sexpr())
    # (declare - fun f (Int) Int)
    # (declare - fun g (Int) Int)
    # (declare - fun c () Int)
    # (declare - fun a () Int)
    # (declare - fun b () Int)
    # (assert (forall ((x Int)) (! (= (f (g x)) x):pattern((f(g x))))))
    # (assert (= (g a) c))
    # (assert (= (g b) c))
    # (assert (distinct a b))
    print(s.check())  # unknown

```

当使用更宽松的模式g（x）时。 Z3证明该公式不令人满意。 
更具恢复性的模式将实例化的数量减至最少（并可能改善性能），但它们也可能使Z3“不那么完整”。

```python
# 示例86
from z3 import *

if __name__ == "__main__":
    f = Function('f', IntSort(), IntSort())
    g = Function('g', IntSort(), IntSort())
    a, b, c = Ints('a b c')
    x = Int('x')

    s = Solver()
    s.set(auto_config=False, mbqi=False)
    s.add(ForAll(x, f(g(x)) == x, patterns=[g(x)]), g(a) == c, g(b) == c, a != b)

    # Display solver state using internal format
    # 使用内部格式显示求解器状态
    print(s.sexpr())
    # (declare - fun g (Int) Int)
    # (declare - fun f (Int) Int)
    # (declare - fun c () Int)
    # (declare - fun a () Int)
    # (declare - fun b () Int)
    # (assert (forall ((x Int)) (! (= (f (g x)) x):pattern((g x)))))
    # (assert (= (g a) c))
    # (assert (= (g b) c))
    # (assert (distinct a b))
    print(s.check())  # unsat

```

某些模式可能还会创建长的实例化链。 考虑以下断言。

```python
ForAll([x, y], Implies(subtype(x, y),subtype(array_of(x), array_of(y))),
       patterns=[subtype(x, y)])
```

只要存在形式子类型 `subtype(s, t)`. 的某个基本项，就可以实例化公理。 
该实例化会导致一个新的基础术语子类型subtype(array_of(s), array_of(t))，从而启用新的实例化。 
**这种不希望的情况称为匹配循环。 Z3使用许多启发式方法来打破匹配循环。**

在详细说明细节之前，我们应该解决一个重要的第一个问题。 
什么定义了搜索过程中创建的术语？ 
在大多数SMT求解器和简化定理证明者的上下文中，术语作为输入公式的一部分存在，
它们当然也可以通过实例化量词来创建，但是当断言等式时也会隐式创建术语。 
最后一点意味着要考虑所有项的全等，并且模式匹配以模地等式进行。 
我们称匹配问题为**E-matching**。 例如，如果我们具有以下相等性：

```python
# 示例87
from z3 import *

if __name__ == "__main__":
    f = Function('f', IntSort(), IntSort())
    g = Function('g', IntSort(), IntSort())
    a, b, c = Ints('a b c')
    x = Int('x')

    s = Solver()
    s.set(auto_config=False, mbqi=False)
    s.add(ForAll(x, f(g(x)) == x, patterns=[f(g(x))]),
          a == g(b),b == c,f(a) != c)

    print(s.check())  # unsat

```

项f（a）和f（g（b））在等式上相等。 
可以匹配模式f（g（x））并将x绑定到b，并推导等式f（g（b））== b。

尽管E-matching是一个NP完全问题，但较大的验证问题中的间接费用的主要来源是在一组不断发展的术语和等式的背景下匹配数千种模式。 
Z3使用术语索引技术集成了高效的E-matching引擎。

### 3、多种模式

在某些情况下，没有包含所有绑定变量且不包含解释符号的模式。 
在这些情况下，我们使用多模式。 
在下面的示例中，量化公式指出f为内射。 
该量化公式使用多模式MultiPattern（f（x），f（y））注释。

```python
# 示例88
from z3 import *

if __name__ == "__main__":
    A = DeclareSort('A')
    B = DeclareSort('B')
    f = Function('f', A, B)
    a1, a2 = Consts('a1 a2', A)
    b = Const('b', B)
    x, y = Consts('x y', A)

    s = Solver()
    s.add(a1 != a2, f(a1) == b, f(a2) == b,
          ForAll([x, y], Implies(f(x) == f(y), x == y), patterns=[MultiPattern(f(x), f(y))])
          )
    print(s)
    print(s.check())  # unsat

```

对于每对出现的f实例化量化公式。 
一个简单的技巧就可以以仅需要线性数量的实例化的方式来公式化f的内射性。 
诀窍是要认识到f仅在具有部分逆的情况下才是内射的。

```python
# 示例89
from z3 import *

if __name__ == "__main__":
    A = DeclareSort('A')
    B = DeclareSort('B')
    f = Function('f', A, B)
    finv = Function('finv', B, A)
    a1, a2 = Consts('a1 a2', A)
    b = Const('b', B)
    x, y = Consts('x y', A)

    s = Solver()
    s.add(a1 != a2,f(a1) == b,f(a2) == b,ForAll(x, finv(f(x)) == x))
    print(s)
    print(s.check())  # unsat

```

### 4、其他属性

在Z3Py中，支持以下附加属性：
qid（用于调试的量化标识符），
权重（到量化器实例化模块的提示：“更多的权重等于更少的实例”），
no_patterns（不应用作模式的表达式），
skid（标识符） 用于创建skolem常数/函数的前缀。

## 7、多重求解器

在Z3Py和Z3 4.0中，可以同时使用多个求解器。
将一个断言/公式从一个求解器复制到另一个求解器也很容易。

```python
# 示例90
from z3 import *

if __name__ == "__main__":
    x, y = Ints('x y')
    s1 = Solver()
    s1.add(x > 10, y > 10)
    s2 = Solver()
    # solver s2 is empty
    print(s2)  # []
    # copy assertions from s1 to s2
    # 将断言从s1复制到s2
    s2.add(s1.assertions())
    print(s2)  # [x > 10, y > 10]

```

## 8、Unsat Cores and Soft Constraints

Z3Py还支持*unsat core*提取。 
基本思想是使用假设，即我们要跟踪的辅助命题变量。 
Z3 SMT 2.0前端和其他Z3前端中也提供了假设。 
它们用于提取无法满足的核心。 它们也可以用来“撤消”约束。 
请注意，假设并不是真正的软约束，但可以将其用于实施。

```python
# 示例91
from z3 import *

if __name__ == "__main__":
    p1, p2, p3 = Bools('p1 p2 p3')
    x, y = Ints('x y')
    # We assert Implies(p, C) to track constraint C using p
    # 我们断言Implies（p，C）使用p跟踪约束C
    s = Solver()
    s.add(Implies(p1, x > 10),
          Implies(p1, y > x),
          Implies(p2, y < 5),
          Implies(p3, y > 0))
    print(s)
    print()
    # Check satisfiability assuming p1, p2, p3 are true
    # 假设p1，p2，p3为真，则检查可满足性
    print(s.check(p1, p2, p3))  # unsat
    print(s.unsat_core())  # [p1, p2]

    # Try again retracting p2
    # 再试一次收回p2
    print(s.check(p1, p3))  # sat
    print(s.model())  # [p3 = True, y = 12, p1 = True, p2 = False, x = 11]

```

上面的示例还显示了布尔变量（p1）可用于跟踪多个约束。 
请注意，Z3不能保证非饱和核的数量最少。

## 9、格式化程序

Z3Py使用格式化程序（又称漂亮打印机）来显示公式，表达式，求解器和其他Z3对象。 
格式化程序支持许多配置选项。 
命令set_option（html_mode = False）使所有公式和表达式都以Z3Py表示法显示。

```python
# 示例92
from z3 import *

if __name__ == "__main__":
    x = Int('x')
    y = Int('y')
    print(x ** 2 + y ** 2 >= 1)  # x**2 + y**2 >= 1
    set_option(html_mode=False)
    print(x ** 2 + y ** 2 >= 1)  # x**2 + y**2 >= 1

```

默认情况下，如果显示的对象太大，则Z3Py将截断输出。 
Z3Py使用…表示输出被截断。 
可以设置以下配置选项来控制Z3Py格式化程序的行为：

**max_depth：**最大表达式深度。 较深的表达式将替换为…。
**max_args：**每个节点要显示的最大参数数。
**rational_to_decimal：**如果为True，则将有理数显示为小数。
**precision：**以十进制表示法显示的数字的最大小数位数。
**max_lines：**要显示的最大行数。
**max_width：**最大线宽（这是对Z3Py的建议）。
**max_indent：**最大缩进。

```python
# 示例93
from z3 import *

if __name__ == "__main__":
    x = IntVector('x', 20)
    y = IntVector('y', 20)
    f = And(Sum(x) >= 0, Sum(y) >= 0)

    set_option(max_args=5)
    print("\ntest 1:")
    print(f)

    print("\ntest 2:")
    set_option(max_args=100, max_lines=10)
    print(f)

    print("\ntest 3:")
    set_option(max_width=300)
    print(f)

```

