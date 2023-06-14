#!/bin/sh

PRE=50
TIME=600
RENDER=--render

for N in $(seq 100 100 400)
do
    for V in $(seq 100 100 400)
    do
        ./app.py --screenshot --dump $RENDER --pre $PRE --time $TIME --number $N --velocity $V
    done
done