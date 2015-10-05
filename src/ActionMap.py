import json
from time import sleep


class ActionMap(object):
    def __init__(self, action_file, text_box):
        # grab the action map
        with open(action_file) as data_file:
            self.action_map = json.load(data_file)
            data_file.close()
        self.tbox = text_box

    def get_action(self, action_id):
        return self.action_map[action_id]

    def get_action_type(self, action_id):
        return self.action_map[action_id]['type']

    def get_next_action(self, action_id):
        return self.action_map[action_id]['next']

    def trigger_action(self, action_id):
        if action_id:
            action_type = self.get_action_type(action_id)
            if action_type == 'text':
                self.action_text_box(self.action_map[action_id])
            elif action_type == 'wait':
                self.action_wait(self.action_map[action_id])

    def action_text_box(self, text_box_data):
        if 'line_1' in text_box_data:
            line_1 = text_box_data['line_1']
        else:
            line_1 = None

        if 'line_2' in text_box_data:
            line_2 = text_box_data['line_2']
        else:
            line_2 = None

        if 'line_3' in text_box_data:
            line_3 = text_box_data['line_3']
        else:
            line_3 = None

        text_lines = (line_1, line_2, line_3)

        if 'portrait' in text_box_data:
            portrait = text_box_data['portrait']
        else:
            portrait = None

        self.tbox.open(text=text_lines, portrait=portrait)
        print 'This would be a text box if I had one'

    def action_wait(self, action_data):
        if 'time' in action_data:
            print 'Waiting for things'
            sleep(action_data['time'])
