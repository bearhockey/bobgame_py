import pygame

import src.battle.BattleFormula as Form
from src.FloatingText import FloatingText


class BattleObject(pygame.sprite.Sprite):
    def __init__(self, name, sprite_sheet, sprite_rect, flipped=False, team=0, stats=None, actions=None):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.team = team
        self.state_dict = {"ATTACK": 0,
                           "ATTACK2": 1,
                           "IDLE": 2,
                           "CAST": 3,
                           "DEFEND": 4,
                           "HURT": 5,
                           "DEAD": 6,
                           "WEAK": 7,
                           "MISC": 8,
                           "WALK": 9}
        self.sprite_sheet = sprite_sheet
        self.sprite_rect = sprite_rect

        self.animation_state = self.state_dict["IDLE"]
        self.flipped = flipped
        self.animation_delay = 5
        self.animating = False
        self.action = None
        self.target = None
        self.timer = 0

        # list of actions from battle_action.json (index values)
        self.actions = actions or []
        self.stats = stats or {}
        self.dead = False

    def set_position(self, x, y):
        self.sprite_rect.left = x
        self.sprite_rect.top = y

    def start_action(self, action, target):
        self.action = action
        self.target = target
        self.animating = True
        self.animation_state = self.state_dict[action["ACTION"]["TYPE"]]
        self.timer = 20

    def animate(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            self.animating = False

    def act(self):
        if self.animating:
            self.animate()
            return None
        elif self.action is not None:
            action = self.action
            self.action = None
            if action["ACTION"]["TYPE"] == "ATTACK":
                self.animation_state = self.state_dict["ATTACK"]
                # check if hits
                hits = Form.hit_check(accuracy=1,
                                      accuracy_stat=self.stats["DEX"],
                                      evade_stat=self.target.stats["DEX"],
                                      bonus=0)
                if hits > 0:
                    self.target.animation_state = self.state_dict["HURT"]
                    damage = Form.normal_damage(base_damage=action["ACTION"]["DAMAGE"],
                                                attack_stat=self.stats["STR"],
                                                defense_stat=self.target.stats["DEF"],
                                                bonus_attack=hits,
                                                bonus_defense=0)
                    self.target.damage(stat=action["ACTION"]["STAT"], damage=damage)
                    print("{0} took {1} damage and now has {2}/{3} HP!".format(self.target.name,
                                                                               action["ACTION"]["DAMAGE"],
                                                                               self.target.stats["HP_CURRENT"],
                                                                               self.target.stats["HP_MAX"]))
                else:
                    print("WHIFF!")
                    damage = "MISS"
                return FloatingText(text=str(damage), box_position=self.target.sprite_rect, color=(255, 255, 255))
            else:
                print("I don't know how to {0} yet...".format(action["ACTION"]["TYPE"]))
                return None

    def damage(self, stat="HP_CURRENT", damage=0):
        self.stats[stat] -= damage
        # check for death
        if self.stats["HP_CURRENT"] < 1:
            self.die()

    def idle(self):
        self.animation_state = self.state_dict["IDLE"]
        print("Going back to idle state")

    def die(self):
        self.stats["HP_CURRENT"] = 0
        self.dead = True
        self.animation_state = self.state_dict["DEAD"]

    def draw(self, screen):
        self.sprite_sheet.animate(screen,
                                  self.sprite_rect,
                                  self.animation_state,
                                  self.animation_delay,
                                  flipped=self.flipped)
