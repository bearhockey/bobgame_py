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
screen_size = width, height = (1280, 720)
black = (0, 0, 0)
player_speed = 4


def start_game(game_data):
    char_data = game_data["CHAR"]
    map_data = game_data["LOC"]
    with open(path.join(assets, "data", "ally_specs.json")) as data_file:
        data = load(data_file)[char_data["DATA"]]
        player_battle = BattleObject(name="Bobman",
                                     sprite_sheet=SpriteSheet(path.join(assets, "battle", data["BATTLE"]["SPRITE"]),
                                                              data["BATTLE"]["WIDTH"],
                                                              data["BATTLE"]["HEIGHT"]),
                                     sprite_rect=pygame.Rect(0, 0, data["BATTLE"]["WIDTH"], data["BATTLE"]["HEIGHT"]),
                                     team=0,
                                     stats=char_data["STATS"] or data["BATTLE"]["BASE_STATS"])
        player_data = {"properties": data}
        player_data["properties"]["SPEED"] = player_speed
        data_file.close()

    player = Player(actor_json=player_data, battle_object=player_battle)
    cam = Camera(screen_size=screen_size, player=player)
    cam.load_map(map_name=map_data["MAP"], goto=map_data["POSITION"])
    return cam


def new_game():
    new_game_data = {
        "CHAR": {
            "DATA": "BOBMAN",
            "STATS": None
        },
        "LOC": {
            "MAP": "test_map",
            "POSITION": None
        }
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
