import pygame
from src.box.TextBox import TextBox


class SelectBox(object):
    def __init__(self, position, box_size, color=None, pressed_color=None, font_size=None, options=None):
        spacing = 10
        self.options = []
        if options:
            i = 0
            for option in options:
                self.options.append({
                    "BOX": TextBox(box_bounds=pygame.Rect(position[0],
                                                          position[1]+(box_size[1]+spacing)*i,
                                                          box_size[0],
                                                          box_size[1]),
                                   text=[option["TEXT"]],
                                   color=color,
                                   pressed_color=pressed_color,
                                   font_size=font_size,
                                   start_open=True),
                    "ACT": option["ACT"]
                })
                i += 1

    def draw(self, screen):
        for option in self.options:
            option["BOX"].draw(screen=screen)

    def click(self):
        for option in self.options:
            if option["BOX"].click():
                return option["ACT"]
