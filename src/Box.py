import pygame


class Box(pygame.sprite.Sprite):
    def __init__(self, box_bounds, color=None):
        pygame.sprite.Sprite.__init__(self)

        self.font_size = 24
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
        self.white = (255, 255, 255)

        self.visible = False
        self.box = box_bounds
        self.border = 3
        self.space = self.border * 8
        self.inner_box = pygame.Rect(self.box.left + self.border, self.box.top + self.border,
                                     self.box.width - self.border * 2,
                                     self.box.height - self.border * 2)
        self.color = color

    def draw(self, screen):
        if self.visible:
            screen.fill(self.white, self.box)
            screen.fill(self.color, self.inner_box)

    def open(self, color=None):
        if color:
            self.color = color
        self.visible = True

    def close(self):
        self.visible = False
