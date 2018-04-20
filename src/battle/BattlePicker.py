import pygame


class BattlePicker(object):
    def __init__(self):
        self.target_list = []
        self.position = 0
        self.visible = False
        self.line_width = 2

    def draw(self, screen):
        if self.visible:
            if self.target_list:
                target = self.target_list[self.position]
                box = target.sprite_rect
                pygame.draw.rect(screen,
                                 (0, 0, 0),
                                 pygame.Rect(box.left+self.line_width,
                                             box.top+self.line_width,
                                             box.width,
                                             box.height),
                                 self.line_width )
                pygame.draw.rect(screen, (255, 255, 255), box, self.line_width)

    def get_target(self):
        return self.target_list[self.position]

    def off(self):
        self.visible = False
        self.position = 0

    def cursor_up(self):
        if self.position < len(self.target_list)-1:
            self.position += 1
        else:
            self.position = 0

    def cursor_down(self):
        if self.position > 0:
            self.position -= 1
        else:
            self.position = len(self.target_list)-1
