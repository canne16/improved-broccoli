#!/usr/bin/python3
import json
import time
import random
import asyncio
import pygame


global proto


FLAG = False

##########################################################################
WIDTH = 1000  # ширина игрового окна
HEIGHT = 500 # высота игрового окна
FPS = 30 # частота кадров в секунду

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
pygame.display.set_caption("Game on")
clock = pygame.time.Clock()
Data = []
###########################################################################


ScrnClr = GREEN
        

class figure:  
    """Базовый класс для всех фигур"""  
    FigCount = 0

    def __init__(self, type, center, R, clr, mass, v):  
        self.type = 0
        self.center = [0,0]
        self.R = 100
        self.clr = BLUE
        self.mass = 1
        self.v = [0,0]
        figure.FigCount += 1  

    def draw(self, screen):

        if self.type == 0:
            pygame.draw.circle(screen, self.clr, centCO(self.center), self.R)


circ1 = [figure(0, [0,0], 100, WHITE, 1, [10,10]) for i in range(1)] # как не прописывать всю строку?



def centCO(XY):
    XY1 = [0]*2
    XY1[0] = XY[0] + WIDTH/2
    XY1[1] = XY[1] + HEIGHT/2
    return XY1



async def draw():

    screen.fill(ScrnClr)
    for i in range(len(circ1)):
        circ1[i].draw(screen)
    pygame.display.flip()


class Proto(asyncio.DatagramProtocol):
    def __init__(self):
        pass
    

    def connection_made(self, transport):
        self.transport = transport
        transport.sendto(f"initial".encode())

    def datagram_received(self, data, addr):
        S = str.split(';')

        for s in range(len(S)):
            f = S[s].split(",")
            for i in range(len(f) - 1):
                fig = list(map(float, f[i].split()))
                if s == 0:
                    while fig[0] + 2 > len(circ1):
                        circ1.append(figure(0, [0,0], 100, WHITE, 1, [10,10]))

                    circ1[fig[0]].R = fig[1]
                    circ1[fig[0]].mass = fig[2]
                    circ1[fig[0]].center = [fig[3],fig[4]]
                    circ1[fig[0]].v = [fig[5],fig[6]]
                """elif s == 1:
                    while fig[0] + 2 > len(circ1):
                        sect1.append(figure(0, [0,0], 100, WHITE, 1, [10,10]))

                    sect1[fig[0]].R = fig[1]
                    sect1[fig[0]].mass = fig[2]
                    sec1[fig[0]].center = [fig[3],fig[4]]
                    sect1[fig[0]].v = [fig[5],fig[6]]"""
                    


                
        """res_map[0]
        res_split = result.split()
        for i in range(len(res_split)):
            res_split[i] = float(res_split[i])
        circ1[0].center[0] = res_split[0]
        circ1[0].center[1] = -res_split[1]"""
        

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
    transport, proto = await loop.create_datagram_endpoint(Proto,remote_addr=('127.0.0.1', 8787))
    await initialize(transport,proto)
    FINISHED = False
  
    while not FINISHED:
        clock.tick(FPS)
        await draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                FINISHED = True
            if event.type == pygame.KEYDOWN:
                transport.sendto(f"+{chr(event.key)}".encode())
            if event.type == pygame.KEYUP:
                transport.sendto(f"-{chr(event.key)}".encode())

        await asyncio.sleep(0.015)
    transport.close()

    transport.close()
    pygame.quit()

asyncio.run(main())
