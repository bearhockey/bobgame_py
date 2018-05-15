import json
from os import path


class ActionMap(object):
    def __init__(self, action_file, camera):
        self.portrait_dir = path.join("..", "assets", "portraits")
        self.background_dir = path.join("..", "assets", "background")
        # grab the action map
        try:
            with open(action_file) as data_file:
                self.action_map = json.load(data_file)
                data_file.close()
        except FileNotFoundError:
            print("Not loading this action map: {0}".format(action_file))
        self.camera = camera
        self.text_box = self.camera.text_box

    def get_action(self, action_id):
        return self.action_map[action_id]

    def get_action_type(self, action_id):
        return self.action_map[action_id]["TYPE"]

    def get_next_action(self, action_id):
        return self.action_map[action_id]["NEXT"]

    def trigger_action(self, action_id):
        if action_id:
            action_type = self.get_action_type(action_id)
            action = self.action_map[action_id]
            # handle flags first
            if "SET_FLAG" in action:
                flag = action["SET_FLAG"]
                self.camera.flags[flag[0]] = flag[1]
                print("FLAG {0} set to {1}".format(flag[0], flag[1]))
            if action_type == "TEXT":
                self.action_text_box(action)
                return None
            elif action_type == "WAIT":
                return self.action_wait(action)
            elif action_type == "BATTLE":
                return self.action_battle(action)
            elif action_type == "MOVE":
                return self.action_move(action)
            elif action_type == "CHECK":
                pass
            elif action_type == "ADD":
                return self.action_add(action)
            else:
                print("Unknown action type '{0}' parsed from action map ID {1}".format(action_type, action_id))

    def action_text_box(self, text_box_data):
        if "PORTRAIT" in text_box_data:
            portrait = path.join(self.portrait_dir, text_box_data["PORTRAIT"])
        else:
            portrait = None
        if "BACKGROUND" in text_box_data:
            background = path.join(self.background_dir, text_box_data["BACKGROUND"])
        else:
            background = None
        self.text_box.open(text=text_box_data["TEXT"], portrait=portrait, background=background)

    def action_add(self, action_data):
        if "HERO" in action_data:
            hero = {"DATA": action_data["HERO"],
                    "NAME": None,
                    "STATS": None}
            self.camera.add_hero(hero_data=hero)

    def action_wait(self, action_data):
        if "TIME" in action_data:
            print("Waiting for things: {0}".format(action_data["TIME"] * 60))
            self.camera.controller.delay_timer += action_data["TIME"] * 60

    def action_battle(self, action_data):
        if "BATTLE" in action_data:
            battle_index = action_data["BATTLE"]
            self.camera.start_battle(battle_index=battle_index)

    def action_move(self, action_data):
        if action_data["TARGET"] == "PLAYER":
            target = self.camera.player
        else:
            target = None
            print("I DUNNO")
        if action_data["DESTINATION"] == "RELATIVE":
            if "DIRECTION" in action_data:
                target.direction = action_data["DIRECTION"]
            target.set_relative_destination(x=action_data["POSITION"][0], y=action_data["POSITION"][1])
            target.acting = True
