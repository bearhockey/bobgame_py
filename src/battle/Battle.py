import json
import os
import pygame

from src.box.SelectBox import SelectBox
from src.battle.BattleObject import BattleObject
from src.battle.BattlePicker import BattlePicker
from src.battle.BattleWheel import BattleWheel
from src.SpriteSheet import SpriteSheet
from src.FloatingText import FloatingText


class Battle (object):
    def __init__(self, screen_size, battle_info, player):
        # grab list of battle actions (gonna be a lot; maybe trim this down somehow?)
        real_url = os.path.join("..", "assets", "data", "battle_action.json")
        with open(real_url) as data_file:
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
        self.background = pygame.image.load(os.path.join("..", "assets", "background", battle_info["background"]))
        self.foreground = pygame.image.load(os.path.join("..", "assets", "battleground", battle_info["foreground"]))
        self.f_position = self.screen_size[1]/2

        # load players
        self.object_list.append(player.battle_object)
        # load enemies
        with open(os.path.join("..", "assets", "data", "enemy_map.json")) as enemy_file:
            enemy_list = json.load(enemy_file)
            enemy_file.close()
            for enemy in battle_info["enemies"]:
                enemy_data = enemy_list[enemy["entity"]]
                sprite_path = os.path.join("..", "assets", "battle", enemy_data["sprite_sheet"])
                sprite_sheet = SpriteSheet(filename=sprite_path,
                                           pic_width=enemy_data["sprite_size"][0],
                                           pic_height=enemy_data["sprite_size"][1])
                sprite_rect = pygame.Rect(enemy["position"][0],
                                          enemy["position"][1],
                                          enemy_data["sprite_size"][0],
                                          enemy_data["sprite_size"][1])
                # make sure to copy the stats dict otherwise all of the same type of enemy will share HP
                self.object_list.append(BattleObject(name=enemy["name"],
                                                     sprite_sheet=sprite_sheet,
                                                     sprite_rect=sprite_rect,
                                                     team=enemy["team"],
                                                     stats=enemy_data["stats"].copy()))
            enemy_file.close()

        self.battle_box = self.build_battle_menu(left=self.screen_size[0]/2+self.screen_size[0]/4,
                                                 width=self.screen_size[0]/4 - 8)
        self.battle_picker = BattlePicker()

        self.battle_wheel = BattleWheel(actors=self.object_list,
                                        position=(120, 110),
                                        radius=100,
                                        background=self.menu_color)

        self.current_actor = None
        self.player_teams = [0]
        self.state = "IDLE"
        self.start_turn()

    def start_turn(self):
        print("\nSTARTING BATTLE LOOP\n--------------------")
        self.current_actor = self.battle_wheel.get_next()
        # check if enemies are all defeated
        win = True
        for o in self.object_list:
            if self.current_actor.team != o.team and not o.dead:
                win = False
        if win:
            print("YOU DID GOOD")
            self.state = "END"
        elif self.current_actor.dead:
            print("CHAR is dead.")
            self.end_turn()
        elif self.current_actor.team in self.player_teams:
            self.show_action_menu()
        else:
            print("CPU {0} would go here...".format(self.current_actor.name))
            self.end_turn()

    def show_action_menu(self):
        # Turn off battle picker just to be safe
        self.battle_picker.off()
        for x in self.current_actor.actions:
            self.battle_box.options.append(self.battle_actions[str(x)])
        self.battle_box.open()
        self.state = "MENU"

    def end_turn(self):
        if self.current_actor.dead:
            self.current_actor.die()
            self.battle_wheel.set_actor_time(-1)
        else:
            self.current_actor.idle()
            self.battle_wheel.set_actor_time(5)
        self.start_turn()

    def character_action(self, target):
        self.state = "IDLE"
        self.battle_picker.off()
        text = self.current_actor.act(action=self.battle_box.get_action(), target=target)
        if text:
            self.damage_numbers.append(text)
        print("{0} did {1} to {2}".format(self.current_actor.name, self.battle_box.get_action()["NAME"], target.name))
        self.battle_box.reset()
        self.end_turn()

    def choose_target(self, category="ENEMY"):
        self.battle_box.close()
        target_list = []
        for o in self.object_list:
            if category == "ENEMY" and o.team != self.current_actor.team:
                target_list.append(o)
            elif category == "ALLY" and o.team == self.current_actor.team:
                target_list.append(o)
            elif category == "ALL":
                target_list.append(o)
            elif category == "SELF":
                target_list.append(self.current_actor)
                break
        self.battle_picker.target_list = target_list
        self.battle_picker.visible = True
        self.state = "TARGET"

    def build_battle_menu(self, left=4, top=10, width=None, height=200,
                          color=(20, 30, 200)):
        if width is None:
            width = self.screen_size[0]/2 - 8
        return SelectBox(pygame.Rect(left, top, width, height), color=color)

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

        self.battle_wheel.draw(screen)
        self.battle_box.draw(screen)
