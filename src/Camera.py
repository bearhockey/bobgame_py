import random
import pygame
import sys

from src.battle.Battle import Battle
from src.Controller import Controller
from src.Map import Map
from src.Menu import Menu
from src.TextBox import TextBox


class Camera(object):
    def __init__(self, screen_size, player):
        self.screen_size = screen_size

        self.player = player
        self.controller = Controller()

        self.center_box = pygame.Rect(self.screen_size[0]/4, self.screen_size[1]/4,
                                      self.screen_size[0]/2, self.screen_size[1]/2)

        self.cam_center = (self.screen_size[0]/2, self.screen_size[1]/2)
        self.cam_offset_x = 0
        self.cam_offset_y = 0
        self.camera_speed = self.player.speed
        self.map = None
        self.menu = None
        self.show_menu = False

        self.destination_door = None
        self.fade_alpha = 0
        self.fade_speed = 5
        self.fade_out = False
        self.fade_in = False

        self.text_box = self.build_text_box()
        self.blackness = pygame.Surface(self.screen_size)
        self.blackness.fill((0, 0, 0))
        self.blackness.set_alpha(self.fade_alpha)

        # battle
        self.in_battle = False
        self.battle = None

    def build_text_box(self, left=4, top=500, height=200, color=(20, 30, 200)):
        return TextBox(pygame.Rect(left, top, self.screen_size[0] - left * 2, height), "TEXT", color)

    def convert_door_destination(self, cords):
        x = int(cords[0]) * self.map.tileset_data["t_width"]
        y = int(cords[1]) * self.map.tileset_data["t_height"]
        return x, y

    def load_map(self, map_name):
        self.map = Map(camera=self, directory=map_name)
        if self.map.starting_location:
            self.player.teleport(x=self.map.starting_location[0], y=self.map.starting_location[1])
        self.cam_offset_x = self.player.sprite_rect.left
        self.cam_offset_y = self.player.sprite_rect.top

    def draw_map(self, screen, draw_player=True):
        view = pygame.Surface(self.map.map_size)
        self.map.draw(view, passmap=False)
        if draw_player:
            self.player.draw(view)
        self.map.draw_upper(view)
        screen.blit(view, (self.cam_center[0] - self.cam_offset_x, self.cam_center[1] - self.cam_offset_y))

    def open_menu(self):
        self.menu = Menu(screen_size=self.screen_size, color=(20, 30, 200), actor_list=[self.player])
        self.show_menu = True
        self.menu.open()

    def close_menu(self):
        self.menu.close()
        self.show_menu = False
        self.menu = None

    def start_battle(self, battle_info):
        self.battle = Battle(screen_size=self.screen_size, battle_info=battle_info, player=self.player)
        self.in_battle = True

    def update(self, screen):
        if self.in_battle:
            if self.battle.state == "END":
                self.in_battle = False
                self.battle = None
            else:
                self.controller.poll_battle(self.battle)
                self.battle.draw(screen)
        elif self.show_menu:
            self.controller.poll_main_menu(camera=self)
            # performance hit might be if you draw this map under the box
            self.draw_map(screen=screen, draw_player=False)
            if self.menu:
                self.menu.draw(screen)
        else:
            if not self.fade_in and not self.fade_out:
                # check for door intersection here?
                for d in self.map.door_list:
                    if d.door.colliderect(self.player.pass_rect):
                        self.destination_door = d
                        self.fade_alpha = 0
                        self.fade_out = True
                if self.player.acting:
                    self.player.move_to()
                else:
                    self.controller.poll(self, self.text_box, self.map.action_map)
                # check if camera should shift
                if self.player.sprite_rect.left < self.cam_offset_x-self.center_box.left:
                    self.cam_offset_x -= self.camera_speed
                elif self.player.sprite_rect.left > self.cam_offset_x+self.center_box.left:
                    self.cam_offset_x += self.camera_speed
                if self.player.sprite_rect.top < self.cam_offset_y-self.center_box.top:
                    self.cam_offset_y -= self.camera_speed
                elif self.player.sprite_rect.top > self.cam_offset_y+self.center_box.top:
                    self.cam_offset_y += self.camera_speed

            # update NPC movement
            for actor in self.map.actor_list:
                if actor.behavior == "WANDER":
                    if actor.internal_clock > 1:
                        actor.move_to()
                        actor.internal_clock -= 1
                    else:
                        x = random.randrange(-3, 4) * actor.position.width + actor.position.left
                        y = random.randrange(-3, 4) * actor.position.height + actor.position.top
                        actor.set_destination(x=x, y=y)
                        print("MOVING ACTOR from {0}, {1} to {2}, {3}".format(actor.position.left, actor.position.top, x, y))
                        actor.internal_clock = random.randrange(200, 400)

            # draw things
            self.draw_map(screen=screen)
            screen.blit(self.blackness, (0, 0))
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
                    self.fade_in = True
                    print(self.destination_door.destination_map)
                    self.load_map(map_name=self.destination_door.destination_map)
                    door_cords = self.convert_door_destination(self.destination_door.destination_cords)
                    self.player.teleport(x=door_cords[0], y=door_cords[1])

    def save_game(self):
        char_block = {"STATS": self.player}
        save_block = {}
    @staticmethod
    def exit():
        print("Exiting gracefully...")
        sys.exit(0)
