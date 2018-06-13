import json
from os import path
import pygame
from random import choice

from src.box.SelectBox import SelectBox
from src.box.TextBox import TextBox

from src.battle.BattleObject import BattleObject
from src.battle.BattlePicker import BattlePicker
from src.battle.BattleWheel import BattleWheel
from src.SpriteSheet import SpriteSheet


import src.settings as settings


class Battle (object):
    def __init__(self, screen_size, font_size, battle_index, team):
        # grab battle info from encounter map
        with open(path.join(settings.ASS_DATA, "encounter_map.json")) as encounter_map:
            battle_info = json.load(encounter_map)[battle_index]
            encounter_map.close()
        # grab list of battle actions (gonna be a lot; maybe trim this down somehow?)
        with open(path.join(settings.ASS_DATA, "battle_action.json")) as data_file:
            self.battle_actions = json.load(data_file)
            data_file.close()
        print("Battle started")
        self.object_list = []
        self.top_lane = []
        self.middle_lane = []
        self.bottom_lane = []
        self.damage_numbers = []

        self.menu_color = (20, 30, 200)

        self.screen_size = screen_size
        self.font_size = font_size
        self.background = pygame.image.load(path.join(settings.BACKGROUND, battle_info["BACKGROUND"]))
        self.foreground = pygame.image.load(path.join(settings.BATTLEGROUND, battle_info["FOREGROUND"]))
        self.f_position = self.screen_size[1]/2

        # load players
        i = 0
        for player in team:
            player.battle_object.set_position(x=screen_size[0]/4*3+(i*10), y=screen_size[1]/3*2+(i*50))
            # player.battle_object.set_position(x=battle_info["SLOTS"][i][0], y=battle_info["SLOTS"][i][1])
            self.object_list.append(player.battle_object)
            i += 1
        # load enemies
        with open(path.join(settings.ASS_DATA, "enemy_map.json")) as enemy_file:
            enemy_list = json.load(enemy_file)
            enemy_file.close()
            for enemy in battle_info["ENEMIES"]:
                enemy_data = enemy_list[enemy["ENTITY"]]
                sprite_path = path.join(settings.BATTLE, enemy_data["SPRITE_SHEET"])
                sprite_sheet = SpriteSheet(filename=sprite_path,
                                           pic_width=enemy_data["SPRITE_SIZE"][0],
                                           pic_height=enemy_data["SPRITE_SIZE"][1])
                sprite_rect = pygame.Rect(enemy["POSITION"][0],
                                          enemy["POSITION"][1],
                                          enemy_data["SPRITE_SIZE"][0],
                                          enemy_data["SPRITE_SIZE"][1])
                # make sure to copy the stats dict otherwise all of the same type of enemy will share HP
                self.object_list.append(BattleObject(name=enemy["NAME"],
                                                     sprite_sheet=sprite_sheet,
                                                     sprite_rect=sprite_rect,
                                                     team=enemy["TEAM"],
                                                     stats=enemy_data["STATS"].copy(),
                                                     actions=enemy_data["ACTIONS"]))
            enemy_file.close()

        self.battle_box = self.build_battle_menu(left=self.screen_size[0]/2+self.screen_size[0]/4,
                                                 width=self.screen_size[0]/4 - 8)
        self.battle_picker = BattlePicker()
        self.battle_wheel = BattleWheel(actors=self.object_list,
                                        position=(120, 110),
                                        radius=100,
                                        background=self.menu_color)
        self.victory_box = self.build_text_box()
        self.xp_pool = 0

        self.current_actor = None
        self.player_teams = [0]
        self.state = "IDLE"
        self.start_turn()

    def build_text_box(self, left=4, top=10, height=50, color=(20, 30, 200)):
        return TextBox(box_bounds=pygame.Rect(left, top, self.screen_size[0] - left * 2, height),
                       text=[],
                       font_size=self.font_size,
                       color=color)

    def start_turn(self):
        print("\nSTARTING BATTLE LOOP\n--------------------")
        self.current_actor = self.battle_wheel.get_next()
        if self.current_actor.dead:
            print("CHAR is dead.")
            self.end_turn()
        elif self.current_actor.team in self.player_teams:
            self.show_action_menu()
        else:
            print("CPU {0} would go here...".format(self.current_actor.name))
            action = self.battle_actions[str(choice(self.current_actor.actions))]
            self.character_action(target=choice(self.get_targets(category=action["TARGET"])), override=action)

    def show_action_menu(self):
        # Turn off battle picker just to be safe
        self.battle_picker.off()
        for x in self.current_actor.actions:
            self.battle_box.options.append(self.battle_actions[str(x)])
        self.battle_box.open()
        self.state = "MENU"

    def end_turn(self):
        if self.current_actor.dead:
            self.battle_wheel.set_actor_time(10)
        else:
            self.current_actor.idle()
            self.battle_wheel.set_actor_time(5)
        if self.state != "VICTORY":
            self.start_turn()

    def end_battle(self):
        self.state = "END"
        self.victory_box.close()

    def character_action(self, target, override=None):
        self.state = "IDLE"
        self.battle_picker.off()
        if override:
            action = override
        else:
            print("GET ACTION; {0}".format(self.battle_box.get_action()))
            action = self.battle_box.get_action()
        self.current_actor.start_action(action=action, target=target)
        print("{0} did {1} to {2}".format(self.current_actor.name, action["NAME"], target.name))
        self.battle_box.reset()
        # self.end_turn()

    def get_targets(self, category="ENEMY"):
        targets = []
        for o in self.object_list:
            if category == "ENEMY" and o.team != self.current_actor.team and not o.dead:
                targets.append(o)
            elif category == "ALLY" and o.team == self.current_actor.team and not o.dead:
                targets.append(o)
            elif category == "ALL" and not o.dead:
                targets.append(o)
            elif category == "SELF":
                targets.append(self.current_actor)
                break
        return targets

    def choose_target(self, category="ENEMY"):
        self.battle_box.close()
        self.battle_picker.target_list = self.get_targets(category=category)
        self.battle_picker.visible = True
        self.state = "TARGET"

    def build_battle_menu(self, left=4, top=10, width=None, height=200,
                          color=(20, 30, 200)):
        if width is None:
            width = self.screen_size[0]/2 - 8
        return SelectBox(box_bounds=pygame.Rect(left, top, width, height), color=color, font_size=self.font_size)

    def update(self, screen):
        # check for deaths
        if self.state != "VICTORY" and self.state != "END":
            win = True
            for o in self.object_list:
                if self.current_actor.team != o.team and not o.dead:
                    win = False
            if win:
                self.victory_box.open(text=["YOU WON THIS YAY"])
                self.state = "VICTORY"
                self.end_turn()
            text = self.current_actor.act()
            if text:
                self.damage_numbers.append(text)
                self.end_turn()
        self.draw(screen=screen)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.foreground, (0, self.f_position))
        if self.object_list:
            for p in self.object_list:
                p.draw(screen)
        for t in self.damage_numbers:
            t.update()
            if t.alpha < 1:
                self.damage_numbers.remove(t)
            else:
                t.draw(screen=screen)

        self.battle_picker.draw(screen)

        # self.battle_wheel.draw(screen)
        self.battle_box.draw(screen)
        if self.victory_box:
            self.victory_box.draw(screen=screen)
