import pygame, sys, random
from pygame.locals import *

def screen_init():
    w = 800
    h = 480
    z = 0

    screen = pygame.display.set_mode((w,h))
    pygame.display.flip()
    clock = pygame.time.Clock()

    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((0,0,0))
        pygame.display.update()

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PacPython \o/")

gameExit = False

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        #print(event)

    gameDisplay.fill(red)
    pygame.display.update()


pygame.quit()
quit()
