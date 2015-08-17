__author__ = 'max_hart'

import sys
import pygame
from SpriteSheet import SpriteSheet
from Map import Map

pygame.init()

clock = pygame.time.Clock()

size = width, height = (800, 600)
black = (0, 0, 0)

screen = pygame.display.set_mode(size)
player = pygame.Rect(10, 10, 32, 48)
peter = SpriteSheet('..\\assets\\pete3a.png', 32, 48)
test_map = Map('..\\assets\\test_map_1.json')

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    # move this to keyboard controller
    if pygame.key.get_focused():
        press = pygame.key.get_pressed()
        if press[pygame.K_DOWN] != 0:
            test = player.copy()
            blocked = False
            for x in test_map.passmap:
                if test.move(0, 4).colliderect(x):
                    blocked = True
            if not blocked:
                player.move_ip(0, 4)
        elif press[pygame.K_UP] != 0:
            test = player.copy()
            blocked = False
            for x in test_map.passmap:
                if test.move(0, -4).colliderect(x):
                    blocked = True
            if not blocked:
                player.move_ip(0, -4)
        if press[pygame.K_LEFT] != 0:
            test = player.copy()
            blocked = False
            for x in test_map.passmap:
                if test.move(-4, 0).colliderect(x):
                    blocked = True
            if not blocked:
                player.move_ip(-4, 0)
        elif press[pygame.K_RIGHT] != 0:
            test = player.copy()
            blocked = False
            for x in test_map.passmap:
                if test.move(4, 0).colliderect(x):
                    blocked = True
            if not blocked:
                player.move_ip(4, 0)

    screen.fill(black)
    test_map.draw(screen, passmap=True)
    # peter.draw(screen, (10, 10), 1, 4)
    peter.animate(screen, player, 0, 10)
    pygame.display.flip()
