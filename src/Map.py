import json
import os
import pygame

from src.Actor import Actor
from src.ActionMap import ActionMap
from src.Door import Door
from src.MapObject import MapObject


class Map(object):
    def __init__(self, camera, directory, map_name="map.json", action_map="action_map.json"):
        # universal place for maps to be stored
        world_directory = os.path.join("..", "assets", "world")
        map_directory = os.path.join(world_directory, directory)

        self.name = "Hey"
        self.passmap = []
        self.actor_list = []
        self.object_list = []
        self.door_list = []
        with open(os.path.join(map_directory, map_name)) as data_file:
            self.map_data = json.load(data_file)
            data_file.close()

        self.tileset_data = {"name": self.map_data["tilesets"][0]["name"],
                             "image": self.map_data["tilesets"][0]["image"],
                             "width": self.map_data["tilesets"][0]["imagewidth"],
                             "height": self.map_data["tilesets"][0]["imageheight"],
                             "t_width": self.map_data["tilesets"][0]["tilewidth"],
                             "t_height": self.map_data["tilesets"][0]["tileheight"]
                             }
        self.map_tileset = pygame.image.load(os.path.join(map_directory, self.tileset_data["image"]))
        self.map_size = (self.map_data["width"] * self.map_data["tilewidth"],
                         self.map_data["height"] * self.map_data["tileheight"])
        self.trans_color = (255, 0, 255)

        if action_map:
            self.action_map = ActionMap(action_file=os.path.join(map_directory, action_map), camera=camera)
        else:
            self.action_map = None

        self.starting_location = None

        self.lower_map = pygame.Surface(self.map_size)
        self.upper_map = pygame.Surface(self.map_size)
        self.upper_map.fill(self.trans_color)
        self.upper_map.set_colorkey(self.trans_color)
        self.build_map()

        if "properties" in self.map_data:
            if "AUTO" in self.map_data["properties"]:
                camera.controller.trigger_action(action_map=self.action_map,
                                                 action_id=self.map_data["properties"]["AUTO"])

        # debug prints
        # print(self.map_data["tilesets"][0]["image"])
        # print("Map size {0}".format(self.map_size))

    def draw(self, screen, passmap=False):
        screen.blit(self.lower_map, (0, 0))
        if passmap:
            for block in self.passmap:
                pygame.draw.rect(screen, (255, 255, 255), block)
        for o in self.object_list:
            o.draw(screen, self.map_tileset)
        for a in self.actor_list:
            a.draw(screen)

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
                        elif "ACTOR" in o["properties"]:
                            print("FOUND ONE")
                            self.actor_list.append(Actor(o))
                        else:
                            self.object_list.append(MapObject(o, self.tileset_data))
