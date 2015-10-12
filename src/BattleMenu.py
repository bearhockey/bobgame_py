import pygame

from Box import Box


class BattleMenu(Box):
    def __init__(self, box_bounds, color=None):
        Box.__init__(self, box_bounds, color)

    def draw(self, screen):
        if self.visible:
            Box.draw(self, screen)

    def open(self, color=None):
        Box.open(self, color)

    def close(self):
        Box.close(self)
