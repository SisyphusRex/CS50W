#!/c/Users/twpod/AppData/Local/Microsoft/WindowsApps/python
"""main program"""
import sys


def run(*args):
    x = int(input("x: "))
    y = int(input("y: "))
    result = int(x / y)

    print(f"x: {x}\ny: {y}\nresult: {result}")


if __name__ == "__main__":
    run(*sys.argv[1:])
else:
    raise ImportError("Run this file directly, dont import it!")
