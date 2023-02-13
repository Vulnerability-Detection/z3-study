# Python中的z3 api-Fixedpoints

- 源地址：https://ericpony.github.io/z3py-tutorial/fixpoint-examples.htm

本教程说明了Z3的定点引擎的用法。 
以下论文[μZ - An Efficient Engine for Fixed-Points with Constraints](http://research.microsoft.com/en-us/people/nbjorner/z3fix.pdf) （CAV 2011）和[Generalized Property Directed Reachability](http://research.microsoft.com/en-us/people/nbjorner/z3pdr.pdf)（SAT 2012）描述了引擎的一些主要功能。

请向nbjorner@microsoft.com发送反馈，评论和/或更正。

## 1、介绍

本教程介绍了Z3可用的一些定点实用程序。 
主要功能是基本的**Datalog引擎**，具有**关系代数的引擎**以及**基于属性定向可达性算法的泛化的引擎**。

## 2、Basic Datalog

**默认的定点引擎是自底向上的Datalog引擎。** 
它适用于**有限关系**，并且使用有限表表示形式作为哈希表作为表示有限关系的默认方式。

### 1、关系，规则和查询

**第一个示例说明了如何声明关系，规则以及如何提出查询。**

```python
# 示例55
from z3 import *

if __name__ == "__main__":
    fp = Fixedpoint()
    a, b, c = Bools('a b c')

    fp.register_relation(a.decl(), b.decl(), c.decl())  # 申明关系
    fp.rule(a, b)  # 定义规则
    fp.rule(b, c)
    fp.set(engine='datalog')  # 设置引擎

    print("current set of rules", )
    print(fp)
    # (declare - rel b ())
    # (declare - rel a ())
    # (declare - rel c ())
    # (rule(= > ( and b) a))
    # (rule(= > ( and c) b))

    # 查询规则
    print(fp.query(a))  # unsat

    fp.fact(c)
    print("updated set of rules", )
    print(fp)
    # (declare - rel b ())
    # (declare - rel a ())
    # (declare - rel c ())
    # (rule(= > b a))
    # (rule(= > c b))
    # (rule c)

    print(fp.query(a))  # sat
    print(fp.get_answer())  # True

```

该示例说明了一些基本构造。

```python
fp = Fixedpoint()
```

创建定点计算的上下文。

```python
fp.register_relation(a.decl(), b.decl(), c.decl())
```

将关系a，b，c注册为递归定义的。

```python
fp.rule(a,b)
```

**创建b遵循a的规则。** 
通常，您可以使用以下格式创建包含多个前提和名称的规则

```python
fp.rule(head,[body1,...,bodyN],name)
```

名称是可选的。 它用于跟踪推导证明中的规则。 
**继续该示例，除非建立了b，否则a为假。**

```python
fp.query(a)
```

询问是否可以派生a。 
到目前为止的规则说，**如果建立了b，则a遵循，同时如果建立c，则b遵循。** 
但是没有建立c的事物，也没有建立b的事物，因此不能导出a。

```python
fp.fact(c)
```

添加一个事实fp.rule(c,True)的简写。 现在是可以导出a的情况。

### 2、解释说明

也可能获得对派生查询的解释。 
对于有限的**Datalog引擎**，解释是一种跟踪，它提供有关如何得出事实的信息。 
解释是一个表达式，其功能符号是推导中使用的**Horn规则和事实**。

```python
# 示例56
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

```

### 3、与arguments的关系

**关系可以引起arguments。** 
我们使用图形中的边和路径来说明与arguments的关系。

```python
# 示例57
from z3 import *

if __name__ == "__main__":
    fp = Fixedpoint()
    fp.set(engine='datalog')

    s = BitVecSort(3)
    edge = Function('edge', s, s, BoolSort())
    path = Function('path', s, s, BoolSort())
    a = Const('a', s)
    b = Const('b', s)
    c = Const('c', s)

    fp.register_relation(path, edge)
    fp.declare_var(a, b, c)
    fp.rule(path(a, b), edge(a, b))
    fp.rule(path(a, c), [edge(a, b), path(b, c)])

    v1 = BitVecVal(1, s)
    v2 = BitVecVal(2, s)
    v3 = BitVecVal(3, s)
    v4 = BitVecVal(4, s)

    fp.fact(edge(v1, v2))
    fp.fact(edge(v1, v3))
    fp.fact(edge(v2, v4))

    print("current set of rules")
    print(fp)
    # (declare - rel path ((_ BitVec 3)(_ BitVec 3)))
    # (declare - rel edge ((_ BitVec 3)(_ BitVec 3)))
    # (declare - var A (_ BitVec 3))
    # (declare - var B (_ BitVec 3))
    # (declare - var C (_ BitVec 3))
    # (rule(= > ( and (edge C B)) (path C B)))
    # (rule(= > ( and (edge C B)(path B A)) (path C A)))
    # (rule(edge  # b001 #b010))
    # (rule(edge  # b001 #b011))
    # (rule(edge  # b010 #b100))
    print()

    print(fp.query(path(v1, v4)), "yes we can reach v4 from v1")  # sat yes we can reach v4 from v1
    print(fp.query(path(v3, v4)), "no we cannot reach v4 from v3")  # unsat no we cannot reach v4 from v3

```

该示例使用了声明

```python
fp.declare_var(a,b,c)
```

以指示定点引擎在规则中出现a，b，c时应将其视为变量。 
考虑一下约定，因为它们将绑定变量传递给Z3Py中的量词。

### 4、尖峰时刻

使用基本定点引擎的一个更有趣的示例是解决“高峰时间”难题。 |
**难题在于将一辆红色汽车移出僵局。** 
我们已经对配置进行了编码，并编译了一组规则，这些规则对给定配置的汽车的合法移动进行了编码。 
**可以通过更改传递给Car的构造函数的参数来测试其他配置。** 
我们已经编码了一个在线拼图中的配置，您可以手动解决它，也可以通过询问Z3来作弊。

```python
# 示例58
# todo 待理解
from z3 import *


class Car:
    def __init__(self, is_vertical, base_pos, length, start, color):
        self.is_vertical = is_vertical
        self.base = base_pos
        self.length = length
        self.start = start
        self.color = color

    def __eq__(self, other):
        return self.color == other.color

    def __ne__(self, other):
        return self.color != other.color


def num(i):
    return BitVecVal(i, bv3)


def bound(i):
    return Const(cars[i].color, bv3)


def mk_state(car_node, value):
    return state([(num(value) if (cars[i] == car_node) else bound(i))
                  for i in range(num_cars)])


def mk_transition(row, col, i0, j, car0):
    body = [mk_state(car0, i0)]
    for index in range(num_cars):
        car_node = cars[index]
    if car0 != car_node:
        if car_node.is_vertical and car_node.base == col:
            for i in range(dimension):
                if i <= row and row < i + car_node.length and i + car_node.length <= dimension:
                    body += [bound(index) != num(i)]
        if car_node.base == row and not car_node.is_vertical:
            for i in range(dimension):
                if i <= col and col < i + car_node.length and i + car_node.length <= dimension:
                    body += [bound(index) != num(i)]

    s = "%s %d->%d" % (car0.color, i0, j)
    fp.rule(mk_state(car0, j), body, s)


def move_down(i, car):
    free_row = i + car.length
    if free_row < dimension:
        mk_transition(free_row, car.base, i, i + 1, car)


def move_up(i, car):
    free_row = i - 1
    if 0 <= free_row and i + car.length <= dimension:
        mk_transition(free_row, car.base, i, i - 1, car)


def move_left(i, car):
    free_col = i - 1
    if 0 <= free_col and i + car.length <= dimension:
        mk_transition(car.base, free_col, i, i - 1, car)


def move_right(i, car):
    free_col = car.length + i
    if free_col < dimension:
        mk_transition(car.base, free_col, i, i + 1, car)


def get_instructions(ans):
    lastAnd = ans.arg(0).children()[-1]
    trace = lastAnd.children()[1]
    while trace.num_args() > 0:
         print(trace.decl())
    trace = trace.children()[-1]


if __name__ == "__main__":
    dimension = 6
    red_car = Car(False, 2, 2, 3, "red")
    cars = [
        Car(True, 0, 3, 0, 'yellow'),
        Car(False, 3, 3, 0, 'blue'),
        Car(False, 5, 2, 0, "brown"),
        Car(False, 0, 2, 1, "lgreen"),
        Car(True, 1, 2, 1, "light blue"),
        Car(True, 2, 2, 1, "pink"),
        Car(True, 2, 2, 4, "dark green"),
        red_car,
        Car(True, 3, 2, 3, "purple"),
        Car(False, 5, 2, 3, "light yellow"),
        Car(True, 4, 2, 0, "orange"),
        Car(False, 4, 2, 4, "black"),
        Car(True, 5, 3, 1, "light purple")
    ]
    num_cars = len(cars)
    print("car number is ", num_cars)
    B = BoolSort()
    bv3 = BitVecSort(3)
    state = Function('state', [bv3 for c in cars] + [B])
    fp = Fixedpoint()
    # 会报错=>"unknown parameter 'generate_explanations'
    # fp.set(generate_explanations=True)
    fp.declare_var([bound(i) for i in range(num_cars)])
    fp.register_relation(state)

    # Initial state:
    # 初始状态：
    fp.fact(state([num(cars[i].start) for i in range(num_cars)]))

    # Transitions:
    # 过渡：
    for car in cars:
        for i in range(dimension):
            if car.is_vertical:
                move_down(i, car)
                move_up(i, car)
            else:
                move_left(i, car)
                move_right(i, car)

    print(fp)

    goal = state([(num(4) if cars[i] == red_car else bound(i)) for i in range(num_cars)])
    fp.query(goal)

    get_instructions(fp.get_answer())

```

## 3、抽象领域

基础引擎使用**基于关系代数的表操作**。
表示对于底层引擎是不透明的。
关系代数运算为任意关系定义得很好。
**它们不依赖于关系是表示一组有限值还是一组无限值。**
**Z3包含两个用于无限域的内置表。**
**第一个是整数和实数的间隔。第二个是用于两个整数或实数之间的边界约束。**
绑定约束的形式为x或x。**当结合使用时，它们形成一个抽象域，称为五角大楼抽象域。**
Z3实现了抽象域的精简乘积，从而使间隔域和边界域之间可以共享约束。

**下面我们给出一个简单的示例，说明位置10处的循环。**
只要循环计数器不超过上限，循环就会递增。
使用边界域和区间域的组合，我们可以从循环中收集派生的不变量，并且我们还可以确定循环后的状态不超过边界。

```python
# 示例59
from z3 import *

# 执行出错
# todo
if __name__ == "__main__":
    I = IntSort()
    B = BoolSort()
    l0 = Function('l0', I, I, B)
    l1 = Function('l1', I, I, B)

    s = Fixedpoint()

    # 会报错=> "unknown parameter 'compile_with_widening'
    # 会报错=> "unknown parameter 'unbound_compressor'
    # s.set(engine='datalog', compile_with_widening=True, unbound_compressor=False)
    s.set(engine='datalog')
    s.set('datalog.compile_with_widening', True)

    s.register_relation(l0, l1)
    s.set_predicate_representation(l0, 'interval_relation', 'bound_relation')
    s.set_predicate_representation(l1, 'interval_relation', 'bound_relation')

    m, x, y = Ints('m x y')

    s.declare_var(m, x, y)
    s.rule(l0(0, m), 0 < m)
    s.rule(l0(x + 1, m), [l0(x, m), x < m])
    s.rule(l1(x, m), [l0(x, m), m <= x])

    print("At l0 we learn that x, y are non-negative:")
    print()
    print(s.query(l0(x, y)))
    print(s.get_answer())

    print("At l1 we learn that x <= y and both x and y are bigger than 0:")
    print(s.query(l1(x, y)))
    print(s.get_answer())

    print("The state where x < y is not reachable")
    print(s.query(And(l1(x, y), x < y)))

```

该示例使用选项，Z3将抽象解释扩展到循环边界上。

```python
set_option(dl_compile_with_widening=True)
```

## 4、属性导向可达性引擎

用于定点的不同底层引擎基于**属性定向可达性（PDR）的算法**。 
使用以下指令启用PDR引擎

```python
set_option(dl_engine=1)
```

Z3中的版本适用于**具有算术和布尔域的Horn子句。**
使用算术时，应启用Z3中使用的主要抽象引擎进行PDR中的算术。

```python
set_option(dl_pdr_use_farkas=True)
```

该引擎还可以使用代数数据类型和位向量与域一起使用，尽管目前还没有针对任何一种进行过调优。 
**PDR引擎针对软件符号模型检查中的应用程序。** 
该系统可以是无限状态。 
以下示例还旨在说明如何将软件模型检查问题（具有安全属性）**嵌入到Horn子句中并使用PDR解决。**

### 1、程序调用

McCarthy的91函数说明了一个过程，该过程递归调用两次。 
下面的Horn子句对递归函数进行编码：

```python
mc(x) = if x > 100 then x - 10 else mc(mc(x+11))
```

编码递归过程的一般方案是为每个过程创建一个谓词，并向该谓词添加一个附加的输出变量。 
可以将对主体内过程的嵌套调用编码为关系的结合。

```python
# 示例60 
from z3 import *

# 执行出错
# todo
if __name__ == "__main__":
    mc = Function('mc', IntSort(), IntSort(), BoolSort())
    n, m, p = Ints('n m p')

    fp = Fixedpoint()

    fp.declare_var(n, m)
    fp.register_relation(mc)

    fp.rule(mc(m, m - 10), m > 100)
    fp.rule(mc(m, n), [m <= 100, mc(m + 11, p), mc(p, n)])

    print(fp.query(And(mc(m, n), n < 90)))
    print(fp.get_answer())

    print(fp.query(And(mc(m, n), n < 91)))
    print(fp.get_answer())

    print(fp.query(And(mc(m, n), n < 92)))
    print(fp.get_answer())

```

前两个查询是无法满足的。 
PDR引擎产生了同样的不满足的证据。 
证明是每个递归谓词的归纳不变式。 
PDR引擎为查询引入了特殊的查询谓词。

### 2、Bakery

我们还可以证明反应系统的不变性。 
将**反应系统**编码为保护过渡系统非常方便。 
直接编码受保护的转换可能不像递归的Horn子句那样方便。 
但是从受保护的过渡系统到递归的Horn子句编写翻译器是相当容易的。 
在下一个示例中，我们将说明翻译器和Lamport的两个过程Bakery算法。

**产生相当冗长（绝不是最小）的归纳不变量作为答案。**

```python
# 示例61
# todo 待理解
from z3 import *


def flatten(l):
    return [s for t in l for s in t]


class TransitionSystem():
    def __init__(self, initial, transitions, vars1):
        self.fp = Fixedpoint()
        self.initial = initial
        self.transitions = transitions
        self.vars1 = vars1

    def declare_rels(self):
        B = BoolSort()
        var_sorts = [v.sort() for v in self.vars1]
        state_sorts = var_sorts
        self.state_vals = [v for v in self.vars1]
        self.state_sorts = state_sorts
        self.var_sorts = var_sorts
        self.state = Function('state', state_sorts + [B])
        self.step = Function('step', state_sorts + state_sorts + [B])
        self.fp.register_relation(self.state)
        self.fp.register_relation(self.step)

    # Set of reachable states are transitive closure of step.
    # 一组可到达状态是步骤的可传递关闭。
    def state0(self):
        idx = range(len(self.state_sorts))
        return self.state([Var(i, self.state_sorts[i]) for i in idx])

    def state1(self):
        n = len(self.state_sorts)
        return self.state([Var(i + n, self.state_sorts[i]) for i in range(n)])

    def rho(self):
        n = len(self.state_sorts)
        args1 = [Var(i, self.state_sorts[i]) for i in range(n)]
        args2 = [Var(i + n, self.state_sorts[i]) for i in range(n)]
        args = args1 + args2
        return self.step(args)

    def declare_reachability(self):
        self.fp.rule(self.state1(), [self.state0(), self.rho()])

    # Define transition relation
    # 定义过渡关系
    
    def abstract(self, e):
        n = len(self.state_sorts)
        sub = [(self.state_vals[i], Var(i, self.state_sorts[i])) for i in range(n)]
        return substitute(e, sub)

    def declare_transition(self, tr):
        len_s = len(self.state_sorts)
        effect = tr["effect"]
        vars1 = [Var(i, self.state_sorts[i]) for i in range(len_s)] + effect
        rho1 = self.abstract(self.step(vars1))
        guard = self.abstract(tr["guard"])
        self.fp.rule(rho1, guard)

    def declare_transitions(self):
        for t in self.transitions:
            self.declare_transition(t)

    def declare_initial(self):
        self.fp.rule(self.state0(), [self.abstract(self.initial)])

    def query(self, query):
        self.declare_rels()
        self.declare_initial()
        self.declare_reachability()
        self.declare_transitions()
        query = And(self.state0(), self.abstract(query))
        print(self.fp)
        print(query)
        print(self.fp.query(query))
        print(self.fp.get_answer())


if __name__ == "__main__":
    set_option(relevancy=0, verbose=1)
    # print self.fp.statistics()

    L = Datatype('L')
    L.declare('L0')
    L.declare('L1')
    L.declare('L2')
    L = L.create()
    L0 = L.L0
    L1 = L.L1
    L2 = L.L2

    y0 = Int('y0')
    y1 = Int('y1')
    l = Const('l', L)
    m = Const('m', L)

    t1 = {"guard": l == L0, "effect": [L1, y1 + 1, m, y1]}
    t2 = {"guard": And(l == L1, Or([y0 <= y1, y1 == 0])), "effect": [L2, y0, m, y1]}
    t3 = {"guard": l == L2, "effect": [L0, IntVal(0), m, y1]}

    s1 = {"guard": m == L0, "effect": [l, y0, L1, y0 + 1]}
    s2 = {"guard": And(m == L1, Or([y1 <= y0, y0 == 0])), "effect": [l, y0, L2, y1]}
    s3 = {"guard": m == L2, "effect": [l, y0, L0, IntVal(0)]}

    ptr = TransitionSystem(And(l == L0, y0 == 0, m == L0, y1 == 0), [t1, t2, t3, s1, s2, s3], [l, y0, m, y1])
    print("start=====")
    ptr.query(And([l == L2, m == L2]))
    print("end=====")

```

### 3、功能程序

-  [*Predicate Abstraction and CEGAR for Higher-Order Model Checking, Kobayashi et.al. PLDI 2011*](http://www.kb.is.s.u-tokyo.ac.jp/~uhiro/)

我们还可以使用Z3的广义PDR验证功能程序的某些属性。 

让我们在这里考虑来自Kobayashi等人的谓词抽象和CEGAR中用于高阶模型检查的示例。 PLDI2011。
我们通过采用适当的操作语义并对功能代码进行编码，以对要验证的程序专用的评估程序进行编码（我们不对通用评估程序进行编码，您应该对通用评估程序进行部分评估以帮助验证）。 
我们使用代数数据类型对正在评估的当前闭包进行编码。

```python
# 示例62
from z3 import *

# 执行出错
# todo
if __name__ == "__main__":
    # let max max2 x y z = max2 (max2 x y) z
    # let f x y = if x > y then x else y
    # assert (f (max f x y z) x) = (max f x y z)

    Expr = Datatype('Expr')
    Expr.declare('Max')
    Expr.declare('f')
    Expr.declare('I', ('i', IntSort()))
    Expr.declare('App', ('fn', Expr), ('arg', Expr))
    Expr = Expr.create()
    Max = Expr.Max
    I = Expr.I
    App = Expr.App
    f = Expr.f
    Eval = Function('Eval', Expr, Expr, Expr, BoolSort())

    x = Const('x', Expr)
    y = Const('y', Expr)
    z = Const('z', Expr)
    r1 = Const('r1', Expr)
    r2 = Const('r2', Expr)
    max = Const('max', Expr)
    xi = Const('xi', IntSort())
    yi = Const('yi', IntSort())

    fp = Fixedpoint()
    fp.register_relation(Eval)
    fp.declare_var(x, y, z, r1, r2, max, xi, yi)

    # Max max x y z = max (max x y) z
    fp.rule(Eval(App(App(App(Max, max), x), y), z, r2),
            [Eval(App(max, x), y, r1),
             Eval(App(max, r1), z, r2)])

    # f x y = x if x >= y
    # f x y = y if x < y
    fp.rule(Eval(App(f, I(xi)), I(yi), I(xi)), xi >= yi)
    fp.rule(Eval(App(f, I(xi)), I(yi), I(yi)), xi < yi)

    print(fp.query(And(Eval(App(App(App(Max, f), x), y), z, r1),
                       Eval(App(f, x), r1, r2),
                       r1 != r2)))

    print(fp.get_answer())

```

