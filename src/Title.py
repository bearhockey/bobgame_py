from src.box.SelectBox import SelectBox


class Title(object):
    def __init__(self, screen_size, font_size):
        s_width, s_height = screen_size
        self.options = SelectBox(position=(s_width/2-140/2, s_height/2),
                                 box_size=(140, 35),
                                 color=(20, 40, 200),
                                 pressed_color=(40, 60, 220),
                                 font_size=font_size,
                                 options=[{"TEXT": "NEW GAME", "ACT": "NEW"},
                                          {"TEXT": "LOAD GAME", "ACT": "LOAD"},
                                          {"TEXT": "EXIT GAME", "ACT": "EXIT"}
                                          ]
                                 )

    def draw(self, screen):
        self.options.draw(screen=screen)
