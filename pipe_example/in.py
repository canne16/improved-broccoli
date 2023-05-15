#!/bin/python3

with open("pipe", "w") as pipe:
    print("Starting!")
    while True:
        pipe.write(input() + "\n")
        pipe.flush()