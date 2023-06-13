#!/bin/sh

PRE=10
TIME=60
#./app.py --screenshot --pre $PRE --time $TIME --velocity 100 &
#./app.py --screenshot --pre $PRE --time $TIME --velocity 150 &
#./app.py --screenshot --pre $PRE --time $TIME --velocity 200 &
#./app.py --screenshot --pre $PRE --time $TIME --velocity 250 &
#./app.py --screenshot --pre $PRE --time $TIME --velocity 300 &
#./app.py --screenshot --pre $PRE --time $TIME --velocity 350 &
#./app.py --screenshot --pre $PRE --time $TIME --velocity 400 &
#./app.py --screenshot --pre $PRE --time $TIME --velocity 450
./app.py --screenshot --pre $PRE --time $TIME --velocity 100
./app.py --screenshot --pre $PRE --time $TIME --velocity 200
./app.py --screenshot --pre $PRE --time $TIME --velocity 300
./app.py --screenshot --pre $PRE --time $TIME --velocity 400

TIME=600
./app.py --screenshot --pre $PRE --time $TIME --velocity 100
./app.py --screenshot --pre $PRE --time $TIME --velocity 200
./app.py --screenshot --pre $PRE --time $TIME --velocity 300
./app.py --screenshot --pre $PRE --time $TIME --velocity 400
