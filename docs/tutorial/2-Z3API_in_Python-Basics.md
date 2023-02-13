# Python中的z3 api-Basics

- 源地址：https://ericpony.github.io/z3py-tutorial/guide-examples.htm

## 1、介绍

Z3是由Microsoft Research开发的高性能定理证明器。 
Z3用于许多应用程序，例如：
软件/硬件验证和测试，约束解决，混合系统分析，安全性，生物学（计算机模拟分析）和几何问题。

本教程演示了Z3Py的主要功能：Python中的Z3 API。 无需Python背景即可阅读本教程。 
但是，在某个时候学习Python（一种有趣的语言！）非常有用，
并且有许多很棒的免费资源可供使用（Python教程）。

Z3发行版还包含C，.Net和OCaml API。 
Z3Py的源代码可在Z3发行版中找到，可以随时对其进行修改以满足您的需求。 
源代码还演示了如何在Z3 4.0中使用新功能。 Z3的其他出色前端包括Scala ^ Z3和SBV。

请向leonardo@microsoft.com发送反馈，评论和/或更正。 您的评论非常有价值。

## 2、入门

让我们从下面的简单示例开始：

```python
# 示例05
from z3 import *

if __name__ == "__main__":
    x = Int('x')
    y = Int('y')
    solve(x > 2, y < 10, x + 2 * y == 7) # [y = 0, x = 7]

```

函数 `Int('x')` 在Z3中创建一个名为x的整数变量。 solve函数求解约束系统。 
上面的示例使用两个变量x和y，以及三个约束。 像Python一样的Z3Py使用=进行赋值。 
用于比较的运算符<，<=，>，> =，==和！=。 
在上面的示例中，表达式x + 2 * y == 7是Z3约束。 Z3可以求解和处理公式。

下例显示了如何使用Z3公式/表达式**简化器**。

```python
# 示例06
from z3 import *

if __name__ == "__main__":
    x = Int('x')
    y = Int('y')
    print(simplify(x + y + 2 * x + 3))  # 3 + 3*x + y
    print(simplify(x < y + x + 2))  # Not(y <= -2)
    print(simplify(And(x + 1 >= 3, x ** 2 + x ** 2 + y ** 2 + 2 >= 5)))  # And(x >= 2, 2*x**2 + y**2 >= 3)

```

默认情况下，Z3Py（用于Web）使用数学符号显示公式和表达式。 
像往常一样，**∧是逻辑，v是逻辑或，依此类推。** 
命令set_option（html_mode = False）使所有公式和表达式都以Z3Py表示法显示。 
这也是Z3发行版随附的Z3Py脱机版本的默认模式。

```python
# 示例07
from z3 import *

if __name__ == "__main__":
    x = Int('x')
    y = Int('y')
    print(x ** 2 + y ** 2 >= 1)  # x**2 + y**2 >= 1
    set_option(html_mode=False)
    print(x ** 2 + y ** 2 >= 1)  # x**2 + y**2 >= 1

```

**Z3提供了遍历表达式的功能。**

```python
# 示例08
from z3 import *

if __name__ == "__main__":
    x = Int('x')
    y = Int('y')
    n = x + y >= 3
    print("num args: ", n.num_args())  # num args:  2
    print("children: ", n.children())  # children:  [x + y, 3]
    print("1st child:", n.arg(0))  # 1st child: x + y
    print("2nd child:", n.arg(1))  # 2nd child: 3
    print("operator: ", n.decl())  # operator:  >=
    print("op name:  ", n.decl().name())  # op name:   >=

```

Z3提供所有基本的数学运算。 
Z3Py使用与Python语言相同的运算符优先级。 
像Python一样，**是幂运算符。 Z3可以解决非线性多项式约束。

```python
# 示例09
from z3 import *

if __name__ == "__main__":
    x = Real('x')  # 实数
    y = Real('y')
    print(simplify(And(x ** 2 + y ** 2 > 3, x ** 3 + y < 5)))  # And(Not(x**2 + y**2 <= 3), Not(5 <= x**3 + y))
    solve(x ** 2 + y ** 2 > 3, x ** 3 + y < 5)  # [y = 2, x = 1/8]


```

过程Real('x')创建实数变量x。 
Z3Py可以表示任意大的整数，有理数（如上面的示例中所示）和无理代数。 
无理数代数是具有整数系数的多项式的根。 
在内部，**Z3精确地表示所有这些数字。** 
无理数以十进制表示，以便于读取结果。

