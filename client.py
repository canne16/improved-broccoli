import json
import time
import random
import asyncio
import pygame



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
pygame.display.set_caption("шщшшщшщшщ")
clock = pygame.time.Clock()
###########################################################################

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
        

# начальные параметры: кружок со скоростью
# json


circ1 = [figure(0, [0,0], 100, WHITE, 1, [10,10]) for i in range(2)] # как не прописывать всю строку?


ScrnClr = GREEN
lTicks = 0
ticks = time.perf_counter()

###########################################################################
def centCO(XY):
    XY1 = [0]*2
    XY1[0] = XY[0] + WIDTH/2
    XY1[1] = XY[1] + HEIGHT/2
    return XY1

async def get_new():

    global FLAG
    global circ1
    
    
    print(" тут будет get_new и обработка доп параметров")
    #print(ticks)

    with open("testdata.json", "r") as fnew: 
        Dt = json.load(fnew)
        ScrnClr = WHITE
        print(len(Dt))
        for i in range(len(Dt)):
            #print(i)
            
            circ1[i].center = Dt[i]['center']
            circ1[i].clr = Dt[i]['clr']
            circ1[i].v = Dt[i]['v']
            circ1[i].v = [circ1[i].v[0]/FPS, circ1[i].v[1]/FPS]
        time.sleep(5)

        FLAG = True
    

async def get_changes():
    print(" тут будет get_new и обработка доп параметров")
        #print(ticks)

    global circ1

    with open("testdata.json", "r") as fnew: 
        Dt = json.load(fnew)
        ScrnClr = WHITE
        print(len(Dt))
        for i in range(len(Dt)):
            #print(i)
            circ1[i].center = Dt[i]['center']
            circ1[i].clr = Dt[i]['clr']
            circ1[i].v = Dt[i]['v']
            circ1[i].v = [circ1[i].v[0]/FPS, circ1[i].v[1]/FPS]



# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    
    ###############################

    # работа с сервером

    ticks = time.perf_counter()
    DeltaTicks = ticks - lTicks
    

    if 2 < DeltaTicks:
        lTicks = ticks
        print(" тут будет get_new и обработка доп параметров")
        #print(ticks)

        #get_new()

        FLAG = True

        with open("testdata.json", "r") as fnew: 
            Dt = json.load(fnew)
            ScrnClr = WHITE
            print(len(Dt))
            for i in range(len(Dt)):
                #print(i)
                circ1[i].center = Dt[i]['center']
                circ1[i].clr = Dt[i]['clr']
                circ1[i].v = Dt[i]['v']
                circ1[i].v = [circ1[i].v[0]/FPS, circ1[i].v[1]/FPS]
            
        fnew.close()

        
        


    else:   #посмотреть, как часто требуется обновлять
        print("get_changes()")
        #get_changes()

        #with open("data.json", "r") as fchanges: 
        #data = json.load(fchanges)
        #fchanges.close()

    
    ###############################
    # перевод полученного сообщения в переменные
    
    
    ###############################
    # отрисовка
    
    screen.fill(ScrnClr)
    
    for i in range(len(circ1)):
        circ1[i].draw(screen)
        circ1[i].center[0] += circ1[i].v[0]
        circ1[i].center[1] += circ1[i].v[1]
        print(circ1[i].center[0], circ1[i].v)
    pygame.display.flip()
    ###############################



pygame.quit()
