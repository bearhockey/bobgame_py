import json
import os
import pygame

from src.Door import Door
from src.MapObject import MapObject


class Map(object):
    def __init__(self, map_file, text_box=None):
        self.name = "Hey"
        self.passmap = []
        self.object_list = []
        self.door_list = []
        with open(map_file) as data_file:
            self.map_data = json.load(data_file)
            data_file.close()
        print(self.map_data["tilesets"][0]["image"])
        self.tileset_data = {"name": self.map_data["tilesets"][0]["name"],
                             "image": self.map_data["tilesets"][0]["image"],
                             "width": self.map_data["tilesets"][0]["imagewidth"],
                             "height": self.map_data["tilesets"][0]["imageheight"],
                             "t_width": self.map_data["tilesets"][0]["tilewidth"],
                             "t_height": self.map_data["tilesets"][0]["tileheight"]
                             }
        self.map_location = "../assets/world/"
        self.map_tileset = pygame.image.load(os.path.normpath('{0}{1}'.format(self.map_location,
                                                                              self.tileset_data["image"])))
        self.map_size = (self.map_data["width"] * self.map_data["tilewidth"],
                         self.map_data["height"] * self.map_data["tileheight"])
        print("Map size {0}".format(self.map_size))

        self.trans_color = (255, 0, 255)

        self.starting_location = None

        self.lower_map = pygame.Surface(self.map_size)
        self.upper_map = pygame.Surface(self.map_size)
        self.upper_map.fill(self.trans_color)
        self.upper_map.set_colorkey(self.trans_color)
        self.build_map()

    def draw(self, screen, passmap=False):
        screen.blit(self.lower_map, (0, 0))
        if passmap:
            for block in self.passmap:
                pygame.draw.rect(screen, (255, 255, 255), block)
        for o in self.object_list:
            o.draw(screen, self.map_tileset)

    def draw_upper(self, screen):
        screen.blit(self.upper_map, (0, 0))

    def build_map(self):
        for layer in self.map_data["layers"]:
            if layer["visible"]:
                if layer["type"] == "tilelayer":
                    pos = 0
                    t_width = self.map_data["tilesets"][0]["tilewidth"]
                    t_height = self.map_data["tilesets"][0]["tileheight"]
                    for i in layer["data"]:
                        if i != 0:
                            y_cord = int(pos / layer["width"])
                            x_cord = int(pos % layer["width"])

                            if layer["name"] == "passmap":
                                self.passmap.append(pygame.Rect(x_cord * t_width, y_cord * t_height, t_width, t_height))
                            else:
                                tile_x = (i - 1) % (self.map_data["tilesets"][0]["imagewidth"] / t_width)
                                tile_x = tile_x * t_width
                                tile_y = (i - 1) / (self.map_data["tilesets"][0]["imagewidth"] / t_height)
                                # need to figure out what the -4 is from
                                tile_y = tile_y * t_height - 4

                                if "properties" in layer \
                                        and "upper" in layer["properties"] \
                                        and layer["properties"]["upper"]:
                                    map_to_draw = self.upper_map
                                else:
                                    map_to_draw = self.lower_map

                                map_to_draw.blit(self.map_tileset, (x_cord * t_width, y_cord * t_height),
                                                 area=pygame.Rect(tile_x, tile_y,
                                                                  self.map_data["tilesets"][0]["tilewidth"],
                                                                  self.map_data["tilesets"][0]["tileheight"]))
                        pos += 1
                elif layer["type"] == "objectgroup":
                    for o in layer["objects"]:
                        if "door" in o["properties"]:
                            self.door_list.append(Door(o))
                        elif "start" in o["properties"]:
                            self.starting_location = (o['x'], o['y'])
                            print("Starting location is {0}".format(self.starting_location))
                        else:
                            self.object_list.append(MapObject(o, self.tileset_data))
