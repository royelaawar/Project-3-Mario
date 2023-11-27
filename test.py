import pygame
from pygame.locals import *

pygame.init()

screen_width = 1300
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

bg_img = pygame.image.load('images/sky2.png')

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Blit the background image onto the screen
    screen.blit(bg_img, (0, 0))

    # Update the display
    pygame.display.flip()

pygame.quit()