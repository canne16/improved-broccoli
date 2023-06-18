#!/bin/sh

START=$(date +%s)

PRE=50
TIME=600
RENDER=--render

echo "" | tee res_lambda | tee wall_collision |  tee res_avg_v | tee res_prob_v | tee res_pressure

for N in $(seq 100 50 300)
do
    for V in $(seq 100 50 300)
    do
        ./app.py --screenshot --dump $RENDER --pre $PRE --time $TIME --number $N --velocity $V
    done
done

END=$(date +%s)
echo "Execution time: $(($END-$START))"