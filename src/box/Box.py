import pygame
import os


class Box(pygame.sprite.Sprite):
    def __init__(self, box_bounds, color=None, cursor=None, font_size=None):
        pygame.sprite.Sprite.__init__(self)

        self.font_size = font_size or 24
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
        self.white = (255, 255, 255)

        self.visible = False
        self.underlay = pygame.Surface((box_bounds.width, box_bounds.height))
        self.box = box_bounds
        self.border = 3
        self.space = self.border * 8
        self.inner_box = pygame.Rect(self.border,
                                     self.border,
                                     self.box.width - self.border * 2,
                                     self.box.height - self.border * 2)
        self.overlay = pygame.Surface((self.inner_box.width, self.inner_box.height))
        self.color = color
        if cursor:
            self.cursor = cursor
        else:
            cursor_location = os.path.normpath("../assets/cursor.png")
            self.cursor = pygame.image.load(cursor_location).convert_alpha()
        self.cursor_offset = 32

        self.underlay.fill(self.white)
        self.underlay.fill(self.color, self.inner_box)

    def draw(self, screen):
        if self.visible:
            self.underlay.blit(self.overlay, self.inner_box)
            screen.blit(self.underlay, (self.box.left, self.box.top))
            # screen.blit(self.overlay, (self.box.left, self.box.top))

    def open(self, color=None):
        if color:
            self.color = color
        self.visible = True

    def close(self):
        self.visible = False
