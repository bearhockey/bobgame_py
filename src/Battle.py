import pygame

from BattleMenu import BattleMenu
from BattleObject import BattleObject
from SpriteSheet import SpriteSheet


class Battle (object):
    def __init__(self, screen_size, foreground=None, background=None):
        print 'Battle started'
        self.player_list = []
        self.enemy_list = []

        self.screen_size = screen_size
        self.background = background
        self.foreground = foreground
        self.f_position = self.screen_size[1]/2

        self.player_list.append(BattleObject(SpriteSheet('..\\assets\\battle\\ninjabob1.png', 48, 48),
                                             pygame.Rect(900, 400, 48, 48)))
        self.enemy_list.append(BattleObject(SpriteSheet('..\\assets\\battle\\fxy.png', 100, 80),
                                             pygame.Rect(100, 500, 100, 80)))
        self.enemy_list[0].animation_state = 0

        self.battle_box = None
        self.build_battle_menu(left=self.screen_size[0]/3+self.screen_size[0]/3, width=self.screen_size[0]/3 - 8)
        print self.screen_size[0]/2

    def build_battle_menu(self, left=4, top=10, width=None, height=200,
                          color=(20, 30, 200)):
        if width is None:
            width = self.screen_size[0]/2 - 8
        choices = ['Fight', 'Defend', 'Item']
        self.battle_box = BattleMenu(pygame.Rect(left, top, width, height), options=choices, color=color)
        self.battle_box.open()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.foreground, (0, self.f_position))
        if self.player_list:
            for p in self.player_list:
                p.draw(screen)
        if self.enemy_list:
            for e in self.enemy_list:
                e.draw(screen)

        self.battle_box.draw(screen)