```python
# 示例10
from z3 import *

if __name__ == "__main__":
    x = Real('x')
    y = Real('y')
    solve(x ** 2 + y ** 2 == 3, x ** 3 == 2)  # [y = -1.1885280594?, x = 1.2599210498?]

    set_option(precision=30)  # 设置精度
    print("Solving, and displaying result with 30 decimal places")
    solve(x ** 2 + y ** 2 == 3, x ** 3 == 2)
    # [y = -1.188528059421316533710369365015?,
    #  x = 1.259921049894873164767210607278?]

```

set_option过程用于配置Z3环境。 
它用于设置全局配置选项，例如结果的显示方式。 
选项set_option(precision=30)设置显示结果时使用的小数位数。 
**这 ？ 标记在1.2599210498中？ 表示输出被截断。**

以下示例演示了一个常见错误。 
表达式3/2是Python整数，而不是Z3有理数。 
该示例还显示了在Z3Py中创建有理数的不同方法。 
过程 **`Q(num, den)`创建一个Z3有理数**，其中num是分子，den是分母。 
**RealVal(1)创建一个代表数字1的Z3实数。**

```python
# 示例11
from z3 import *

if __name__ == "__main__":
    print(1 / 3)  # 0.3333333333333333
    print(RealVal(1) / 3)  # 1/3
    print(Q(1, 3))  # 1/3

    x = Real('x')
    print(x + 1 / 3)  # x + 3333333333333333/10000000000000000
    print(x + Q(1, 3))  # x + 1/3
    print(x + "1/3")  # x + 1/3
    print(x + 0.25)  # x + 1/4

```

**有理数也可以十进制表示。**

```python
# 示例12
from z3 import *

if __name__ == "__main__":
    x = Real('x')
    solve(3 * x == 1)  # [x = 1/3]

    set_option(rational_to_decimal=True)
    solve(3 * x == 1)  # [x = 0.3333333333?]

    set_option(precision=30)
    solve(3 * x == 1)  # [x = 0.333333333333333333333333333333?]

```

约束系统可能没有解决方案。 在这种情况下，我们说该系统不令人满意。

```python
# 示例13
from z3 import *

if __name__ == "__main__":
    x = Real('x')
    solve(x > 4, x < 0)  # no solution

```

像在Python中一样，注释以井号字符＃开头，并在行尾终止。 
**Z3Py不支持跨越多行的注释。**

```python
# 示例14
from z3 import *

if __name__ == "__main__":
    # This is a comment
    x = Real('x')  # comment: creating x
    print(x ** 2 + 2 * x + 2)  # x**2 + 2*x + 2 comment: 输出多项式

```

## 3、布尔逻辑

Z3支持布尔运算符：`And`, `Or`, `Not`, `Implies` (implication), `If` (if-then-else)。
“与”，“或”，“不”，“隐含”（蕴含），“隐含”（if-then-else）。 
双含义使用等号==表示。 
以下示例显示了如何解决一组简单的布尔约束。

```python
# 示例15
from z3 import *

if __name__ == "__main__":
    p = Bool('p')
    q = Bool('q')
    r = Bool('r')
    solve(Implies(p, q), r == Not(q), Or(Not(p), r))  # [q = True, p = False, r = False]

```

**Python布尔常量True和False可用于构建Z3布尔表达式。**

```python
# 示例16
from z3 import *

if __name__ == "__main__":
    p = Bool('p')
    q = Bool('q')
    print(And(p, q, True))  # And(p, q, True)
    print(simplify(And(p, q, True)))  # And(p, q)
    print(simplify(And(p, False)))  # False

```

以下示例使用多项式约束和布尔约束的组合。

```python
# 示例17
from z3 import *

if __name__ == "__main__":
    p = Bool('p')
    x = Real('x')
    solve(Or(x < 5, x > 10), Or(p, x ** 2 == 2), Not(p))  # [x = -1.4142135623?, p = False]

```

## 4、Solvers

Z3提供了不同的求解器。 
先前示例中使用的命令Solve是使用Z3求解器API实现的。 
可以在Z3发行版的z3.py文件中找到该实现。 
下面的示例演示了基本的Solver API。

```python
# 示例18
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

```

**命令Solver（）创建一个通用求解器。**
**可以使用add方法添加约束。**
我们说约束已在求解器中确定。**方法check（）解决断言的约束。**
如果找到解决方案，则结果 `sat`（令人满意）。如果不存在任何解决方案，结果将是 `unsat` （无法满足）。
我们也可以说断言约束系统是不可行的。
最后，求解器可能无法求解约束系统，并且返回未知数。

在某些应用程序中，我们希望探讨共享多个约束的几个类似问题。
我们可以使用命令push和pop做到这一点。
每个求解器维护一堆断言。
**命令push通过保存当前堆栈大小来创建新作用域。** 
**pop命令删除在它和匹配的push之间执行的所有断言。**
检查方法始终对求解器声明堆栈的内容进行操作。

