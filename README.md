# About project

This project is about precise physic of circle objects simulation. By precise I mean processing all collisions of circles with each other and boundaries in right order using the laws of physics.
This was made as first year project for MIPT DREC informatics course.

# Structure

This project consists of three main parts: 
- dvizh_ok - c library for physics and python demos (including 2D gas simulation, check choosed_question.pdf file)
- server - simple udp game server, which supports lua scripts to make games (with scripts you can create and delete objects and process keys got from clients)
- client - simple python pygame app to draw scene got from server and send key presses 

# Running

## Requirements

- Linux (other platforms wasn't tested)
- Python3 and Pygame
- Make
- Lua and uv libraries

## Demos

To run physic demos you should clone repo, `cd` into it, `cd` into dvizh_ok direcotory, run `make` and then run `physic_demo.py`.

## Game

0. Check `server/server.c` file and change IP to your local ip address (Yes, that's stupid)
1. run `make` in the root of repo, then you
2. run `start.sh` script
3. run clients (`player/player.py`)

## Creating games

Game script consists of two main functions: `set_pos()` for initial game setup and `translate` for translating key presses to dvizh_ok commands (visit `server/game.lua` for example)

### dvizh_ok commands

There are a few commands to create, delete circles and boundaries and change their collision types (yes or no for any circle-circle and circle-section pair). You can also change circles' mass, size, position and velocity by setting value, adding value and limiting value (check `dvizh_ok/main.c` source file for more info)
All commands above should start with `begin` and after getting `end` dvizh_ok will render them for one step and return result
There are also `init` and `exit` commands which should be outside `begin` (This is planned to be changed in future)

# Authors
- Matveev Vladislav (dvizh_ok and game script)
- Kirill Madorsky (server)
- Alisa Victorova (client)
