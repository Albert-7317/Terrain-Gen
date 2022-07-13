import pygame, sys, random, math, time, numpy
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2

##setup for tiles and cells
TILESIZE = 20

##additoinal terrain features
TREESIZEx = 6
TREESIZEy = 16

ROCKSIZE = 10
VEGSIZE = 15

WIDTH = 1200
HEIGHT = 800
FPS = 12
FramesPerSecond = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Evolution game')

class Land(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        super().__init__()
        self.surf = pygame.Surface((TILESIZE, TILESIZE))
        self.surf.fill((57, 58, 16))
        self.rect = self.surf.get_rect(center=(posx, posy))
    
    def update(self):
        pass
        
class Water(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        super().__init__()
        self.surf = pygame.Surface((TILESIZE, TILESIZE))
        self.surf.fill((74, 109, 124))
        self.rect = self.surf.get_rect(center=(posx, posy))

    def update(self):
        pass #check = pygame.sprite.spritecollide(self, checks, True)

class Check(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        super().__init__()
        self.surf = pygame.Surface((TILESIZE, TILESIZE))
        self.surf.fill((244, 51, 171))
        self.rect = self.surf.get_rect(center=(posx, posy))

        self.health = 100

    def update(self):
        land = pygame.sprite.spritecollide(self, all_land, False)
        if land:
            self.kill()
            return True
        else:
            self.kill()
            return False

class Tree(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        super().__init__()
        self.surf = pygame.Surface((TREESIZEx, TREESIZEy))
        self.surf.fill((236, 154, 41))
        self.rect = self.surf.get_rect(center=(posx, posy))

    def update(self):
        pass

class Stone(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        super().__init__()
        self.surf = pygame.Surface((ROCKSIZE, ROCKSIZE))
        self.surf.fill((234, 239, 211))
        self.rect = self.surf.get_rect(center=(posx, posy))

    def update(self):
        pass

class Vegitation(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        super().__init__()
        self.surf = pygame.Surface((VEGSIZE, VEGSIZE))
        self.surf.fill((190, 213, 88))
        self.rect = self.surf.get_rect(center=(posx, posy))

    def update(self):
        pass

class Air(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        super().__init__()
        self.surf = pygame.Surface((1, 1))
        self.rect = self.surf.get_rect(center=(posx, posy))

    def update(self):
        pass

all_sprites = pygame.sprite.Group()
all_land = pygame.sprite.Group()
checks = pygame.sprite.Group()

def getGridScreen():
    tiles = []
    startX = 0
    for i in range(0, int(WIDTH/TILESIZE)):
        startY = 0
        startX += TILESIZE
        for j in range(0, int(HEIGHT/TILESIZE)):
            position = vec((startX, startY))
            tiles.append(position)
            startY += TILESIZE
    return tiles

def placeLand(density, grid):
    loop = [-TILESIZE*2, -TILESIZE, 0, TILESIZE, TILESIZE*2]
    for i in range(0, density):
        randPos = random.randint(0, len(grid)-1)
        for j in loop:
            for k in loop:
                if random.randint(0, 1) == 0:
                    LAND = Land(grid[randPos].x+j, grid[randPos].y+k)
                    all_sprites.add(LAND)
                    all_land.add(LAND)
        
def cellCheck(cellx, celly, place, neighbours):
    loop = [-TILESIZE, 0, TILESIZE]
    surround = 0
    for i in loop:
        for j in loop:
            CHECK = Check(cellx+i, celly+j)
            all_sprites.add(CHECK)
            checks.add(CHECK)
            if CHECK.update():
                surround += 1
    if surround >= neighbours:
        WATER = place(cellx, celly)
        all_sprites.add(WATER)
        all_land.add(WATER)

def singleCheck(cellx, celly, place):
    CHECK = Check(cellx, celly)
    all_sprites.add(CHECK)
    checks.add(CHECK)
    if CHECK.update() == False:
        PLACE = place(cellx, celly)
        all_sprites.add(PLACE)

def placeExtras(density, grid, type):
    for i in getGridScreen():
        CHECK = Check(i.x, i.y)
        all_sprites.add(CHECK)
        checks.add(CHECK)
        if CHECK.update():
            if random.randint(0, density) == 0:
                TYPE = type(i.x, i.y)
                all_sprites.add(TYPE)

placeLand(100, getGridScreen())

for loop in range(0, 3):
    for i in getGridScreen():
        cellCheck(i.x, i.y, Land, 7)

for i in getGridScreen():
    singleCheck(i.x, i.y, Water)

placeExtras(10, getGridScreen(), Tree)
placeExtras(20, getGridScreen(), Stone)
placeExtras(15, getGridScreen(), Vegitation)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    screen.fill((0,0,0))
    
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    pygame.display.update()
    FramesPerSecond.tick(FPS)