以下示例显示了Z3无法解决的示例。
在这种情况下，求解器返回未知数。回想一下Z3可以解决非线性多项式约束，但是2 ** x不是多项式。

```python
# 示例19
from z3 import *

if __name__ == "__main__":
    x = Real('x')
    s = Solver()
    s.add(2 ** x == 3)
    print(s.check())  # unknown

```

下面的示例演示如何**遍历声明到求解器中的约束**，以及如何为check方法收集性能统计信息。

```python
# 示例20
from z3 import *

if __name__ == "__main__":
    x = Real('x')
    y = Real('y')
    s = Solver()
    s.add(x > 1, y > 1, Or(x + y > 3, x - y < 2))
    print("asserted constraints...")
    for c in s.assertions():
        print(c)

    print()
    print(s.check())  # sat
    print("statistics for the last check method...")
    print(s.statistics())
    # Traversing statistics
    print()
    for k, v in s.statistics():
        print("%s : %s" % (k, v))

# decisions : 2
# final checks : 1
# num checks : 1
# mk bool var : 4
# arith-lower : 1
# arith-upper : 3
# arith-make-feasible : 3
# arith-max-columns : 8
# arith-max-rows : 2
# num allocs : 284913
# rlimit count : 355
# max memory : 2.92
# memory : 2.6
# time : 0.01
```

当Z3为一组确定的约束找到解决方案时，命令检查返回sat。
我们说Z3满足约束集。 **我们说解决方案是一组声明约束的模型。** 
**模型是一种使每个声明的约束均成立的解释。** 
以下示例显示了检查模型的基本方法。

```python
# 示例21
from z3 import *

if __name__ == "__main__":
    x, y, z = Reals('x y z')
    s = Solver()
    s.add(x > 1, y > 1, x + y > 3, z - x < 10)
    print(s.check())  # sat
    print(s.model())  # [z = 0, y = 2, x = 3/2]
    m = s.model()
    print("x = %s" % m[x])  # x = 3/2

    print("traversing model...")
    for d in m.decls():
        print("%s = %s" % (d.name(), m[d]))
# z = 0
# y = 2
# x = 3/2

```

在上面的示例中，函数Reals（'x y z'）创建变量。 x，y和z。 它是以下各项的简写：

```
x = Real('x')
y = Real('y')
z = Real('z')
```

表达式m [x]返回模型m中x的解释。 
表达式"%s = %s" % (d.name(), m[d])返回一个字符串，其中第一个％s被替换为d的名称（即d.name（）），第二个被替换为d.name（）。 
％s带有d解释的文本表示形式（即m[d]）。
Z3Py会在需要时自动将Z3对象转换为文本表示形式。

## 5、算术（Arithmetic）

Z3支持实数和整数变量。 可以将它们混合在一个问题中。 
像大多数编程语言一样，Z3Py将在需要时自动添加强制转换，以将整数表达式转换为实数表达式。 
下面的示例演示了声明整数和实数变量的不同方法。

```python
# 示例22
from z3 import *

if __name__ == "__main__":
    x = Real('x')
    y = Int('y')
    a, b, c = Reals('a b c')
    s, r = Ints('s r')
    print(x + y + 1 + (a + s))  # x + ToReal(y) + 1 + a + ToReal(s)
    print(ToReal(y) + c)  # ToReal(y) + c

```

**函数ToReal将整数表达式转换为实数表达式。**
Z3Py支持所有基本的算术运算。

```python
# 示例23
from z3 import *

if __name__ == "__main__":
    a, b, c = Ints('a b c')
    d, e = Reals('d e')
    solve(a > b + 2, a == 2 * c + 10, c + b <= 1000, d >= e)  # [d = 0, c = 0, b = 0, e = 0, a = 10]

```

该命令simple将简单的转换应用于Z3表达式。

```python
# 示例24
from z3 import *

if __name__ == "__main__":
    x, y = Reals('x y')
    # Put expression in sum-of-monomials form
    # 将表达式以总和形式表示
    t = simplify((x + y) ** 3, som=True)  # x*x*x + 3*x*x*y + 3*x*y*y + y*y*y
    print(t)
    # Use power operator
    # 使用power运算符
    t = simplify(t, mul_to_power=True)  # x**3 + 3*x**2*y + 3*x*y**2 + y**3
    print(t)

```

命令help_simplify（）打印所有可用选项。 
Z3Py允许用户以两种样式编写选项。 
Z3内部选项名称以：开头，单词之间用-分隔。 
这些选项可以在Z3Py中使用。 
Z3Py还支持类似Python的名称，其中：被抑制，而-被_代替。 
下面的示例演示如何使用两种样式。

