import pygame

from src.Box import Box


class Menu(Box):
    def __init__(self, screen_size, actor_list, color=None):
        border_gap = 50
        box_size = pygame.Rect(border_gap, border_gap, screen_size[0] - border_gap * 2, screen_size[1] - border_gap * 2)
        Box.__init__(self, box_size, color)

        self.actor_list = actor_list

        self.options = Box(box_bounds=pygame.Rect((box_size.width/3)*2,
                                                  box_size.top + border_gap,
                                                  box_size.width/3 - border_gap,
                                                  box_size.height-border_gap*2 - border_gap),
                           color=color)
        self.options.open()

    def draw(self, screen):
        self.overlay.fill(self.color)
        self.options.draw(self.overlay)
        for actor in self.actor_list:
            self.draw_profile(character=actor, color=(80, 80, 250))
        Box.draw(self, screen)

    def draw_profile(self, character, color=None):
        profile = pygame.Surface((500, 200))
        if color:
            profile.fill(color)
        else:
            profile.fill(self.color)
        if character.portrait:
            profile.blit(character.portrait, (10, 10))
        p_size = 150
        profile.blit(self.font.render(str(character.battle_object.stats["HP_MAX"]), True, self.white), (200, 20))
        self.overlay.blit(profile, (20, 20))
