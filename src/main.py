from json import load
import pygame
from os import path
from sys import exit

from src.Camera import Camera
from src.Controller import Controller
from src.Title import Title

# screen_size = width, height = (640, 400) # SNES view
screen_size = width, height = (800, 480) # mobile view
# screen_size = width, height = (1280, 720)  # desktop view
font_size = int(height/30)
black = (0, 0, 0)


def start_game(game_data):
    char_data = game_data["CHAR"]
    map_data = game_data["LOC"]
    flags = game_data["FLAGS"]
    cam = Camera(screen_size=screen_size, font_size=font_size, roster=char_data, flags=flags)
    cam.load_map(map_name=map_data["MAP"], goto=map_data["POSITION"])
    return cam


def new_game():
    new_game_data = {
        "CHAR": [
            {
                "DATA": "BOBMAN",
                "NAME": None,
                "STATS": None
            }],
        "LOC": {
            "MAP": "test_map",
            "POSITION": None
        },
        "FLAGS": {}
    }
    return start_game(game_data=new_game_data)


def load_game():
    with open(path.join("..", "data", "save.json")) as data_file:
        data = load(data_file)
        data_file.close()
    return start_game(game_data=data)


pygame.init()

clock = pygame.time.Clock()

# needs to be set before any images are loaded
screen = pygame.display.set_mode(screen_size)
title_screen = Title(screen_size=screen_size, font_size=font_size)
camera = None
controller = Controller()
state = "TITLE"


while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            camera.exit()

    screen.fill(black)
    if state == "TITLE":
        action = controller.poll_menu(menu=title_screen.title_menu)
        if action:
            act = action["ACT"]
            if act == "NEW":
                # start new game
                camera = new_game()
                state = "GAME"
            elif act == "LOAD":
                camera = load_game()
                state = "GAME"
            if act == "EXIT":
                exit(0)
        title_screen.draw(screen=screen)
    elif state == "GAME":
        camera.update(screen)
    pygame.display.flip()
