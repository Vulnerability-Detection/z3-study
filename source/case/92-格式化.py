from z3 import *

if __name__ == "__main__":
    x = Int('x')
    y = Int('y')
    print(x ** 2 + y ** 2 >= 1)  # x**2 + y**2 >= 1
    set_option(html_mode=False)
    print(x ** 2 + y ** 2 >= 1)  # x**2 + y**2 >= 1
