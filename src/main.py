import pygame

from src.Camera import Camera
from src.Player import Player
from src.SpriteSheet import SpriteSheet
from src.battle.BattleObject import BattleObject

pygame.init()

clock = pygame.time.Clock()

screen_size = width, height = (1280, 720)
black = (0, 0, 0)
# needs to be set before any images are loaded
screen = pygame.display.set_mode(screen_size)

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

camera = Camera(screen_size, peter)
camera.load_map("test_map_1.json")
camera.load_action_map("..\\assets\\world\\action_map1.json")

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            camera.exit()

    screen.fill(black)
    camera.update(screen)
    pygame.display.flip()
