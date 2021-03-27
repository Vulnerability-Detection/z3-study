# Python中的z3 api-Strategies

- 源地址：https://ericpony.github.io/z3py-tutorial/strategies-examples.htm

诸如Z3之类的高性能求解器包含**许多算法证明方法的紧密集成**，手工制作的启发式组合。 
尽管这些启发式组合往往针对已知的问题类别进行了高度调整，但它们在新的问题类别上可能很容易表现很差。 **随着求解器开始引起科学和工程学各个领域的从业者的注意，这个问题变得越来越紧迫。** 
在许多情况下，更改求解器试探法可能会带来巨大的不同。

在本教程中，我们将展示如何使用Z3中可用的基本构建块来创建自定义策略。 
Z3Py和Z3 4.0实现了本文提出的思想。

请向leonardo@microsoft.com发送反馈，评论和/或更正。 您的评论非常有价值。

- http://research.microsoft.com/en-us/um/people/leonardo/strategy.pdf

## 1、介绍

Z3实现了一种用于编排推理引擎的方法，其中将“大”符号推理步骤表示为称为战术的功能，
**并且使用称为战术的组合器来组成战术。战术处理称为目标的公式集。**

将策略应用于**某个目标G**时，**可能会有四个不同的结果。**
该策略成功地表明G是可满足的（即可行的）；
成功表明G不满足要求（即不可行）;
产生一系列子目标；
或失败。
当将目标G减少为子目标G1，...，Gn的序列时，我们面临模型转换的问题。
**模型转换器使用一些子目标Gi的模型构造G的模型。**

在下面的示例中，我们创建一个目标g，该目标g由三个公式组成，一个策略t由两个内置策略组成：
**simple和solve-eqs。**
**简化策略将应用等效于命令simple的转换。**
**战术solver-eqs使用高斯消除法消除变量。**
实际上，solve-eqs不仅仅限于线性算术。它还可以消除任意变量。
然后，**组合器then将simplify应用于输入目标，并对由simplify产生的每个子目标求解等式。**
在此示例中，仅生成一个子目标。

```python
# 示例44
from z3 import *

if __name__ == "__main__":
    x, y = Reals('x y')
    g = Goal()
    g.add(x > 0, y > 0, x == y + 2)
    print(g)  # [x > 0, y > 0, x == y + 2]

    t1 = Tactic('simplify')
    t2 = Tactic('solve-eqs')
    t = Then(t1, t2)
    print(t(g))  # [[Not(y <= -2), Not(y <= 0)]]

```

**在上面的示例中，变量x被消除，并且不代表最终目标。**

在Z3中，我们说一个子句是形式为Or（f_1，...，f_n）的任何约束。 
战术拆分子句将在输入目标中选择子句Or（f_1，...，f_n），并将其拆分为n个子目标。 
每个子公式f_i一个。

```python
# 示例45
from z3 import *

if __name__ == "__main__":
    x, y = Reals('x y')
    g = Goal()
    g.add(Or(x < 0, x > 0), x == y + 1, y < 0)

    t = Tactic('split-clause')
    r = t(g)
    for g in r:
        print(g)

# [x < 0, x == y + 1, y < 0]
# [x > 0, x == y + 1, y < 0]

```

## 2、策略

Z3配备了许多内置策略。 命令describe_tactics()提供了所有内置策略的简短描述。

```python
describe_tactics()
```

Z3Py配备了以下战术组合器（又名战术）：

**Then(t, s)**：将t应用于输入目标，并将s应用于t产生的每个子目标。
**OrElse(t, s)**：首先将t应用于给定目标，如果失败，则返回s应用于给定目标的结果。
**Repeat(t)** ：继续应用给定的策略，直到没有子目标被修改。
**Repeat(t, n)**：继续应用给定的策略，直到没有子目标被修改，或者迭代次数大于n。
**TryFor(t, ms)**：将策略t应用于输入目标，如果它没有以ms millisenconds的形式返回，则它将失败。
**With(t, params)**：使用给定的参数应用给定的策略。

