import pygame


class TextBox(pygame.sprite.Sprite):
    def __init__(self, box_bounds, text, color=None, picture=None):
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
        self.text = text
        self.portrait = picture
        self.color = color

        self.choice = False
        self.choice_box = pygame.Rect(self.box.right - self.box.width / 3 - 10, self.box.top - 100,
                                      self.box.width / 3, self.font_size * 2 + self.space * 3)
        self.choice_inner_box = pygame.Rect(self.choice_box.left + self.border, self.choice_box.top + self.border,
                                            self.choice_box.width - self.border * 2,
                                            self.choice_box.height - self.border * 2)

    def draw(self, screen):
        if self.visible:
            if self.portrait:
                portrait_offset = 150 + self.space
            else:
                portrait_offset = 0

            screen.fill(self.white, self.box)
            screen.fill(self.color, self.inner_box)
            if self.portrait:
                screen.blit(self.portrait, (self.inner_box.left + self.space,
                                            self.inner_box.top + (self.inner_box.height - 150) / 2))
            screen.blit(self.font.render(self.text, True, self.white),
                        (portrait_offset + self.inner_box.left + self.space,
                         self.inner_box.top + (self.inner_box.height - 150) / 2))
            if self.choice:
                screen.fill(self.white, self.choice_box)
                screen.fill(self.color, self.choice_inner_box)
                screen.blit(self.font.render('Yes', True, self.white),
                            (self.choice_inner_box.left + self.space,
                            self.choice_inner_box.top + self.space))
                screen.blit(self.font.render('No', True, self.white),
                            (self.choice_inner_box.left + self.space,
                            self.choice_inner_box.top + self.space * 2 + self.font_size))

    def open(self, text=None, portrait=None, color=None, choice=None):
        if text:
            self.text = text
        if portrait:
            self.portrait = portrait
        if color:
            self.color = color
        if choice:
            self.choice = choice

        self.visible = True

    def close(self):
        self.visible = False
        self.portrait = None
        self.text = None
