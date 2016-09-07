import pygame

from BattleMenu import BattleMenu
from BattleObject import BattleObject
from BattleWheel import BattleWheel
from SpriteSheet import SpriteSheet


class Battle (object):
    def __init__(self, screen_size, foreground=None, background=None):
        print 'Battle started'
        self.player_list = []
        self.enemy_list = []
        self.top_lane = []
        self.middle_lane = []
        self.bottom_lane = []

        self.menu_color = (20, 30, 200)

        self.screen_size = screen_size
        self.background = background
        self.foreground = foreground
        self.f_position = self.screen_size[1]/2

        self.player_list.append(BattleObject(SpriteSheet('..\\assets\\battle\\ninjabob1.png', 48, 48),
                                             pygame.Rect(900, 400, 48, 48)))
        self.enemy_list.append(BattleObject(SpriteSheet('..\\assets\\battle\\fxy.png', 100, 80),
                                             pygame.Rect(100, 500, 100, 80)))
        self.enemy_list[0].animation_state = 0
        self.enemy_list[0].actions = ["poop", "hgey", "not", "great"]

        self.battle_box = None
        self.build_battle_menu(left=self.screen_size[0]/3+self.screen_size[0]/3, width=self.screen_size[0]/3 - 8)
        actor_list = self.player_list + self.enemy_list
        self.battle_wheel = BattleWheel(actors=actor_list, position=(120, 110), radius=100, background=self.menu_color)

        self.current_actor = None
        self.start_turn()

    def start_turn(self):
        self.current_actor = self.battle_wheel.get_next()
        self.battle_box.options = self.current_actor.actions
        self.battle_box.open()

    def end_turn(self):
        self.battle_wheel.set_actor_time(5)

    def character_action(self):
        self.battle_box.close()
        self.current_actor.act(self.battle_box.get_action())
        self.end_turn()
        self.start_turn()

    def build_battle_menu(self, left=4, top=10, width=None, height=200,
                          color=(20, 30, 200)):
        if width is None:
            width = self.screen_size[0]/2 - 8
        self.battle_box = BattleMenu(pygame.Rect(left, top, width, height), options=[], color=color)
        # self.battle_box.open()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.foreground, (0, self.f_position))
        if self.player_list:
            for p in self.player_list:
                p.draw(screen)
        if self.enemy_list:
            for e in self.enemy_list:
                e.draw(screen)

        self.battle_wheel.draw(screen)
        self.battle_box.draw(screen)