下面的示例演示如何使用这些组合器。

```python
# 示例46
from z3 import *

if __name__ == "__main__":
    x, y, z = Reals('x y z')
    g = Goal()
    g.add(Or(x == 0, x == 1),
          Or(y == 0, y == 1),
          Or(z == 0, z == 1),
          x + y + z > 2)
    # Split all clauses
    # 拆分所有子句
    split_all = Repeat(OrElse(Tactic('split-clause'), Tactic('skip')))
    print(split_all(g))
    # [[x == 0, y == 0, z == 0, x + y + z > 2],
    #  [x == 0, y == 0, z == 1, x + y + z > 2],
    #  [x == 0, y == 1, z == 0, x + y + z > 2],
    #  [x == 0, y == 1, z == 1, x + y + z > 2],
    #  [x == 1, y == 0, z == 0, x + y + z > 2],
    #  [x == 1, y == 0, z == 1, x + y + z > 2],
    #  [x == 1, y == 1, z == 0, x + y + z > 2],
    #  [x == 1, y == 1, z == 1, x + y + z > 2]]
    print()

    split_at_most_2 = Repeat(OrElse(Tactic('split-clause'), Tactic('skip')), 1)
    print(split_at_most_2(g))
    # [[x == 0, y == 0, Or(z == 0, z == 1), x + y + z > 2],
    #  [x == 0, y == 1, Or(z == 0, z == 1), x + y + z > 2],
    #  [x == 1, y == 0, Or(z == 0, z == 1), x + y + z > 2],
    #  [x == 1, y == 1, Or(z == 0, z == 1), x + y + z > 2]]
    print()

    # Split all clauses and solve equations
    # 拆分所有子句并求解方程式
    split_solve = Then(Repeat(OrElse(Tactic('split-clause'), Tactic('skip'))),Tactic('solve-eqs'))
    print(split_solve(g))  # [[]]

```

在策略split_solver中，策略solve-eqs释放了除一个目标以外的所有目标。 
请注意，此策略会产生一个目标：可以轻松满足（即可行）的空目标。

**可以使用Python for语句轻松遍历子目标列表。**

```python
# 示例47
from z3 import *

if __name__ == "__main__":
    x, y, z = Reals('x y z')
    g = Goal()
    g.add(Or(x == 0, x == 1),
          Or(y == 0, y == 1),
          Or(z == 0, z == 1),
          x + y + z > 2)

    # Split all clauses"
    split_all = Repeat(OrElse(Tactic('split-clause'),
                              Tactic('skip')))
    for s in split_all(g):
        print(s)

```

可以使用Solver()方法将战术转换为求解器对象。

如果该策略产生了空目标，则关联的求解器将返回sat。 

如果该策略产生包含False的单个目标，则求解器将返回unsat。 否则，返回未知。

```python
# 示例48
from z3 import *

if __name__ == "__main__":
    bv_solver = Then('simplify', 'solve-eqs', 'bit-blast', 'sat').solver()
    x, y = BitVecs('x y', 16)
    solve_using(bv_solver, x | y == 13, x > y)  # [y = 0, x = 13]

```

在上面的示例中，策略bv_solver使用方程式求解，位爆破和命题SAT求解器来实现基本的位向量求解器。 
注意，命令“战术”被禁止。 如果参数是字符串，则所有Z3Py组合器都会自动调用Tactic命令。 
最后，**命令solve_using是solve命令的变体，其中第一个参数指定要使用的求解器。**

在以下示例中，我们直接使用求解器API而不是命令resolve_using。 
我们使用**组合器With来配置我们的小解算器。** 我们还包括战术aig，它尝试使用“与逆图”压缩布尔公式。

