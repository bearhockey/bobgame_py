import pygame
import os

from ActionMap import ActionMap
from Battle import Battle
from Controller import Controller
from Map import Map
from Player import Player
from TextBox import TextBox


class Camera(object):
    def __init__(self, screen_size, player):
        self.screen_size = screen_size
        self.view = None

        self.player = player
        self.controller = Controller(self.player)
        self.delay_timer = 0

        self.center_box = pygame.Rect(self.screen_size[0]/4, self.screen_size[1]/4,
                                      self.screen_size[0]/2, self.screen_size[1]/2)

        self.cam_center = (self.screen_size[0]/2, self.screen_size[1]/2)
        self.cam_offset_x = 0
        self.cam_offset_y = 0
        self.camera_speed = self.player.speed
        self.map = None
        self.action_map = None

        self.destination_door = None
        self.fade_alpha = 0
        self.fade_speed = 5
        self.fade_out = False
        self.fade_in = False

        self.text_box = None
        self.build_text_box()
        self.blackness = pygame.Surface(self.screen_size)
        self.blackness.fill((0, 0, 0))
        self.blackness.set_alpha(self.fade_alpha)

        # battle
        self.in_battle = False
        sample_back = pygame.image.load(os.path.normpath('../assets/background/mountains1.png'))
        sample_bat = pygame.image.load(os.path.normpath('../assets/battleground/grass1.png'))
        self.battle = Battle(self.screen_size, sample_bat, sample_back)

    def build_text_box(self, left=4, top=500, height=200, color=(20, 30, 200)):
        self.text_box = TextBox(pygame.Rect(left, top, self.screen_size[0] - left * 2, height), 'TEXT', color)

    def convert_door_destination(self, cords):
        x = int(cords[0]) * self.map.tileset_data['t_width']
        y = int(cords[1]) * self.map.tileset_data['t_height']
        return x, y

    def load_action_map(self, action_map_url):
        self.action_map = ActionMap(action_map_url, self.text_box)

    def load_map(self, map_url):
        real_url = os.path.join('..', 'assets', 'world', map_url)
        self.map = Map(real_url, self.text_box)
        if self.map.starting_location:
            self.player.teleport(self.map.starting_location)
        self.view = pygame.Surface(self.map.map_size)
        self.cam_offset_x = self.player.sprite_rect.left
        self.cam_offset_y = self.player.sprite_rect.top

    def update(self, screen):
        if self.in_battle:
            delay = self.controller.poll_battle(self.battle, self.delay_timer)
            self.battle.draw(screen)
            if delay:
                self.delay_timer += delay
        else:
            if not self.fade_in and not self.fade_out:
                # check for door intersection here?
                for d in self.map.door_list:
                    if d.door.colliderect(self.player.pass_rect):
                        self.destination_door = d
                        self.fade_alpha = 0
                        self.fade_out = True
                delay = self.controller.poll(self.map, self.text_box, self.delay_timer, self.action_map)
                if delay:
                    self.delay_timer += delay
                # check if camera should shift
                if self.player.sprite_rect.left < self.cam_offset_x-self.center_box.left:
                    self.cam_offset_x -= self.camera_speed
                elif self.player.sprite_rect.left > self.cam_offset_x+self.center_box.left:
                    self.cam_offset_x += self.camera_speed
                if self.player.sprite_rect.top < self.cam_offset_y-self.center_box.top:
                    self.cam_offset_y -= self.camera_speed
                elif self.player.sprite_rect.top > self.cam_offset_y+self.center_box.top:
                    self.cam_offset_y += self.camera_speed

            # draw things
            self.map.draw(self.view, passmap=False)
            self.player.draw(self.view)
            self.map.draw_upper(self.view)

            screen.blit(self.view, (self.cam_center[0]-self.cam_offset_x, self.cam_center[1]-self.cam_offset_y))
            # screen.blit(self.blackness, (0, 0))
            if self.text_box:
                self.text_box.draw(screen)

            if self.fade_in:
                if self.fade_alpha > 0:
                    self.fade_alpha -= self.fade_speed
                    self.blackness.set_alpha(self.fade_alpha)
                    screen.blit(self.blackness, (0, 0))
                else:
                    self.fade_in = False
            elif self.fade_out:
                if self.fade_alpha < 255:
                    self.fade_alpha += self.fade_speed
                    self.blackness.set_alpha(self.fade_alpha)
                    screen.blit(self.blackness, (0, 0))
                else:
                    self.fade_out = False
                    self.load_map(self.destination_door.destination_map)
                    self.player.teleport(self.convert_door_destination(self.destination_door.destination_cords))

        if self.delay_timer > 0:
            self.delay_timer -= 1
