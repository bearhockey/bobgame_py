import json


class ActionMap(object):
    def __init__(self, action_file, text_box):
        # grab the action map
        with open(action_file) as data_file:
            self.action_map = json.load(data_file)
            data_file.close()
        self.tbox = text_box

    def trigger_action(self, action_id):
        if action_id:
            action_type = self.action_map[action_id]['type']
            if action_type == 'text':
                self.action_text_box(self.action_map[action_id])

    def action_text_box(self, text_box_data):
        if 'line_1' in text_box_data:
            line_1 = text_box_data['line_1']
        else:
            line_1 = None

        self.tbox.open(text=line_1)
        print 'This would be a text box if I had one'
