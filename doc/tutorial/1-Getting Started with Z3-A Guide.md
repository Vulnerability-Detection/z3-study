# Z3入门：指南

- 原地址：https://rise4fun.com/Z3/tutorial/guide
- 实验可以直接在原地址网页执行。

## 1、介绍

**Z3是Microsoft Research提供的最先进的定理证明器。**它可用于检查一种或多种理论上逻辑公式的可满足性。 

Z3为软件分析和验证工具提供了引人注目的匹配项，因为几种常见的软件结构直接映射到受支持的理论中。

本教程的主要目的是向读者介绍**如何有效使用Z3进行逻辑建模和求解。**

本教程提供了一些有关**逻辑建模**的一般背景知识，但是我们必须将**一阶逻辑**和**决策过程**的完整介绍推迟到教科书上。

Z3是低级工具。在需要解决逻辑公式的其他工具的上下文中，它最好用作组件。

因此，Z3公开了许多API工具，以方便工具映射到Z3，但是没有独立的编辑器或以用户为中心的工具来与Z3进行交互。

与语言方便相比，前端使用的语言语法更倾向于简单。

## 2、基本命令

- http://www.smtlib.org/

Z3输入格式是SMT-LIB 2.0标准定义的格式的扩展。 

**Z3脚本是一系列命令。** 

help命令显示所有可用命令的列表。 命令回显将显示一条消息。 

在内部，Z3维护了一堆用户提供的公式和声明。 我们说这些是用户提供的断言。 

#### 代码1

**命令define-const声明给定类型（也称为sort）的常量。** 

**命令clarify-fun声明一个函数。** 

在下面的示例中，我们声明了一个函数，该函数接收一个整数和一个布尔值，并返回一个整数。

- 输入

```bash
(echo "starting Z3...")
(declare-const a Int)
(declare-fun f (Int Bool) Int)
```

- 输出

```bash
starting Z3...
```

#### 代码2

命令assert会在Z3内部堆栈中添加一个公式。 

我们说，如果有一种解释（对于用户声明的常量和函数）可以使所有断言的公式为真，则Z3堆栈中的公式集是可以满足的。

- 输入

```bash
(declare-const a Int)
(declare-fun f (Int Bool) Int)
(assert (> a 10))
(assert (< (f a true) 100))
(check-sat)
```

- 输出

```
sat
```

**第一个断言的公式指出常数a必须大于10。**

**第二个断言的公式指出，应用于a和true的函数f必须返回小于100的值。**

命令check-sat确定Z3堆栈上的当前公式是否 是否令人满意。 

**如果公式可满足，则Z3返回sat。**

 如果它们不能满足要求（即它们不能满足要求），则**Z3返回不满足要求。**

当Z3无法确定公式是否可满足时，**Z3可能还会返回unknown。**

#### 代码3

当命令check-sat返回sat时，可以使用命令**get-model**检索使Z3内部堆栈上的所有公式为true的解释。

- 输入

```bash
(declare-const a Int)
(declare-fun f (Int Bool) Int)
(assert (> a 10))
(assert (< (f a true) 100))
(check-sat)
(get-model)
```

- 输出

```bash
sat
(model 
  (define-fun a () Int
    11)
  (define-fun f ((x!1 Int) (x!2 Bool)) Int
    (ite (and (= x!1 11) (= x!2 true)) 0
      0))
)
```

使用定义提供解释。 例如，定义：

```bash
(define-fun a () Int [val])
```

指出模型中a的值为[val]。 定义：

```bash
(define-fun f ((x!1 Int) (x!2 Bool)) Int
   ...
)
```

与编程语言中使用的函数定义非常相似。 

在此示例中，x1和x2是Z3创建的函数解释的参数。 

对于此简单示例，f的定义基于ite的（aka if-then-elses或条件表达式）。 例如，表达式：

```bash
(ite (and (= x!1 11) (= x!2 false)) 21 0)
```

当x！1等于11且x！2等于false时，计算（返回）21。 否则，它返回0。

### 使用范围

在某些应用程序中，我们希望探索共享相似定义和断言的相似问题。 

我们可以使用命令push和pop做到这一点。 **Z3维护声明和断言的全局堆栈。**

命令push通过保存当前堆栈大小来创建新作用域。 

pop命令删除在它与匹配的push之间执行的所有断言或声明。 

**check-sat和get-assertions**命令始终对全局堆栈的内容进行操作。

在以下示例中，命令（assert p）签名错误，因为pop命令删除了p的声明。 

如果删除了最后一个弹出命令，则错误将得到纠正。

#### 代码4

- 输入

```
(declare-const x Int)
(declare-const y Int)
(declare-const z Int)
(push)
(assert (= (+ x y) 10))
(assert (= (+ x (* 2 y)) 20))
(check-sat)

(pop) ; remove the two assertions
(push) 
(assert (= (+ (* 3 x) y) 10))
(assert (= (+ (* 2 x) (* 2 y)) 21))
(check-sat)

(declare-const p Bool)
(pop)
(assert p) ; error, since declaration of p was removed from the stack
```

