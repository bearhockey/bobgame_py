import pygame
import os

from src.Actor import Actor
# from SpriteSheet import SpriteSheet


class Player(Actor):
    def __init__(self, actor_json, battle_object, portrait=None):
        Actor.__init__(self, object_json=actor_json)

        self.battle_object = battle_object

        if not portrait:
            self.portrait = pygame.image.load(os.path.join("..", "assets", "portraits", "ball_2.gif")).convert_alpha()
        else:
            self.portrait = portrait
