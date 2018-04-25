import pygame
# from SpriteSheet import SpriteSheet


class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, sprite_rect, horizontal_cut, veritcal_cut, battle_object):
        pygame.sprite.Sprite.__init__(self)

        self.direction_dir = {"down": 0,
                              "left": 1,
                              "right": 2,
                              "up": 3
                              }
        self.horizontal_cut = horizontal_cut
        self.vertical_cut = veritcal_cut

        self.sprite_sheet = sprite_sheet
        self.sprite_rect = sprite_rect
        self.pass_rect = None
        self.translate_pass_rect()

        self.speed = 4
        self.direction = self.direction_dir["down"]
        self.moving = False

        self.battle_object = battle_object

    def translate_pass_rect(self):
        self.pass_rect = pygame.Rect(self.sprite_rect.left + self.horizontal_cut,
                                     self.sprite_rect.top + (self.sprite_rect.height / 2) + self.vertical_cut,
                                     self.sprite_rect.width - self.horizontal_cut * 2,
                                     self.sprite_rect.height / 2 - self.vertical_cut * 2)

    def get_action_rect(self):
        if self.direction == self.direction_dir["up"]:
            y_mod = -1
        elif self.direction == self.direction_dir["down"]:
            y_mod = 1
        else:
            y_mod = 0
        if self.direction == self.direction_dir["left"]:
            x_mod = -1
        elif self.direction == self.direction_dir["right"]:
            x_mod = 1
        else:
            x_mod = 0

        return pygame.Rect(self.pass_rect.left + (self.pass_rect.width * x_mod),
                           self.pass_rect.top + (self.pass_rect.height * y_mod),
                           self.pass_rect.width, self.pass_rect.height)

    def set_speed(self, new_speed):
        self.speed = new_speed

    def set_direction(self, direction):
        self.direction = self.direction_dir[direction]

    def move(self, x, y):
        self.sprite_rect.move_ip(x, y)
        self.pass_rect.move_ip(x, y)

    def teleport(self, x, y):
        self.sprite_rect.left = x
        self.sprite_rect.top = y
        self.translate_pass_rect()

    def draw(self, screen):
        if self.moving:
            self.sprite_sheet.animate(screen, self.sprite_rect, self.direction, 10)
        else:
            self.sprite_sheet.draw(screen, self.sprite_rect, 1, self.direction)