```python
# 示例25
from z3 import *

if __name__ == "__main__":
    x, y = Reals('x y')
    # Using Z3 native option names
    # 使用Z3本地选项名称
    print(simplify(x == y + 2, ':arith-lhs', True))  # x + -1*y == 2
    # Using Z3Py option names
    # 使用Z3Py选项名称
    print(simplify(x == y + 2, arith_lhs=True))  # x + -1*y == 2

    print("\nAll available options:")
    help_simplify()

```

Z3Py支持任意数量的数字。 
下面的示例演示如何使用较大的整数，有理数和无理数执行基本算术。 
Z3Py仅支持代数无理数。 代数无理数足以表示多项式约束系统的解。 
Z3Py将始终以十进制表示形式显示非理性数字，因为它更易于阅读。 
可以使用sexpr（）方法提取内部表示。 
它以s表达式（类似于Lisp）表示法显示Z3内部表示的数学公式和表达式。

```python
# 示例26
from z3 import *

if __name__ == "__main__":
    x, y = Reals('x y')
    solve(x + 10000000000000000000000 == y, y > 20000000000000000)
    # [y = 20000000000000001, x = -9999979999999999999999]

    print(Sqrt(2) + Sqrt(3))  # 2**(1/2) + 3**(1/2)
    print(simplify(Sqrt(2) + Sqrt(3)))  # 3.1462643699?
    print(simplify(Sqrt(2) + Sqrt(3)).sexpr())  # (root-obj (+ (^ x 4) (* (- 10) (^ x 2)) 1) 4)
    # The sexpr() method is available for any Z3 expression
    # sexpr（）方法可用于任何Z3表达式
    print((x + Sqrt(y) * 2).sexpr())  # (+ x (* (^ y (/ 1.0 2.0)) 2.0))

```

## 6、机器算术

- **位向量（bit vector）就是由一些二进制位组成的向量。**

现代CPU和主流编程语言对固定大小的**位向量使用算术运算。** 
Z3Py中的机器算法可作为位向量使用。 
它们实现了**无符号和带符号的两个补码算法的精确语义**。

下面的示例演示如何创建位向量变量和常量。 
**函数BitVec('x', 16)在Z3中创建一个名为x的具有16位的位向量变量。** 
为了方便起见，可以使用整数常量在Z3Py中创建位向量表达式。 
**函数BitVecVal（10，32）创建一个大小为32的位向量，其中包含值10。**

```python
# 示例27
from z3 import *

if __name__ == "__main__":
    x = BitVec('x', 16)
    y = BitVec('y', 16)
    print(x + 2)  # x + 2
    # Internal representation
    # 内部表示
    print((x + 2).sexpr())  # (bvadd x #x0002)

    # -1 is equal to 65535 for 16-bit integers
    # 对于16位整数，-1等于65535
    print(simplify(x + y - 1))  # 65535 + x + y

    # Creating bit-vector constants
    # 创建位向量常数
    a = BitVecVal(-1, 16)
    b = BitVecVal(65535, 16)
    print(simplify(a == b))  # True

    a = BitVecVal(-1, 32)
    b = BitVecVal(65535, 32)
    # -1 is not equal to 65535 for 32-bit integers
    # 对于32位整数，-1不等于65535
    print(simplify(a == b))  # False

```

与诸如C，C ++，C＃，Java之类的编程语言相比，有符号和无符号位向量之间没有区别。 
取而代之的是，Z3提供了特殊的算术运算符号版本，在该版本中，将位向量视为带符号的还是无符号的都有所不同。 
在Z3Py中，运算符<，<=，>，> =，/，％和>>对应于已签名的版本。 
相应的无符号运算符是ULT，ULE，UGT，UGE，UDiv，URem和LShR。

```python
# 示例28
from z3 import *

if __name__ == "__main__":
    # Create to bit-vectors of size 32
    x, y = BitVecs('x y', 32)

    solve(x + y == 2, x > 0, y > 0)  # [y = 1, x = 1]

    # Bit-wise operators
    # & bit-wise and
    # | bit-wise or
    # ~ bit-wise not
    solve(x & y == ~y)  # [x = 0, y = 4294967295]

    solve(x < 0)  # [x = 4294967295]

    # using unsigned version of <
    # 使用<
    solve(ULT(x, 0))  # no solution

```

运算符>>是算术右移，<<是左移。 逻辑右移是运算符LShR。

```python
# 示例29
from z3 import *

if __name__ == "__main__":
    # Create to bit-vectors of size 32
    x, y = BitVecs('x y', 32)

    solve(x >> 2 == 3)  # [x = 12]

    solve(x << 2 == 3)  # no solution

    solve(x << 2 == 24)  # [x = 6]

```

## 7、函数

