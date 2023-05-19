#!/bin/python3

with open("fp_ser_eng", "w") as pipe:
    print("Starting!")
    while True:
        pipe.write(input() + "\n")
        pipe.flush()