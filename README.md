# z3-study

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

  【官方文档】Getting Started with Z3: A Guide：http://rise4fun.com/z3/tutorial/guide

  https://rise4fun.com/Z3/tutorialcontent/fixedpoints
  https://rise4fun.com/Z3/tutorial/strategies
- [x] 【Python】z3 API in Python：https://ericpony.github.io/z3py-tutorial/guide-examples.htm

  Z3py tutorial：https://github.com/ericpony/z3py-tutorial 103

  Z3 API in PYTHON 中文文档 （官方文档翻译）：https://arabelatso.github.io/2018/06/14/Z3%20API%20in%20Python/
- [ ] SMT *Competition*：https://smt-comp.github.io/2021/
- [ ] SMT-LIB：http://smtlib.cs.uiowa.edu/
- [ ] 二进制分析框架angr框架的内置Z3：https://github.com/angr/angr-z3
- [ ] Go Bindings to the Z3 Theorem Prover：https://github.com/mitchellh/go-z3
- [ ] Leonardo de Moura（Senior Principal Researcher）：https://www.microsoft.com/en-us/research/people/leonardo/publications/

## 教程-视频

- [x] **Z3入门简介**：https://www.bilibili.com/s/video/BV1T7411C7tG

## 教程/文章/安装参考

- [x] win10：带你入逆向坑，怎样在win10上安装并使用Z3库：https://www.jianshu.com/p/5530c6bb4a39
- [x] z3-solver安装和使用方法：https://www.cnblogs.com/pcat/p/12592272.html
- [x] [python/工具] python z3库学习 减乘除位与运算 ctf一把梭：https://www.jianshu.com/p/64d87659673a
- [ ] Intro to Binary Analysis with Z3 and angr：https://github.com/FSecureLABS/z3_and_angr_binary_analysis_workshop
- [ ] z3-playground：https://github.com/0vercl0k/z3-playground 218

## 经典应用

- 解方程
- 八皇后
- 数独
- 安装依赖、冲突问题
- [x] 使用Z3 Solver求解逻辑题：https://www.7forz.com/3255/

## Paper

- [ ] 金继伟,马菲菲,张健.SMT求解技术简述[J].计算机科学与探索,2015,9(07):769-780.
- [ ] **Programming Z3**：https://theory.stanford.edu/~nikolaj/programmingz3.html
- [ ] yinyang: a fuzzer for SMT solvers：https://github.com/testsmt/yinyang 84
- [ ] 【PLDI2020 CCF-A】Validating SMT solvers via semantic fusion：http://chengyuzhang.com/
- [ ] On the unusual effectiveness of type-aware operator mutations for testing SMT solvers

- [ ] 【ASE2019 CCF-A】Manticore: A User-Friendly Symbolic Execution Framework for Binaries and Smart Contracts：https://github.com/trailofbits/manticore



