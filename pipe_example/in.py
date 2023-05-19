#!/bin/python3
import sys

with open(sys.argv[1], "w") as pipe:
    print("Starting!")
    while True:
        pipe.write(input() + "\n")
        pipe.flush()