#!/usr/bin/sh
make clean
make

python3 -m venv venv
venv/bin/python3 -m pip install pygame
chmod +x physic_test.py