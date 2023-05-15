#!/bin/python3

with open("pipe", "r") as pipe:
    print("Starting!")
    while True:
        s = pipe.readline()
        if s == "":
            continue
        print(s, end="")