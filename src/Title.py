import pygame
from src.box.SelectBox import SelectBox


class Title(object):
    def __init__(self, screen_size):
        title_menu_color = (20, 40, 200)
        self.title_menu = SelectBox(box_bounds=pygame.Rect(screen_size[0]/3,
                                                           screen_size[1]/2,
                                                           screen_size[0]/3,
                                                           screen_size[1]/4),
                                    color=title_menu_color)
        self.title_menu.options = [{"NAME": "New Game", "ACT": "NEW"},
                                   {"NAME": "Load Game", "ACT": "LOAD"},
                                   {"NAME": "Exit", "ACT": "EXIT"}]
        self.title_menu.open()

    def draw(self, screen):
        self.title_menu.draw(screen=screen)
