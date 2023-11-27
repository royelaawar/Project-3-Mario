import pygame
from pygame.locals import *

pygame.init()

screen_width = 1600
screen_height = 900

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

bg_img = pygame.image.load('images/sky-4.png')
sun_img = pygame.image.load('images/bomb.png')

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Blit the background image onto the screen
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (1300, 50))

    # Update the display
    pygame.display.flip()

pygame.quit()