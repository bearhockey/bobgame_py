__author__ = 'max_hart'

import pygame


class TextBox(pygame.sprite.Sprite):
    def __init__(self, box_bounds, text, color=None, picture=None):
        pygame.sprite.Sprite.__init__(self)

        self.box = box_bounds
        self.text = text
        self.portrait = picture

