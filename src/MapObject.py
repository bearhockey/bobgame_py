import pygame


class MapObject(object):
    def __init__(self, object_json, tileset_info):
        self.name = "You"
        self.data = object_json
        self.properties = self.data["properties"]

        self.tile_set_data = tileset_info
        x = (self.data["gid"] - 1) % (self.tile_set_data["width"] / self.tile_set_data["t_width"])
        x = x * self.tile_set_data["t_width"]
        y = (self.data["gid"] - 1) / self.tile_set_data["t_width"]
        y = y * self.tile_set_data["t_height"]
        self.tileset_rect = pygame.Rect(x, y, self.data["width"], self.data["height"])

        self.position = pygame.Rect(self.data['x'], self.data['y'], self.data["width"], self.data["height"])

    def draw(self, screen, tileset_image):
        screen.blit(tileset_image, self.position, area=self.tileset_rect)

    def turn_to_face(self, direction):
        # if the object should turn to face something, it goes here (so far, nope)
        pass

    def action(self):
        if "ACTION" in self.properties:
            return self.properties["ACTION"]
        else:
            return None
