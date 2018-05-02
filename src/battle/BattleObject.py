import pygame

from src.FloatingText import FloatingText


class BattleObject(pygame.sprite.Sprite):
    def __init__(self, name, sprite_sheet, sprite_rect, flipped=False, team=0, stats=None):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.team = team
        self.state_dict = {"attack": 0,
                           "attack2": 1,
                           "idle": 2,
                           "cast": 3,
                           "defend": 4,
                           "hurt": 5,
                           "dead": 6,
                           "weak": 7,
                           "misc": 8,
                           "walk": 9}
        self.sprite_sheet = sprite_sheet
        self.sprite_rect = sprite_rect

        self.animation_state = self.state_dict["idle"]
        self.flipped = flipped
        self.animation_delay = 5

        # list of actions from battle_action.json (index values)
        self.actions = ['0', '1', '2', '3', '4']
        self.stats = stats or {}
        self.dead = False

    def act(self, action, target):
        if action["ACTION"]["TYPE"] == "ATTACK":
            self.animation_state = self.state_dict["attack"]
            print("Attacking {0}!".format(target.name))
            target.animation_state = self.state_dict["hurt"]
            damage = action["ACTION"]["DAMAGE"]
            target.damage(stat=action["ACTION"]["STAT"], damage=damage)
            print("{0} took {1} damage and now hags {2}/{3} HP!".format(target.name,
                                                                        action["ACTION"]["DAMAGE"],
                                                                        target.stats["HP_CURRENT"],
                                                                        target.stats["HP_MAX"]))
            return FloatingText(text=str(damage), box_position=target.sprite_rect, color=(255, 255, 255))
        else:
            print("I don't know how to {0} yet...".format(action["ACTION"]["TYPE"]))
            return None

    def damage(self, stat="HP_CURRENT", damage=0):
        self.stats[stat] -= damage
        # check for death
        if self.stats["HP_CURRENT"] < 1:
            self.dead = True

    def idle(self):
        self.animation_state = self.state_dict["idle"]
        print("Going back to idle state")

    def die(self):
        self.animation_state = self.state_dict["dead"]

    def draw(self, screen):
        self.sprite_sheet.animate(screen,
                                  self.sprite_rect,
                                  self.animation_state,
                                  self.animation_delay,
                                  flipped=self.flipped)
