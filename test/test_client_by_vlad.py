#!venv/bin/python3
import sys
import asyncio
import pygame
import pygame.freetype
import random
import json 
from collections import deque

FINISHED = False
get_queue = deque()

WIDTH = 1000  # ширина игрового окна
HEIGHT = 500 # высота игрового окна
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
GAME_FONT = pygame.freetype.Font("AGENCYB.TTF", 24)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

R = 100
v = [10, 10]
V = [v[0]/FPS, v[1]/FPS]
xy = [0, 0]

###########################################################################
def centCO(XY):
    XY1 = [0]*2
    XY1[0] = XY[0] + WIDTH/2
    XY1[1] = XY[1] + HEIGHT/2
    return XY1

class PongProto(asyncio.DatagramProtocol):
    def __init__(self):
        pass
    
    def connection_made(self, transport):
        self.transport = transport
        transport.sendto(b"initial")

    def datagram_received(self, data, addr):
        result = data.decode()
        print(result)
        get_queue.append(result)
        

async def step(transport, proto):
    global FINISHED

    transport.sendto(b"get_pos")

    for event in pygame.event.get():        
        if event.type == pygame.QUIT:
            FINISHED = True
    
    screen.fill(WHITE)
    if len(get_queue) > 1:
        get_queue.popleft()
    if len(get_queue) >= 1:
        text_surface, rect = GAME_FONT.render(get_queue[0], (0, 0, 0))
        screen.blit(text_surface, (40, 250))
    
    pygame.draw.circle(screen, RED, centCO(xy), R)
    xy[0] += V[0] ### * V[0] * delta_t?
    xy[1] += V[1]
    #print(xy[0], V[0], xy[1], V[1], centCO(xy))
    pygame.display.flip()
    return 1


async def main():
    global FPS
    global FINISHED
    loop = asyncio.get_running_loop()
    transport, proto = await loop.create_datagram_endpoint(PongProto, remote_addr=('127.0.0.1', '9898'))

    while not FINISHED:
        if await step(transport, proto) == 0:
            break
        await asyncio.sleep(1/FPS)
    transport.close()
    #pygame.quit()

asyncio.run(main())