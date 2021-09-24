import random

import pygame
from time import sleep
from random import randrange

pygame.init()

width = pygame.display.Info().current_w
height = pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height))

difference = pygame.image.load('spot_the_diff.png')
difference = pygame.transform.scale(difference, (width, height))

zombie = pygame.image.load('scary_face.png')
zombie = pygame.transform.scale(zombie, (width, height))

scream = pygame.mixer.Sound("scream.wav")


screen.blit(difference,(0,0))
pygame.display.update()

sleep(randrange(5,15))

screen.blit(zombie,(0,0))
pygame.display.update()

sleep(0.2)

pygame.quit()
