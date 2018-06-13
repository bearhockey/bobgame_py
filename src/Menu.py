import pygame

from src.box.Box import Box
from src.box.SelectBox import SelectBox


class Menu(Box):
    def __init__(self, screen_size, actor_list, color=None, font_size=None):
        self.border_gap = border_gap = 5
        box_size = pygame.Rect(border_gap, border_gap, screen_size[0] - border_gap * 2, screen_size[1] - border_gap * 2)
        Box.__init__(self, box_bounds=box_size, color=color, font_size=font_size)

        self.actor_list = actor_list

        self.profile_dimensions = (box_size.width*(2/5)-border_gap*2, 160)

        self.options = SelectBox(box_bounds=pygame.Rect((box_size.width/5)*4 + border_gap,
                                                        box_size.top + border_gap,
                                                        box_size.width/5 - border_gap*4,
                                                        box_size.height-border_gap*5),
                                 color=(80, 80, 150),
                                 font_size=font_size)
        self.options.options = [{"NAME": "Stats", "ACT": "PASS"},
                                {"NAME": "Order", "ACT": "PASS"},
                                {"NAME": "Items", "ACT": "PASS"},
                                {"NAME": "Save", "ACT": "SAVE"},
                                {"NAME": "Exit", "ACT": "EXIT"}]
        self.options.open()

    def act(self, action, camera):
        if action["ACT"] == "EXIT":
            camera.exit()
        elif action["ACT"] == "SAVE":
            camera.save_game()
            camera.close_menu()
        else:
            print("Something: {0}".format(action["NAME"]))

    def draw(self, screen):
        self.overlay.fill(self.color)
        self.options.draw(self.overlay)
        slot = 0
        for actor in self.actor_list:
            self.draw_profile(character=actor, slot=[slot % 2, int(slot / 2)], color=(80, 80, 250))
            slot += 1
        Box.draw(self, screen)

    def draw_profile(self, character, slot, color=None):
        stats = character.battle_object.stats
        profile = pygame.Surface(self.profile_dimensions)
        if color:
            profile.fill(color)
        else:
            profile.fill(self.color)
        if character.portrait:
            profile.blit(character.portrait, (5, 5))
        p_size = 150
        strings = [character.battle_object.name,
                   "HP: {0}/{1}".format(stats["HP_CURRENT"], stats["HP_MAX"]),
                   "STR: {0}".format(stats["STR"]),
                   "DEF: {0}".format(stats["DEF"])]
        for text in strings:
            profile.blit(self.font.render(text, True, self.white), (p_size+50, strings.index(text)*30+15))
        x = slot[0] * self.profile_dimensions[0] + slot[0] * self.border_gap
        y = slot[1] * self.profile_dimensions[1]
        self.overlay.blit(profile, (self.border_gap + x, self.border_gap + y))
