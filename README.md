# Project Description

This project focuses on simulating the precise physics of circular objects, ensuring accurate collision handling between circles and boundaries based on the laws of physics. Originally developed as a first-year project for the MIPT DREC informatics course, it aims to demonstrate realistic interactions between objects in a simulated environment.

# Structure Overview

The project comprises three main components:

- `dvizh_ok`: This is a C library designed for physics computations and includes Python demos. The demos showcase various simulations, such as 2D gas simulations. Users can refer to the "choosed_question.pdf" file for detailed information.

- Server: A simple UDP game server that supports Lua scripts for game development. These scripts enable users to create and delete objects, as well as process key inputs received from clients.

- Client: A straightforward Python pygame application responsible for visualizing the scenes provided by the server and transmitting key presses.

# Running the Project

## Requirements

To run the project, ensure you have the following prerequisites:

- Linux OS (compatibility with other platforms has not been verified)
- Python 3 with Pygame
- Make utility
- Lua programming language and the uv library

## Running Demos

To execute the physics demos:
1. Clone the repository.
2. Navigate to the project directory.
3. Enter the `dvizh_ok` directory.
4. Run the make command.
5. Execute the `physic_demo.py` script (you can use `physics_demo.py --help` for more info).

## Running the Game

To set up and run the game:
1. Modify the IP address in the `server/server.c` file to match your local IP address (Yes, that' stupid).
2. Run `make` in the root directory of the repository.
3. Execute the `start.sh` script.
4. Launch the clients using `player/player.py`.

## Creating your own multiplayer Games

Game scripts are structured around two main functions:
- `set_pos()`: Used for initial game setup.
- `translate()`: Translates key presses into commands for dvizh_ok. Refer to server/game.lua for a sample script.

### dvizh_ok Commands

Various commands are available to manipulate circles and boundaries within the simulation (check `dvizh_ok/main.c` source file for more info):
- Create and delete circles and boundaries.
- Modify collision types between circles and sections.
- Adjust properties like mass, size, position, and velocity of circles.
- Commands must be enclosed between begin and end to be processed by dvizh_ok.
- Additional commands like init and exit should be outside the begin scope.

# Authors

The project was contributed to by the following individuals:
- Matveev Vladislav: dvizh_ok library development and game script creation.
- Kirill Madorskii: Server implementation.
- Alisa Victorova: Client application development.
