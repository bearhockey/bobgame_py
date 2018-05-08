from json import load
import pygame
from os import path
from sys import exit

from src.Camera import Camera
from src.Controller import Controller
from src.Player import Player
from src.SpriteSheet import SpriteSheet
from src.Title import Title
from src.battle.BattleObject import BattleObject

assets = path.join("..", "assets")


def new_game(size_of_screen):
    with open(path.join(assets, "data", "ally_specs.json")) as data_file:
        data = load(data_file)["BOBMAN"]
        player_battle = BattleObject(name="Bobman",
                                     sprite_sheet=SpriteSheet(path.join(assets, "battle", data["BATTLE"]["SPRITE"]),
                                                              data["BATTLE"]["WIDTH"],
                                                              data["BATTLE"]["HEIGHT"]),
                                     sprite_rect=pygame.Rect(0, 0, data["BATTLE"]["WIDTH"], data["BATTLE"]["HEIGHT"]),
                                     team=0,
                                     stats=data["BATTLE"]["BASE_STATS"])
        player_data = {"properties": data}
        player_data["properties"]["SPEED"] = 4
        data_file.close()

    peter = Player(actor_json=player_data, battle_object=player_battle)
    cam = Camera(screen_size=size_of_screen, player=peter)
    cam.load_map(map_name="test_map")
    return cam


pygame.init()

clock = pygame.time.Clock()

screen_size = width, height = (1280, 720)
black = (0, 0, 0)
# needs to be set before any images are loaded
screen = pygame.display.set_mode(screen_size)
title_screen = Title(screen_size=screen_size)
camera = None
controller = Controller()
delay_timer = 0
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
                camera = new_game(size_of_screen=screen_size)
                state = "GAME"
            elif act == "LOAD":
                pass
            if act == "EXIT":
                exit(0)
        title_screen.draw(screen=screen)
    elif state == "GAME":
        camera.update(screen)
    pygame.display.flip()
    if delay_timer > 0:
        delay_timer -= 1