与编程语言不同，在编程语言中，函数具有副作用，可能引发异常或永远不会返回，而Z3中的函数则没有副作用，并且是合计的。
即，它们在所有输入值上定义。这包括除法等功能。 
**Z3基于一阶逻辑。**

给定诸如x + y> 3的约束，我们一直在说x和y是变量。
在许多教科书中，x和y称为未解释的常量。
也就是说，它们允许任何与约束x + y> 3一致的解释。

更准确地说，**纯一阶逻辑中的功能和常数符号是未解释的或自由的，这意味着没有附加先验的解释。**
这与属于理论签名的函数相反，例如算术，其中函数+具有固定的标准解释（两个数字相加）。
未解释的函数和常量具有最大的灵活性；它们允许进行任何与函数或常量约束一致的解释。

为了说明未解释的函数和常量，让我们了解未解释的整数常量（又称变量）x，y。
最后，让f为一个未解释的函数，该函数接受一个类型（即排序）整数的参数，并得出一个整数值。
该示例说明了如何强制解释，**其中对x两次应用f会再次导致x，但是对x一次应用f与x不同。**

```python
# 示例30
from z3 import *

if __name__ == "__main__":
    x = Int('x')
    y = Int('y')
    f = Function('f', IntSort(), IntSort()) 
    solve(f(f(x)) == x, f(x) == y, x != y)  # [x = 0, y = 1, f = [1 -> 0, else -> 1]]

```

f的解（解释）应读为**f（0）为1，f（1）为0，而f（a）为1，**表示所有0和1都不相同。

在Z3中，我们还可以为**约束系统评估模型中的表达式**。 下面的示例演示如何使用评估方法。

```python
# 示例31
from z3 import *

if __name__ == "__main__":
    x = Int('x')
    y = Int('y')
    f = Function('f', IntSort(), IntSort())
    s = Solver()
    s.add(f(f(x)) == x, f(x) == y, x != y)
    print(s.check())  # sat
    m = s.model()
    print("f(f(x)) =", m.evaluate(f(f(x))))  # f(f(x)) = 0
    print("f(x)    =", m.evaluate(f(x)))  # f(x)    = 1
    print(m)  # [x = 0, y = 1, f = [1 -> 0, else -> 1]]

```

## 8、可满足性和有效性

如果F始终对其未解释的符号分配适当的值，则公式/约束F**有效**。
如果对公式/约束F的未解释符号进行了一些适当的赋值，则F满足true，则公式/约束F是**可满足的**。
**有效性在于寻找陈述的证明；可满足性是关于找到一组约束的解决方案。**
考虑包含a和b的公式F。我们可以问F是否有效，即对于a和b的值的任何组合，它是否始终为真。
如果F始终为true，则Not（F）始终为false，然后Not（F）将没有任何令人满意的分配（即解决方案）;
也就是说，Not（F）是不令人满意的。
也就是说，**当Not（F）不能满足（不满足）时，F正好有效。**
或者，当且仅当Not（F）无效（无效）时，F才可满足。以下示例证明了德摩根定律。

下面的示例重新定义了Z3Py函数，该函数证明接收公式作为参数。
此函数创建一个求解器，添加/声明公式的求反，并检查是否不能满足求反。
此功能的实现是Z3Py命令证明的较简单版本。

```python
# 示例32
from z3 import *

if __name__ == "__main__":
    p, q = Bools('p q')
    demorgan = And(p, q) == Not(Or(Not(p), Not(q)))
    print(demorgan)  # And(p, q) == Not(Or(Not(p), Not(q)))

    def prove(f):
        s = Solver()
        s.add(Not(f))
        if s.check() == unsat:
            print("proved")  # proved
        else:
            print("failed to prove")


    print("Proving demorgan...")
    prove(demorgan)

```

## 9、列表推导

Python支持列表推导。 
列表理解为创建列表提供了一种简洁的方法。
它们可用于在Z3Py中创建Z3表达式和问题。 
以下示例演示了如何在Z3Py中使用Python列表推导。

```python
# 示例33
from z3 import *

if __name__ == "__main__":
    # Create list [1, ..., 5]
    # 创建列表[1，...，5]
    print([x + 1 for x in range(5)])  # [1, 2, 3, 4, 5]

    # Create two lists containing 5 integer variables
    # 创建两个包含5个整数变量的列表
    X = [Int('x%s' % i) for i in range(5)]
    Y = [Int('y%s' % i) for i in range(5)]
    print(X)  # [x0, x1, x2, x3, x4]

    # Create a list containing X[i]+Y[i]
    # 创建一个包含X [i] + Y [i]的列表
    X_plus_Y = [X[i] + Y[i] for i in range(5)]
    print(X_plus_Y)  # [x0 + y0, x1 + y1, x2 + y2, x3 + y3, x4 + y4]

    # Create a list containing X[i] > Y[i]
    # 创建一个包含X [i]> Y [i]的列表
    X_gt_Y = [X[i] > Y[i] for i in range(5)]
    print(X_gt_Y)  # [x0 > y0, x1 > y1, x2 > y2, x3 > y3, x4 > y4]

    print(And(X_gt_Y))  # And(x0 > y0, x1 > y1, x2 > y2, x3 > y3, x4 > y4)

    # Create a 3x3 "matrix" (list of lists) of integer variables
    # 创建一个3x3的“矩阵”（列表列表）整数变量
    X = [[Int("x_%s_%s" % (i + 1, j + 1)) for j in range(3)]
         for i in range(3)]
    pp(X)

```

