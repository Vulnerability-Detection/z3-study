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
