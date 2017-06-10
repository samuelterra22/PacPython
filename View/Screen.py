import pygame, sys, random
from pygame.locals import *

pygame.init()

# Cores

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
yellow = (255,255,0)

change_rate = 10
tick = 13

gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PacPython \o/")

gameExit = False

lead_x = 300
lead_y = 300
lead_x_change = 0
lead_y_change = 0

clock = pygame.time.Clock()

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                lead_x_change = -change_rate
                lead_y_change = 0
            if event.key == pygame.K_RIGHT:
                lead_x_change = change_rate
                lead_y_change = 0
            if event.key == pygame.K_UP:
                lead_y_change = -change_rate
                lead_x_change = 0
            if event.key == pygame.K_DOWN:
                lead_y_change = change_rate
                lead_x_change = 0

    lead_x += lead_x_change
    lead_y += lead_y_change
    gameDisplay.fill(black)
    pygame.draw.circle(gameDisplay, yellow, (lead_x,lead_y), 15, 0)
    pygame.display.update()

    # FPS

    clock.tick(tick)


pygame.quit()
quit()
