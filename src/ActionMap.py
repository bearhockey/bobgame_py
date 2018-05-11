import json


class ActionMap(object):
    def __init__(self, action_file, camera):
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
        return self.action_map[action_id]["type"]

    def get_next_action(self, action_id):
        return self.action_map[action_id]["next"]

    def trigger_action(self, action_id):
        if action_id:
            action_type = self.get_action_type(action_id)
            action = self.action_map[action_id]
            if action_type == "text":
                self.action_text_box(action)
                return None
            elif action_type == "WAIT":
                return self.action_wait(action)
            elif action_type == "battle":
                return self.action_battle(action)
            elif action_type == "MOVE":
                return self.action_move(action)
            else:
                print("Unknown action type '{0}' parsed from action map ID {1}".format(action_type, action_id))

    def action_text_box(self, text_box_data):
        if "portrait" in text_box_data:
            portrait = text_box_data["portrait"]
        else:
            portrait = None

        self.text_box.open(text=text_box_data["TEXT"], portrait=portrait)

    def action_wait(self, action_data):
        if "TIME" in action_data:
            print("Waiting for things: {0}".format(action_data["TIME"] * 60))
            self.camera.controller.delay_timer += action_data["TIME"] * 60

    def action_battle(self, action_data):
        if "battle" in action_data:
            self.camera.in_battle = True

    def action_move(self, action_data):
        if action_data["TARGET"] == "PLAYER":
            target = self.camera.player
        else:
            target = None
            print("I DUNNO")
        if action_data["DESTINATION"] == "RELATIVE":
            target.set_relative_destination(x=action_data["POSITION"][0], y=action_data["POSITION"][1])
            target.acting = True
