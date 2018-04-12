import pygame


class Door(object):
    def __init__(self, door_json):
        self.door = pygame.Rect(door_json['x'], door_json['y'], door_json["width"], door_json["height"])
        self.destination_map = None
        self.destination_cords = None
        properties = door_json["properties"]
        self.set_destination(properties["door"], properties['x'], properties['y'])

    def set_destination(self, url, x, y):
        self.destination_map = url
        self.destination_cords = (x, y)
