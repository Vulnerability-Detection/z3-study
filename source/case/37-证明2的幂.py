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
