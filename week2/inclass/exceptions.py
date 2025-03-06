#!/usr/bin/env python
"""main program"""
import sys


def run(*args):
    x = int(input("x: "))
    y = int(input("y: "))
    try:
        result = x / y
    except ZeroDivisionError:
        print("Error: Cannot divide by 0")
        sys.exit(1)

    print(f"x: {x}\ny: {y}\nresult: {result}")


if __name__ == "__main__":
    run(*sys.argv[1:])
else:
    raise ImportError("Run this file directly, dont import it!")