**在上面的示例中，表达式“ x％s”％i返回一个字符串，其中％s被替换为i的值。**

**pp命令**与print相似，但是它**使用Z3Py格式化程序来处理列表和元组，而不是Python的格式化程序。**

Z3Py还提供了用于创建**布尔，整数和实数变量的向量的函数**。 这些功能是使用列表推导来实现的。

```python
# 示例34
from z3 import *

if __name__ == "__main__":
    X = IntVector('x', 5)
    Y = RealVector('y', 5)
    P = BoolVector('p', 5)
    print(X)  # [x__0, x__1, x__2, x__3, x__4]
    print(Y)  # [y__0, y__1, y__2, y__3, y__4]
    print(P)  # [p__0, p__1, p__2, p__3, p__4]

    print([y ** 2 for y in Y])  # [y__0**2, y__1**2, y__2**2, y__3**2, y__4**2]
    print(Sum([y ** 2 for y in Y]))  # y__0**2 + y__1**2 + y__2**2 + y__3**2 + y__4**2

```

## 10、运动方程（Kinematic Equations）

在高中，学生学习运动方程。
这些方程式描述了位移（d），时间（t），加速度（a），初始速度（v_i）和最终速度（v_f）之间的数学关系。
用Z3Py表示法，我们可以将这些方程写为：

```
d == v_i * t + (a*t**2)/2,
v_f == v_i + a*t
```

### 1、问题1

Ima Hurryin正在接近一个以30.0 m / s的速度移动的信号灯。 
指示灯变黄，Ima踩下刹车并打滑。
如果Ima的加速度为-8.00 m/s^2，则在打滑过程中确定汽车的排量。

```python
# 示例35
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

```

### 2、问题2

本·鲁辛（Ben Rushin）正在红绿灯前等待。 
当它最终变为绿色时，Ben以6.00 m / s2的速度从静止加速了4.10秒。 
确定这段时间内本汽车的排量。

```python
# 示例36
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

```

## 11、位技巧

一些低级hack在C程序员中非常流行。 
我们在Z3实现中使用了其中一些技巧。

### 1、二次方

此hack经常在C程序（包括Z3）中使用，以测试机器整数是否为2的幂。 
我们可以使用Z3证明它确实有效。 
声称x！= 0 &&！（x＆（x-1））为真，且仅当x为2的幂时才成立。

```python
# 示例37
from z3 import *

if __name__ == "__main__":
    x = BitVec('x', 32)
    powers = [2 ** i for i in range(32)]
    fast = And(x != 0, x & (x - 1) == 0)
    slow = Or([x == p for p in powers])
    print(fast)  # And(x != 0, x & x - 1 == 0)
    prove(fast == slow)  # proved

    print("trying to prove buggy version...")
    fast = x & (x - 1) == 0
    prove(fast == slow)
    # counterexample
    # [x = 0]

```

### 2、相反的符号

以下简单技巧可用于测试两个机器整数是否具有相反的符号。

```python
# 示例38
from z3 import *

if __name__ == "__main__":
    x = BitVec('x', 32)
    y = BitVec('y', 32)
    # Claim: (x ^ y) < 0 iff x and y have opposite signs
    # 要求：（x ^ y）<0，如果x和y具有相反的符号
    trick = (x ^ y) < 0
    # Naive way to check if x and y have opposite signs
    # 检查x和y是否有相反符号的简单方法
    opposite = Or(And(x < 0, y >= 0), And(x >= 0, y < 0))

    prove(trick == opposite)  # proved

```

## 12、难题

### 1、狗，猫和老鼠

考虑以下难题。 
正好花了100美元，正好买了100只动物。 
狗的价格为15美元，猫的价格为1美元，小鼠的价格为25美分。 
您必须至少购买其中之一。 您应该购买多少个？

