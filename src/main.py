import pygame
import sys

from ActionMap import ActionMap
from Controller import Controller
from Map import Map
from Player import Player
from SpriteSheet import SpriteSheet
from TextBox import TextBox

pygame.init()

clock = pygame.time.Clock()
delay_timer = 0

size = width, height = (1280, 720)
black = (0, 0, 0)
# needs to be set before any images are loaded
screen = pygame.display.set_mode(size)

peter = Player(SpriteSheet('..\\assets\\pete3a.png', 32, 48), pygame.Rect(10, 10, 32, 48))
controller = Controller(peter)

tbox = TextBox(pygame.Rect(4, 500, width - 8, 200), 'Howdy', (20, 30, 200))

test_map = Map('..\\assets\\test_map_1.json', size, tbox)
action_map = ActionMap('..\\assets\\action.map', tbox)

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    delay = controller.poll(test_map, tbox, delay_timer, action_map)
    if delay:
        delay_timer += delay
    screen.fill(black)
    test_map.draw(screen, passmap=False)
    peter.draw(screen)
    # test_map.draw_upper(screen)
    if tbox:
        tbox.draw(screen)
    pygame.display.flip()
    if delay_timer > 0:
        delay_timer -= 1