- 输出

```bash
sat
unsat
Z3(15, 8): ERROR: unknown constant p
```

push和pop命令可以选择接收SMT 2语言指定的数字参数。

### 配置

**命令set-option用于配置Z3。 Z3有几个选项可以控制其行为。**

其中一些选项（例如：produce-proofs）**只能在任何声明或断言之前设置。** 

我们使用**reset命令清除所有的断言和声明**。

使用reset命令后，可以设置所有配置选项。

#### 代码5

- 输入

```bash
(set-option :print-success true) 
(set-option :produce-unsat-cores true) ; enable generation of unsat cores
(set-option :produce-models true) ; enable model generation
(set-option :produce-proofs true) ; enable proof generation
(declare-const x Int)
(set-option :produce-proofs false) ; error, cannot change this option after a declaration or assertion
(echo "before reset")
(reset)
(set-option :produce-proofs false) ; ok
```

- 输出

```bash
success
success
success
success
success
Z3(6, 28): ERROR: error setting ':produce-proofs', option value cannot be modified after initialization
before reset
success
success
```

当另一个应用程序使用管道控制Z3时，**：print-success true**选项特别有用。 

在这种模式下，原本不会打印任何输出的命令将成功打印。

### 附加命令

命令（**display t**）仅将Z3代码美化器应用于给定表达式。 

命令（**simplify t**）显示与t等效的可能更简单的表达式。 

该命令接受许多不同的选项，（帮助简化）将显示所有可用选项。

#### 代码6

- 输入

```bash
(declare-const a (Array Int Int))
(declare-const x Int)
(declare-const y Int)
(display (+ x 2 x 1))
(simplify (+ x 2 x 1))
(simplify (* (+ x y) (+ x y)))
(simplify (* (+ x y) (+ x y)) :som true) ; put all expressions in sum-of-monomials form.
(simplify (= x (+ y 2)) :arith-lhs true)
(simplify (= (store (store a 1 2) 4 3)
             (store (store a 4 3) 1 2)))
(simplify (= (store (store a 1 2) 4 3)
             (store (store a 4 3) 1 2))
          :sort-store true)
;(help simplify)
```

- 输出

```bash
(+ x 2 x 1)
(+ 3 (* 2 x))
(* (+ x y) (+ x y))
(+ (* x x) (* 2 x y) (* y y))
(= (+ x (* (- 1) y)) 2)
(= (store (store a 1 2) 4 3) (store (store a 4 3) 1 2))
true
```

**define-sort**命令定义一个新的排序符号，它是排序表达式的缩写。 

可以对新的排序符号进行参数化，在这种情况下，在命令中指定参数的名称，并且排序表达式使用排序参数。

命令的形式是这样的：

```bash
(define-sort [symbol] ([symbol]+) [sort])
```

以下示例为排序表达式定义了几种缩写。

#### 代码7

- 输入

```bash
(define-sort Set (T) (Array T Bool))
(define-sort IList () (List Int))
(define-sort List-Set (T) (Array (List T) Bool))
(define-sort I () Int)

(declare-const s1 (Set I))
(declare-const s2 (List-Set Int))
(declare-const a I)
(declare-const l IList)

(assert (= (select s1 a) true))
(assert (= (select s2 l) false))
(check-sat)
(get-model)
```

- 输出

```bashsat
sat
(model 
  (define-fun s2 () (Array (List Int) Bool)
    (_ as-array k!1))
  (define-fun a () Int
    0)
  (define-fun l () (List Int)
    nil)
  (define-fun s1 () (Array Int Bool)
    (_ as-array k!0))
  (define-fun k!0 ((x!1 Int)) Bool
    (ite (= x!1 0) true
      true))
  (define-fun k!1 ((x!1 (List Int))) Bool
    (ite (= x!1 nil) false
      false))
)
```

## 3、命题逻辑(Propositional Logic)

预定义的排序布尔是所有布尔命题表达式的排序（类型）。 

Z3支持通常的布尔运算符， `and`, `or`, `xor`, `not`, `=>` (implication), `ite` (if-then-else)。 

双含义使用等式=表示。 

以下示例说明如何证明如果p包含q和q包含r，则p包含r。 

我们通过表明否定是不令人满意的来实现的。 

**命令define-fun用于定义宏（又名别名）。** 

在此示例中，猜想是我们要证明的猜想的别名。

#### 代码1

- 输入

```bash
(declare-const p Bool)
(declare-const q Bool)
(declare-const r Bool)
(define-fun conjecture () Bool
	(=> (and (=> p q) (=> q r))
		(=> p r)))
(assert (not conjecture))
(check-sat)
```

- 输出

```bash
unsat
```

