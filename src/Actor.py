import pygame
from os import path

from src.SpriteSheet import SpriteSheet

import src.settings as settings


class Actor(pygame.sprite.Sprite):
    def __init__(self, object_json):
        self.data = object_json["properties"]
        pygame.sprite.Sprite.__init__(self)

        self.direction_dir = {"DOWN": 0, "LEFT": 1, "RIGHT": 2, "UP": 3}
        self.horizontal_cut = self.data["H_CUT"]
        self.vertical_cut = self.data["V_CUT"]

        self.sprite_sheet = SpriteSheet(filename=path.join(settings.ACTOR, self.data["ACTOR"]),
                                        pic_width=self.data["WIDTH"],
                                        pic_height=self.data["HEIGHT"])
        if 'x' in object_json:
            x = object_json['x']
        else:
            x = 0
        if 'y' in object_json:
            y = object_json['y']
        else:
            y = 0
        self.sprite_rect = pygame.Rect(x, y, self.data["WIDTH"], self.data["HEIGHT"])
        self.position = self.sprite_rect
        self.pass_rect = None
        self.translate_pass_rect()

        self.speed = self.data["SPEED"]
        self.direction = "DOWN"
        self.moving = False
        self.acting = False
        self.destination = self.position.left, self.position.top
        if "BEHAVIOR" in self.data:
            self.behavior = self.data["BEHAVIOR"]
        self.internal_clock = 0

    def translate_pass_rect(self):
        self.pass_rect = pygame.Rect(self.sprite_rect.left + self.horizontal_cut,
                                     self.sprite_rect.top + (self.sprite_rect.height / 2) + self.vertical_cut,
                                     self.sprite_rect.width - self.horizontal_cut * 2,
                                     self.sprite_rect.height / 2 - self.vertical_cut * 2)

    def get_action_rect(self):
        if self.direction == "UP":
            y_mod = -1
        elif self.direction == "DOWN":
            y_mod = 1
        else:
            y_mod = 0
        if self.direction == "LEFT":
            x_mod = -1
        elif self.direction == "RIGHT":
            x_mod = 1
        else:
            x_mod = 0

        return pygame.Rect(self.pass_rect.left + (self.pass_rect.width * x_mod),
                           self.pass_rect.top + (self.pass_rect.height * y_mod),
                           self.pass_rect.width, self.pass_rect.height)

    def set_speed(self, new_speed):
        self.speed = new_speed

    def turn_to_face(self, direction):
        # actor turns to FACE this direction, not turns IN this direction
        if direction == "UP":
            self.direction = "DOWN"
        elif direction == "DOWN":
            self.direction = "UP"
        elif direction == "LEFT":
            self.direction = "RIGHT"
        elif direction == "RIGHT":
            self.direction = "LEFT"
        else:
            print("Unrecognized direction '{0}'; setting to DOWN".format(direction))
            self.direction ="DOWN"

    def set_relative_destination(self, x, y):
        self.destination = (self.position.left + x, self.position.top + y)

    def set_destination(self, x, y):
        self.destination = x, y

    def move_to(self):
        if self.destination[0] > self.position.left:
            x_mod = 1
        elif self.destination[0] < self.position.left:
            x_mod = -1
        else:
            x_mod = 0
        if self.destination[1] > self.position.top:
            y_mod = 1
        elif self.destination[1] < self.position.top:
            y_mod = -1
        else:
            y_mod = 0
        if x_mod or y_mod:
            self.move(x=self.speed*x_mod, y=self.speed*y_mod)
            self.moving = True
            self.acting = True
        else:
            self.moving = False
            self.acting = False

    def move(self, x, y):
        self.sprite_rect.move_ip(x, y)
        self.pass_rect.move_ip(x, y)

    def teleport(self, x, y):
        self.sprite_rect.left = x
        self.sprite_rect.top = y
        self.translate_pass_rect()

    def action(self):
        if "ACTION" in self.data:
            return self.data["ACTION"]
        else:
            return None

    def draw(self, screen):
        if self.moving:
            self.sprite_sheet.animate(screen, self.sprite_rect, self.direction_dir[self.direction], 10)
        else:
            self.sprite_sheet.draw(screen, self.sprite_rect, 1, self.direction_dir[self.direction])
