#!/bin/python3
import sys

with open(sys.argv[1], "r") as f:
    while True:
        print(f.readline(), end="")
        f.flush()