```python
# 示例39
from z3 import *

if __name__ == "__main__":
    # Create 3 integer variables
    dog, cat, mouse = Ints('dog cat mouse')
    s = Solver()
    s.add(dog >= 1)  # 至少一只狗
    s.add(cat >= 1)  # 至少一只猫
    s.add(mouse >= 1)  # 至少一只老鼠
    s.add(dog + cat + mouse == 100)  # 我们想买100只动物
    s.add(1500 * dog + 100 * cat + 25 * mouse == 10000)  # 我们有100美元（10000美分）
    # 狗的费用为15美元（1500美分）
    # 猫的售价为1美元（100美分）
    # 老鼠花了25美分
    print(s)
    print(s.check())
    print(s.model())  # [cat = 41, mouse = 56, dog = 3]

```

### 2、数独

数独是一个非常受欢迎的难题。 
目标是将数字插入框中仅满足一个条件：
每一行，每一列和3x3框必须只包含一次1到9的数字。

以下示例对Z3中的数独问题进行了编码。 
可以通过修改矩阵实例来解决不同的数独实例。 
此示例大量使用了Python编程语言中的列表推导。

```python
# 示例40
from z3 import *

if __name__ == "__main__":
    # 9x9 matrix of integer variables
    # 9x9整数变量矩阵
    X = [[Int("x_%s_%s" % (i + 1, j + 1)) for j in range(9)]
         for i in range(9)]

    # each cell contains a value in {1, ..., 9}
    # 每个单元格都包含{1，...，9}中的值
    cells_c = [And(1 <= X[i][j], X[i][j] <= 9) for i in range(9) for j in range(9)]

    # each row contains a digit at most once
    # 每行最多包含一个数字
    rows_c = [Distinct(X[i]) for i in range(9)]

    # each column contains a digit at most once
    # 每列最多包含一个数字
    cols_c = [Distinct([X[i][j] for i in range(9)]) for j in range(9)]

    # each 3x3 square contains a digit at most once
    # 每个3x3正方形最多包含一个数字
    sq_c = [Distinct([X[3 * i0 + i][3 * j0 + j]
                      for i in range(3) for j in range(3)])
            for i0 in range(3) for j0 in range(3)]

    sudoku_c = cells_c + rows_c + cols_c + sq_c

    # sudoku instance, we use '0' for empty cells
    # 数独实例，我们对空单元格使用“ 0”
    instance = ((0, 0, 0, 0, 9, 4, 0, 3, 0),
                (0, 0, 0, 5, 1, 0, 0, 0, 7),
                (0, 8, 9, 0, 0, 0, 0, 4, 0),
                (0, 0, 0, 0, 0, 0, 2, 0, 8),
                (0, 6, 0, 2, 0, 1, 0, 5, 0),
                (1, 0, 2, 0, 0, 0, 0, 0, 0),
                (0, 7, 0, 0, 0, 0, 5, 2, 0),
                (9, 0, 0, 0, 6, 5, 0, 0, 0),
                (0, 4, 0, 9, 7, 0, 0, 0, 0))

    instance_c = [If(instance[i][j] == 0, True, X[i][j] == instance[i][j])
                  for i in range(9) for j in range(9)]
    s = Solver()
    s.add(sudoku_c + instance_c)  
    if s.check() == sat:
        m = s.model()
        r = [[m.evaluate(X[i][j]) for j in range(9)]
             for i in range(9)]
        print_matrix(r)
    else:
        print("failed to solve")

```

### 3、八皇后

八皇后难题是将八个国际象棋皇后放在8x8棋盘上的问题，这样就不会有两个皇后互相攻击。 
因此，解决方案要求没有两个皇后共享相同的行，列或对角线。

```python
# 示例41
from z3 import *

if __name__ == "__main__":
    # We know each queen must be in a different row.
    # So, we represent each queen by a single integer: the column position
    # 我们知道每个女王都必须在不同的行中。
    # 因此，我们用一个整数表示每个皇后：列位置
    Q = [Int('Q_%i' % (i + 1)) for i in range(8)]

    # Each queen is in a column {1, ... 8 }
    # 每个女王都在{1，... 8}列中
    val_c = [And(1 <= Q[i], Q[i] <= 8) for i in range(8)]

    # At most one queen per column
    # 每列最多一位皇后
    col_c = [Distinct(Q)]

    # Diagonal constraint
    # 对角约束
    diag_c = [If(i == j, True, And(Q[i] - Q[j] != i - j, Q[i] - Q[j] != j - i))
              for i in range(8) for j in range(i)]

    solve(val_c + col_c + diag_c)

# [Q_5 = 1,
#  Q_8 = 7,
#  Q_3 = 8,
#  Q_2 = 2,
#  Q_6 = 3,
#  Q_4 = 6,
#  Q_7 = 5,
#  Q_1 = 4]

```

## 13、应用程序：安装问题

