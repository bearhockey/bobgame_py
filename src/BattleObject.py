import pygame


class BattleObject(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, sprite_rect, flipped=False):
        pygame.sprite.Sprite.__init__(self)
        self.state_dict = {'attack': 0,
                              'attack2': 1,
                              'idle': 2,
                              'cast': 3,
                              'defend': 4,
                              'hurt': 5,
                              'dead': 6,
                              'weak': 7,
                              'misc': 8,
                              'walk': 9}
        self.sprite_sheet = sprite_sheet
        self.sprite_rect = sprite_rect

        self.animation_state = self.state_dict['idle']
        self.flipped = flipped
        self.animation_delay = 5

    def draw(self, screen):
        self.sprite_sheet.animate(screen, self.sprite_rect, self.animation_state, self.animation_delay,
                                  flipped=self.flipped)
