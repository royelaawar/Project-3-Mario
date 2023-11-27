import pygame
from pygame.locals import *

pygame.init()

screen_width = 1300
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

sun_img = pygame.image.load('./images/sun1.png')
bg_img = pygame.image.load('./images/sky-3.png')

run = True
while run:

    screen.blit(bg_img(0, 0))
    screen.blit(sun_img(100, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
