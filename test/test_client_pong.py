#!/bin/python3
import curses
import sys
import asyncio

stdscr = curses.initscr()
H, W = stdscr.getmaxyx()

ROCKET_WIDTH=10
ROCKET_A = 1
ROCKET_B = 10
BALL=[10, 20]
BALLVEL = [1, 2]

SIDE = 'R'
if len(sys.argv) == 1 or sys.argv[1][0] == 'l' or sys.argv[1][0] == 'L':
    SIDE = 'L'


FINISHED = False

class PongProto(asyncio.DatagramProtocol):
    def __init__(self):
        pass
    

    def connection_made(self, transport):
        self.transport = transport
        transport.sendto(f"DIM {H} {W}".encode())

    def datagram_received(self, data, addr):
        global ROCKET_A, ROCKET_B, BALL, BALLVEL, H, W, FINISHED
        result = data.decode()
        cmd = result.split()
        if cmd[0] == 'pos' and len(cmd) > 6:
            ROCKET_A, ROCKET_B = map(int, cmd[1:3])
            BALL = list(map(int, cmd[3:5]))
            BALLVEL = list(map(int, cmd[5:7]))
            stdscr.clear()
            #stdscr.addstr(10, 10, f"Cmd recieved {cmd}")
            draw_rocket_a()
            draw_rocket_b()
            draw_net()
            draw_ball()
            draw_score(cmd[7:9])
            #print(cmd[7:9], file=sys.stderr)
            stdscr.refresh()
        elif cmd[0] == 'dim' and len(cmd) > 2:
            stdscr.clear()
            H, W = map(int, cmd[1:3])

        elif cmd[0] == 'exit':
            FINISHED = True

def draw_rocket_a():
    for i in range(ROCKET_A, min(ROCKET_A+ROCKET_WIDTH, H)):
        stdscr.addch(i, 0, '#', curses.color_pair(1))

def draw_rocket_b():
    for i in range(ROCKET_B, min(ROCKET_B+ROCKET_WIDTH, H)):
        stdscr.addch(i, W-1, '#', curses.color_pair(1))

NUMBERS = [
["###", " # ", "###", "###", "# #", "###", "###", "###", "###", "###"],
["# #", "## ", "  #", "  #", "# #", "#  ", "#  ", "  #", "# #", "# #"],
["# #", " # ", "###", "###", "###", "###", "###", "  #", "###", "###"],
["# #", " # ", "#  ", "  #", "  #", "  #", "# #", "  #", "# #", "  #"],
["###", "###", "###", "###", "  #", "###", "###", "  #", "###", "###"]
]

def draw_net():
    for i in range(1, H):
        stdscr.addch(i, W//2, 'X', curses.color_pair(1))
        stdscr.refresh()

def draw_score(score):
    for i in range(5):
        stdscr.addstr(H//2-2 + i, W//4-4, NUMBERS[i][int(score[0]) // 10])
        stdscr.addstr(H//2-2 + i, W//4, NUMBERS[i][int(score[0]) % 10])
        stdscr.addstr(H//2-2 + i, W*3//4-4, NUMBERS[i][int(score[1]) // 10])
        stdscr.addstr(H//2-2 + i, W*3//4, NUMBERS[i][int(score[1]) % 10])

def draw_ball():
    stdscr.addch(BALL[0], BALL[1], 'O', curses.color_pair(2))

curses.noecho()
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLUE)
stdscr.nodelay(True)

async def step(transport, proto):
    global ROCKET_A, BALL, BALLVEL, SIDE

    key = stdscr.getch()

    if key == ord('a'):
        transport.sendto(f'INC{SIDE}'.encode())

    elif key == ord('q'):
        transport.sendto(f'DEC{SIDE}'.encode())
    elif key == ord('x'):
        transport.sendto('EXIT'.encode())
        return 0
    return 1

async def main():
    loop = asyncio.get_running_loop()
    transport, proto = await loop.create_datagram_endpoint(PongProto, remote_addr=('127.0.0.1', '9898'))

    while not FINISHED:
        if await step(transport, proto) == 0:
            break
        await asyncio.sleep(0.01)
    transport.close()

asyncio.run(main())
curses.nocbreak()
curses.endwin()
