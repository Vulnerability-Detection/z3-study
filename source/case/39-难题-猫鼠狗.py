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
