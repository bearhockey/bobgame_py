import pygame
from sys import exit

from src.Camera import Camera
from src.Controller import Controller
from src.Player import Player
from src.SpriteSheet import SpriteSheet
from src.Title import Title
from src.battle.BattleObject import BattleObject


def new_game(size_of_screen):
    # player setup
    peter_battle = (BattleObject(name="player",
                                 sprite_sheet=SpriteSheet("..\\assets\\battle\\ninjabob1.png", 48, 48),
                                 sprite_rect=pygame.Rect(900, 400, 48, 48),
                                 team=0,
                                 stats={"HP_MAX": 50, "HP_CURRENT": 50, "STR": 5, "DEF": 4}))
    player_data = {
        "properties": {
            "ACTOR": "pete3a.png",
            "WIDTH": 32,
            "HEIGHT": 48,
            "H_CUT": 8,
            "V_CUT": 2,
            "SPEED": 4
        }
    }
    peter = Player(actor_json=player_data, battle_object=peter_battle)
    cam = Camera(screen_size=size_of_screen, player=peter)
    cam.load_map(map_url="test_map_1.json")
    cam.load_action_map("action_map1.json")
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
