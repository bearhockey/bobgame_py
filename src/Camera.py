import pygame

from ActionMap import ActionMap
from Controller import Controller
from Map import Map
from Player import Player
from TextBox import TextBox


class Camera(object):
    def __init__(self, screen_size, player):
        print 'this is a camera'

        self.screen_size = screen_size

        self.player = player
        self.controller = Controller(self.player)
        self.delay_timer = 0

        self.cam_offset_x = 0
        self.cam_offset_y = 0
        self.map = None
        self.action_map = None

        self.text_box = None
        self.build_text_box()

    def build_text_box(self, left=4, top=500, height=200, color=(20, 30, 200)):
        self.text_box = TextBox(pygame.Rect(left, top, self.screen_size[0] - left * 2, height), 'TEXT', color)

    def load_action_map(self, action_map_url):
        self.action_map = ActionMap(action_map_url, self.text_box)

    def load_map(self, map_url):
        self.map = Map(map_url, self.screen_size, self.text_box)
        if self.map.starting_location:
            self.player.teleport(self.map.starting_location[0], self.map.starting_location[1])

    def update(self, screen):
        delay = self.controller.poll(self.map, self.text_box, self.delay_timer, self.action_map)
        if delay:
            self.delay_timer += delay
        # check if camera should shift
        if self.player.sprite_rect.top > self.screen_size[1]/2:
            self.cam_offset_y -= 1
        self.map.draw(screen, (self.cam_offset_x, self.cam_offset_y), passmap=False)
        self.player.draw(screen)
        self.map.draw_upper(screen, (self.cam_offset_x, self.cam_offset_y))
        if self.text_box:
            self.text_box.draw(screen)

        if self.delay_timer > 0:
            self.delay_timer -= 1
