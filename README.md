# Z3 API in Pythonz3-study

z3学习-推荐使用Python进行学习。

---

z3是由微软公司开发的一个优秀的**SMT求解器**（其实就是一个**定理证明器**），它能够检查逻辑表达式的可满足性。

```python
from z3 import *

if __name__ == '__main__':
    solver = Solver()  # 第1步：创建求解器
    x = Int('x')
    y = Int('y')
    solver.add(x > 2)
    solver.add(y < 10)
    solver.add(x + 2 * y == 7)  # 第2步：添加约束
    if solver.check() == sat:  # 第3步：判断解是否存在
        print(solver.model())  # 第4步：输出结果
    else:
        print("no sat")

```

## 学习资源

- [x] z3 github：https://github.com/Z3Prover/z3

- [ ] API文档（C、C++、.NET、Java、Python）：http://z3prover.github.io/api/html/index.html

  【Python】http://z3prover.github.io/api/html/namespacez3py.html

  【官方教程】Getting Started with Z3: A Guide：
  http://rise4fun.com/z3/tutorial/guide

  https://rise4fun.com/Z3/tutorialcontent/fixedpoints

  https://rise4fun.com/Z3/tutorial/strategies

- [x] 【Python】z3 API in Python：https://ericpony.github.io/z3py-tutorial/guide-examples.htm

  Z3py tutorial：https://github.com/ericpony/z3py-tutorial 103

  【翻译】Z3 API in PYTHON 中文文档 （官方文档翻译）：https://arabelatso.github.io/2018/06/14/Z3%20API%20in%20Python/
  【翻译】Z3 API in Python：https://nen9ma0.github.io/2018/03/14/z3py/
  
- [ ] SMT竞赛：https://smt-comp.github.io/2021/

  SAT竞赛：http://www.satcompetition.org/

- [ ] SMT-LIB：http://smtlib.cs.uiowa.edu/

- [ ] 二进制分析框架angr框架的内置Z3：https://github.com/angr/angr-z3

- [ ] Go Bindings to the Z3 Theorem Prover：https://github.com/mitchellh/go-z3

- [ ] Leonardo de Moura（Senior Principal Researcher）：https://www.microsoft.com/en-us/research/people/leonardo/publications/

## 其它求解器

- http://smtlib.cs.uiowa.edu/solvers.shtml

- Yices
- CVC3
- Simplify
- TSAT
- MathSAT
- Verifun
- Ario

## 相关关键概念/Keyword

- **SAT（Satisfiability）：指命题逻辑公式的可满足性问题。**

- **SMT（Satisfiability Modulo Theories）：**被翻译为“**可满足性模理论**”、“**多理论下的可满足性问题**”或者“**特定（背景）理论下的可满足性问题**”，其**判定算法被称为SMT求解器**。

  SMT算法分为2种：积极（eager）类算法/**惰性（lazy）类算法**（主流）。

- **CNF（conjunctive normal form）：**命题公式的**合取范式形式**。也就是形如A1^A2^...^An的公式，其中每一个Ai是一个子句。

- UF（uninterpreted function）：未解释函数。

- LRA（linear real arithmetic）：线性实数演算。

- LIA（linear integer arithmetic）：线性整数演算。

- NRA（non-linear real arithmetic）：非线性实数演算。

- NIA（non-linear integer arithmetic）：非线性整数演算。

- RDL（difference logic over the reals）：实数差分逻辑。

- IDL（difference logic over the integers）：整数差分逻辑。

- arrays：数组。

- **BV（bit vector）：位向量。**

- DPLL算法 （Davis-Putnam-Logemann-Loveland algorithm）。

- CDCL算法（conflict-driven clause learning SAT solver)：基于冲突检测的子句学习求解算法。

- DAG（directed acyclic graph）：有向无环图。

## 教程-视频

- [x] **Z3入门简介**：https://www.bilibili.com/s/video/BV1T7411C7tG

## 教程/文章/安装参考

- [x] win10：带你入逆向坑，怎样在win10上安装并使用Z3库：https://www.jianshu.com/p/5530c6bb4a39
- [x] z3-solver安装和使用方法：https://www.cnblogs.com/pcat/p/12592272.html
- [x] [python/工具] python z3库学习 减乘除位与运算 ctf一把梭：https://www.jianshu.com/p/64d87659673a
- [ ] Intro to Binary Analysis with Z3 and angr：https://github.com/FSecureLABS/z3_and_angr_binary_analysis_workshop
- [ ] z3-playground：https://github.com/0vercl0k/z3-playground 218

## 经典应用

- 约束求解
- 八皇后
- 数独
- 安装依赖、冲突问题
- CTF竞赛解题
- [x] 使用Z3 Solver求解逻辑题：https://www.7forz.com/3255/
- [ ] Z3简介及在逆向领域的应用：https://cloud.tencent.com/developer/article/1423409

## Paper

- [x] 【综述】金继伟,马菲菲,张健.**SMT求解技术简述**[J].计算机科学与探索,2015,9(07):769-780. 

  http://fcst.ceaj.org/CN/abstract/abstract956.shtml

- [x] 【综述】王翀,吕荫润,陈力,王秀利,王永吉.**SMT求解技术的发展及最新应用研究综述**[J].计算机研究与发展,2017,54(07):1405-1425. 

  https://crad.ict.ac.cn/CN/10.7544/issn1000-1239.2017.20160303

- [ ] **Programming Z3**：https://theory.stanford.edu/~nikolaj/programmingz3.html

- [ ] yinyang: a fuzzer for SMT solvers：https://github.com/testsmt/yinyang 84

- [ ] 【PLDI2020 CCF-A】Validating SMT solvers via semantic fusion：http://chengyuzhang.com/

- [ ] On the unusual effectiveness of type-aware operator mutations for testing SMT solvers

- [ ] 【ASE2019 CCF-A】Manticore: A User-Friendly Symbolic Execution Framework for Binaries and Smart Contracts：https://github.com/trailofbits/manticore



