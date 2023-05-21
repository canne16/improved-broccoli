#!/usr/bin/python3
import json
import time
import random
import asyncio
import pygame
import numpy as np


global proto

IP = '192.168.0.108'
PORT = 8787

FLAG = False

##########################################################################
WIDTH = 1920  # ширина игрового окна
HEIGHT = 1080 # высота игрового окна
FPS = 120 # частота кадров в секунду

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
##########################################################################

# создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game on!")
clock = pygame.time.Clock()
Data = []
KeyList = "wasdop"
###########################################################################


ScrnClr = WHITE

class figure:  
    """Базовый класс для всех фигур"""  
    FigCount = 0

    def __init__(self, type, center, R, clr, mass, v):  
        self.type = type
        self.center = center
        self.R = R
        self.clr = clr
        self.mass = mass
        self.vorx1y1 = v
        figure.FigCount += 1

    def draw(self, screen):

        if self.type == 0:
            pygame.draw.circle(screen, self.clr, centCO(self.center), self.R)

        if self.type == 1:
            pygame.draw.line(screen, self.clr, centCO(self.center), centCO(self.vorx1y1), 3)

circ1 = [] # как не прописывать всю строку?
sect1 = []



def centCO(XY):
    XY1 = [0]*2
    XY1[0] = XY[0] + WIDTH/2
    XY1[1] = XY[1] + HEIGHT/2
    return XY1



async def draw():
    screen.fill(ScrnClr)
    for circle in circ1:
        circle.draw(screen)
    for sect in sect1:
        sect.draw(screen)
    pygame.display.flip()


class Proto(asyncio.DatagramProtocol):
    def __init__(self):
        pass
    

    def connection_made(self, transport):
        self.transport = transport
        transport.sendto(f"initial".encode())

    def datagram_received(self, data, addr):
        result = data.decode()
        if result.startswith("CONF"):
            S = result.split(' ')
            global WIDTH
            WIDTH = int(S[1])
            global HEIGHT
            HEIGHT = int(S[2])
            global FPS
            FPS= int(S[3])
            pygame.display.set_mode((WIDTH, HEIGHT))
            return
        
        S = result.split(';')
        for s in range(len(S)):
            f = list(filter(None, S[s].split(",")))
            for i in range(len(f)):
                fig = list(map(float, f[i].split()))
                if s == 0:
                    if fig[0] >= len(circ1):
                        circ1.append(figure(0, [0,0], 100, list(np.random.choice(range(256), size=3)), 1, [10,10]))

                    circ1[int(fig[0])].R = fig[1]
                    circ1[int(fig[0])].mass = fig[2]
                    circ1[int(fig[0])].center = [fig[3],fig[4]]
                    circ1[int(fig[0])].vorx1y1 = [fig[5],fig[6]]
                elif s == 1:
                    if fig[0] >= len(sect1):
                        sect1.append(figure(1, [fig[1],fig[2]], 100, BLACK, 1, [fig[3],fig[4]]))

                    sect1[int(fig[0])].center = [fig[1],fig[2]]
                    sect1[int(fig[0])].vorx1y1 = [fig[3],fig[4]]
                    

async def initialize(transport, proto):
    transport
    return 1


async def step(transport, proto):
    transport.sendto(f"get_pos".encode())
    
    return 1

async def initialize(transport, proto):
    return 1

async def main():

    global pipe
    global FINISHED
    
    loop = asyncio.get_running_loop()
    transport, proto = await loop.create_datagram_endpoint(Proto,remote_addr=(IP, PORT))
    await initialize(transport,proto)
    FINISHED = False
  
    while not FINISHED:
        clock.tick(FPS)
        await draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("QUIT")
                transport.sendto(f"quit".encode())
                FINISHED = True
            if event.type == pygame.KEYDOWN:
                try:
                    if chr(event.key) in KeyList:
                        transport.sendto(f"+{chr(event.key)}".encode())
                        print(f"+{chr(event.key)}")

                except:
                    ValueError
            if event.type == pygame.KEYUP:
                try:
                    if chr(event.key) in KeyList:    
                        transport.sendto(f"-{chr(event.key)}".encode())
                except:
                    ValueError
        await asyncio.sleep(0.015)
    transport.close()

    transport.close()
    pygame.quit()

asyncio.run(main())
