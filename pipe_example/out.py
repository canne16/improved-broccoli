#!/bin/python3
import sys

with open(sys.argv[1], "r") as pipe:
    print("Starting!")
    while True:
        s = pipe.readline()
        if s == "":
            continue
        print(s, end="")