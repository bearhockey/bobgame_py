import json
import random
from os import path
import pygame
import sys

from src.battle.Battle import Battle
from src.battle.BattleObject import BattleObject
from src.box.Notice import Notice
from src.Controller import Controller
from src.Map import Map
from src.Menu import Menu
from src.Player import Player
from src.SpriteSheet import SpriteSheet
from src.box.TextBox import TextBox

import src.settings as settings


class Camera(object):
    def __init__(self, screen_size, font_size, roster, flags):
        self.screen_size = screen_size
        self.font_size = font_size
        self.flags = flags
        self.controller = Controller()
        # build team roster
        self.team = []
        for hero in roster:
            self.add_hero(hero_data=hero)

        self.player = self.team[0]

        self.center_box = pygame.Rect(self.screen_size[0]/4, self.screen_size[1]/4,
                                      self.screen_size[0]/2, self.screen_size[1]/2)

        self.cam_center = (self.screen_size[0]/2, self.screen_size[1]/2)
        self.cam_offset_x = 0
        self.cam_offset_y = 0
        self.map = None
        self.menu = None
        self.show_menu = False

        self.notification = None

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

    def build_text_box(self, padding=4, height=200, color=(20, 30, 200)):
        top = self.screen_size[1]-height-padding
        return TextBox(box_bounds=pygame.Rect(padding, top, self.screen_size[0] - padding * 2, height),
                       text="TEXT",
                       color=color,
                       font_size=self.font_size)

    def convert_door_destination(self, cords):
        x = int(cords[0]) * self.map.tileset_data["t_width"]
        y = int(cords[1]) * self.map.tileset_data["t_height"]
        return x, y

    def load_map(self, map_name, goto=None):
        self.map = Map(camera=self, directory=map_name)
        if goto:
            self.player.teleport(x=goto[0], y=goto[1])
        elif self.map.starting_location:
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
        self.menu = Menu(screen_size=self.screen_size,
                         actor_list=self.team,
                         color=(20, 30, 200),
                         font_size=self.font_size)
        self.show_menu = True
        self.menu.open()

    def close_menu(self):
        self.menu.close()
        self.show_menu = False
        self.menu = None

    def add_hero(self, hero_data):
        with open(path.join(settings.ASS_DATA, "ally_specs.json")) as data_file:
            data = json.load(data_file)[hero_data["DATA"]]
            player_battle = BattleObject(name=hero_data["NAME"] or data["NAME"],
                                         sprite_sheet=SpriteSheet(path.join(settings.BATTLE, data["BATTLE"]["SPRITE"]),
                                                                  data["BATTLE"]["WIDTH"],
                                                                  data["BATTLE"]["HEIGHT"]),
                                         sprite_rect=pygame.Rect(0, 0, data["BATTLE"]["WIDTH"],
                                                                 data["BATTLE"]["HEIGHT"]),
                                         team=0,
                                         stats=hero_data["STATS"] or data["BATTLE"]["BASE_STATS"],
                                         actions=['0', '1', '2', '3', '4'])
            player_data = {"properties": data}
            player_data["properties"]["SPEED"] = settings.PLAYER_SPEED
            self.team.append(Player(actor_id=hero_data["DATA"], actor_json=player_data, battle_object=player_battle))
            data_file.close()

    def start_battle(self, battle_index):
        self.battle = Battle(screen_size=self.screen_size,
                             font_size=self.font_size,
                             battle_index=battle_index,
                             team=self.team)
        self.in_battle = True

    def update(self, screen):
        if self.notification:
            self.notification.draw(screen)
            if self.controller.any_key():
                self.notification = None
        elif self.in_battle:
            if self.battle.state == "END":
                self.in_battle = False
                self.battle = None
            else:
                self.controller.poll_battle(self.battle)
                self.battle.update(screen=screen)
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
                    self.controller.poll(camera=self,
                                         tbox=self.text_box,
                                         action_map=self.map.action_map)
                # check if camera should shift
                if self.player.sprite_rect.left < self.cam_offset_x-self.center_box.left:
                    self.cam_offset_x -= settings.CAM_SPEED
                elif self.player.sprite_rect.left > self.cam_offset_x+self.center_box.left:
                    self.cam_offset_x += settings.CAM_SPEED
                if self.player.sprite_rect.top < self.cam_offset_y-self.center_box.top:
                    self.cam_offset_y -= settings.CAM_SPEED
                elif self.player.sprite_rect.top > self.cam_offset_y+self.center_box.top:
                    self.cam_offset_y += settings.CAM_SPEED

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
                        # print("MOVING ACTOR from {0}, {1} to {2}, {3}".format(actor.position.left,
                        #                                                       actor.position.top, x, y))
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
        char_block = []
        for hero in self.team:
            char_block.append({"DATA": hero.id, "NAME": hero.battle_object.name, "STATS": hero.battle_object.stats})
        loc_block = {"MAP": self.map.name,
                     "POSITION": (self.player.sprite_rect.left, self.player.sprite_rect.top)
                     }
        save_block = {"CHAR": char_block,
                      "LOC": loc_block,
                      "FLAGS": self.flags
                      }
        with open(path.join(settings.SAVE, "save.json"), 'w') as out_file:
            json.dump(save_block, out_file)
            out_file.close()
        self.notification = Notice(screen_size=self.screen_size, text="GAME SAVED", color=(80, 80, 150))

    def exit(self):
        print("Exiting gracefully...")
        sys.exit(0)
