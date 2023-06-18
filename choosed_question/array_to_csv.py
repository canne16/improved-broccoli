#!/bin/python3
vmax = 2000
name = input()
a = list(map(int, input().replace("[", "").replace("]", "").split(", ")[:-1]))

with open(f"csv/{name}.csv", "w") as f:
    for i in range(len(a)):
        f.write(f"{vmax / len(a) * i}, {a[i]};\n")