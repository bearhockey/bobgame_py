__author__ = 'max_hart'

import sys
import pygame
from SpriteSheet import SpriteSheet
from Map import Map
from Player import Player
from Controller import Controller

pygame.init()

clock = pygame.time.Clock()

size = width, height = (1280, 720)
black = (0, 0, 0)

screen = pygame.display.set_mode(size)
peter = Player(SpriteSheet('..\\assets\\pete3a.png', 32, 48), pygame.Rect(10, 10, 32, 48))
controller = Controller(peter)
test_map = Map('..\\assets\\test_map_1.json', size)

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    controller.poll(test_map)
    screen.fill(black)
    test_map.draw(screen, passmap=False)
    peter.draw(screen)
    # peter.draw(screen, (10, 10), 1, 4)
    # peter.animate(screen, player, 0, 10)
    pygame.display.flip()
