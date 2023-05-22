#!/bin/python3
import sys

with open(sys.argv[1], "w") as f:
    while True:
        f.write(input() + "\n")
        f.flush()