import pygame
import sys

from src.Camera import Camera
from src.Player import Player
from src.SpriteSheet import SpriteSheet

pygame.init()

clock = pygame.time.Clock()

screen_size = width, height = (1280, 720)
black = (0, 0, 0)
# needs to be set before any images are loaded
screen = pygame.display.set_mode(screen_size)

peter = Player(SpriteSheet("..\\assets\\pete3a.png", 32, 48), pygame.Rect(10, 10, 32, 48), 8, 2)

camera = Camera(screen_size, peter)
camera.load_map("test_map_1.json")
camera.load_action_map("..\\assets\\world\\action_map1.json")

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    screen.fill(black)
    camera.update(screen)
    pygame.display.flip()
