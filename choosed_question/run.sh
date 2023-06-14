#!/bin/sh

START=$(date +%s)

PRE=50
TIME=600
RENDER=--render

for N in $(seq 100 50 300)
do
    for V in $(seq 100 50 300)
    do
        ./app.py --screenshot --dump $RENDER --pre $PRE --time $TIME --number $N --velocity $V
    done
done

END=$(date +%s)
echo "Execution time: $(($END-$START))"