```python
# 示例49
from z3 import *

if __name__ == "__main__":
    bv_solver = Then(With('simplify', mul2concat=True),
                     'solve-eqs',
                     'bit-blast',
                     'aig',
                     'sat').solver()
    x, y = BitVecs('x y', 16)
    bv_solver.add(x * 32 + y == 13, x & y < 10, y > -100)
    print(bv_solver.check())  # sat
    m = bv_solver.model()
    print(m)  # [y = 10509, x = 1720]
    print(x * 32 + y, "==", m.evaluate(x * 32 + y))  # x*32 + y == 13
    print(x & y, "==", m.evaluate(x & y))  # x & y == 8

```

**策略smt将主要求解器包装在Z3中作为策略。**

```python
# 示例50
from z3 import *

if __name__ == "__main__":
    x, y = Ints('x y')
    s = Tactic('smt').solver()
    s.add(x > y + 1)
    print(s.check())  # sat
    print(s.model())  # [y = -2, x = 0]

```

**现在，我们展示如何使用SAT实现整数算法的求解器。** 
仅对于每个变量都有上限和下限的问题，求解器才是完整的。

```python
# 示例51
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

```

策略可以与求解器结合使用。 
例如，我们可以将策略应用于目标，生成一组子目标，然后选择一个子目标并使用求解器对其进行求解。 
下一个示例演示了如何执行此操作，以及如何使用**模型转换器将子目标的模型转换为原始目标的模型。**

```python
# 示例52
from z3 import *

if __name__ == "__main__":
    t = Then('simplify','normalize-bounds','solve-eqs')
    x, y, z = Ints('x y z')
    g = Goal()
    g.add(x > 10, y == x + 3, z > y)

    r = t(g)
    # r contains only one subgoal
    # r仅包含一个子目标
    print(r)  # [[Not(k!0 <= -1), Not(z <= 14 + k!0)]]

    s = Solver()
    s.add(r[0])
    print(s.check())  # sat
    # Model for the subgoal
    # 子目标模型
    print(s.model())  # [z = 15]
    # Model for the original goal
    # 最初目标的模型
    # 会报错=> AttributeError: 'ApplyResult' object has no attribute 'convert_model'
    # print(r.convert_model(s.model()))

```

## 3、探针

探测（又称**公式测度**）是针对目标进行评估的。
可以使用关系运算符和布尔连接词来构建它们之上的布尔表达式。 
如果给定目标不满足条件cond，则战术FailIf（cond）失败。 
Z3Py中提供了许多数值和布尔量度。 
命令describe_probes（）提供所有内置探针的列表。

```python
describe_probes()
```

在下面的示例中，我们使用FailIf构建简单的策略。 
它还表明可以将探针直接应用于目标。

```python
# 示例53
from z3 import *

if __name__ == "__main__":
    x, y, z = Reals('x y z')
    g = Goal()
    g.add(x + y + z > 0)

    p = Probe('num-consts')
    print("num-consts:", p(g))  # num-consts: 3.0

    t = FailIf(p > 2)
    try:
        t(g)
    except Z3Exception:
        print("tactic failed")  # tactic failed

    print("trying again...")  # trying again...
    g = Goal()
    g.add(x + y > 0)
    print(t(g))  # [[x + y > 0]]

```

Z3Py还提供了组合器（战术） `If(p, t1, t2)`，它是以下各项的简写：

```python
OrElse(Then(FailIf(Not(p)), t1), t2)
```

组合器 `When(p, t)`是以下各项的简写：

```python
If(p, t, 'skip')
```

skip策略只是返回输入目标。 下面的示例演示如何使用If组合器。

```python
# 示例54
from z3 import *

if __name__ == "__main__":
    x, y, z = Reals('x y z')
    g = Goal()
    g.add(x ** 2 - y ** 2 >= 0)

    p = Probe('num-consts')
    t = If(p > 2, 'simplify', 'factor')
    print(t(g))  # [[(y + -1*x)*(y + x) <= 0]]

    g = Goal()
    g.add(x + x + y + z >= 0, x ** 2 - y ** 2 >= 0)
    print(t(g))  # [[2*x + y + z >= 0, x**2 + -1*y**2 >= 0]]

```

