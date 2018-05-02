import pygame

from src.box.Box import Box


class TextBox(Box):
    def __init__(self, box_bounds, text=None, color=None, picture=None):
        Box.__init__(self, box_bounds, color)

        self.text = text
        self.portrait_url = picture
        self.portrait = None

        self.choice = False
        self.choice_box = pygame.Rect(self.box.right - self.box.width / 3 - 10, self.box.top - 100,
                                      self.box.width / 3, self.font_size * 2 + self.space * 3)
        self.choice_inner_box = pygame.Rect(self.choice_box.left + self.border, self.choice_box.top + self.border,
                                            self.choice_box.width - self.border * 2,
                                            self.choice_box.height - self.border * 2)

    def draw(self, screen):
        if self.visible:
            self.overlay.fill(self.color)
            if self.portrait_url:
                portrait_offset = 150 + self.space
                if not self.portrait:
                    self.portrait = pygame.image.load("..\\assets\\portraits\\{0}".
                                                      format(self.portrait_url)).convert_alpha()
            else:
                portrait_offset = 0

            if self.portrait:
                self.overlay.blit(self.portrait, (self.space, (self.inner_box.height - 150) / 2))
            # line 1
            self.overlay.blit(self.font.render(self.text[0], True, self.white),
                              (portrait_offset + self.space, (self.inner_box.height - 150) / 2))
            # line 2
            self.overlay.blit(self.font.render(self.text[1], True, self.white),
                              (portrait_offset + self.space, (self.inner_box.height - 150) / 2 + self.font_size * 1.2))
            # line 3
            self.overlay.blit(self.font.render(self.text[2], True, self.white),
                              (portrait_offset + self.space, (self.inner_box.height - 150) / 2 + self.font_size * 2.4))
            if self.choice:
                self.overlay.fill(self.white, self.choice_box)
                self.overlay.fill(self.color, self.choice_inner_box)
                self.overlay.blit(self.font.render("Yes", True, self.white),
                                  (self.choice_inner_box.left + self.space,
                                   self.choice_inner_box.top + self.space))
                self.overlay.blit(self.font.render("No", True, self.white),
                                  (self.choice_inner_box.left + self.space,
                                   self.choice_inner_box.top + self.space * 2 + self.font_size))

            Box.draw(self, screen)

    def open(self, text=None, portrait=None, color=None, choice=None):
        if text:
            self.text = text
        if portrait:
            self.portrait_url = portrait
        if choice:
            self.choice = choice
        Box.open(self, color)

    def close(self):
        self.portrait_url = None
        self.portrait = None
        self.text = None
        Box.close(self)