- 最佳软件包安装/卸载管理器：http://cseweb.ucsd.edu/~rjhala/papers/opium.pdf

安装问题包括确定是否可以在系统中安装一组新的软件包。 
此应用程序基于文章OPIUM：**最佳软件包安装/卸载管理器**。 
许多软件包都依赖于其他软件包来提供某些功能。 
每个发行版都包含一个元数据文件，该文件说明了该发行版每个程序包的要求。 
元数据包含详细信息，例如名称，版本等。
更重要的是，它包含depends和conflicts子句，这些子句规定了系统上还应该安装其他软件包。 
Depends子句规定必须存在哪些其他软件包。 冲突条款规定不得存在其他软件包。

使用Z3可以轻松解决安装问题。 这个想法是为每个包定义一个布尔变量。 
如果程序包必须在系统中，则此变量为true。
如果程序包a依赖于程序包b，c和z，我们将这样写：

```python
DependsOn(a, [b, c, z])

def DependsOn(pack, deps):
   return And([ Implies(pack, dep) for dep in deps ])
   
And(Implies(a, b), Implies(a, c), Implies(a, z))
```

DependsOn是一个简单的Python函数，它创建Z3约束来**捕获Depends子句的语义。**

因此，依赖项（a，[b，c，z]）生成约束。

**也就是说，如果用户安装了软件包a，那么他们还必须安装软件包b、c和z。**
如果包d与包e冲突，**我们就写Conflict（d，e）**。
Conflict也是一个简单的Python函数。

```python
def Conflict(p1, p2):
    return Or(Not(p1), Not(p2))
```

冲突（d，e）生成约束 `Or(Not(d), Not(e))`。
通过这两个函数，我们可以很容易地将Z3Py中的安装paper（第2节）中的示例编码为：

```python
# 示例42
from z3 import *

if __name__ == "__main__":
    def DependsOn(pack, deps):
        return And([Implies(pack, dep) for dep in deps])


    def Conflict(p1, p2):
        return Or(Not(p1), Not(p2))


    a, b, c, d, e, f, g, z = Bools('a b c d e f g z')

    solve(DependsOn(a, [b, c, z]),
          DependsOn(b, [d]),
          DependsOn(c, [Or(d, e), Or(f, g)]),
          Conflict(d, e),
          a, z)

# [f = True,
#  b = True,
#  a = True,
#  d = True,
#  g = False,
#  z = True,
#  c = True,
#  e = False]

```

**请注意，该示例包含约束**

```python
DependsOn(c, [Or(d, e), Or(f, g)]),
```

含义是：要安装c，必须安装d或e，以及f或g

现在，我们完善前面的示例。 
首先，我们修改DependsOn以允许我们编写DependsOn（b，d）而不是DependsOn（b，[d]）。 
我们还编写了一个函数install_check，该函数返回必须在系统中安装的软件包的列表。 
功能冲突也被修改。 
现在，它可以接收多个参数。

```python
# 示例43
from z3 import *

if __name__ == "__main__":
    def DependsOn(pack, deps):
        if is_expr(deps):
            return Implies(pack, deps)
        else:
            return And([Implies(pack, dep) for dep in deps])


    def Conflict(*packs):
        return Or([Not(pack) for pack in packs])


    def install_check(*problem):
        s = Solver()
        s.add(*problem)
        if s.check() == sat:
            m = s.model()
            r = []
            for x in m:
                if is_true(m[x]):
                    # x is a Z3 declaration
                    # x() returns the Z3 expression
                    # x.name() returns a string
                    r.append(x())
            print(r)
        else:
            print("invalid installation profile")


    a, b, c, d, e, f, g, z = Bools('a b c d e f g z')
    print("Check 1")
    # [f, b, a, d, z, c]
    install_check(DependsOn(a, [b, c, z]),DependsOn(b, d), 
                  DependsOn(c, [Or(d, e), Or(f, g)]),
                  Conflict(d, e),Conflict(d, g),
                  a, z)

    print("Check 2")
    # invalid installation profile
    install_check(DependsOn(a, [b, c, z]),DependsOn(b, d),
                  DependsOn(c, [Or(d, e), Or(f, g)]),
                  Conflict(d, e),Conflict(d, g),
                  a, z, g)

```

## 14、在本地使用Z3Py

Z3Py是Z3发行版的一部分。 
它位于python子目录中。 要在本地使用它，您必须在Python脚本中包含以下命令。

```python
from Z3 import *
```

**Z3 Python前端目录必须位于您的PYTHONPATH环境变量中。** 
Z3Py将自动搜索Z3库（z3.dll（Windows），libz3.so（Linux）或libz3.dylib（OSX））。
 您也可以使用以下命令手动初始化Z3Py：

```python
init("z3.dll")
```

