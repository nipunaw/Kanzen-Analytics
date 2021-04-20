import configparser
import os

class Shared_Info:
    def __init__(self):
        self.pending_updates_main = False
        self.pending_updates_export = False
        self.pending_updates_edit = False

        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

        self.color_graphs = config['SETTINGS']['color']
        self.time_scale = config['SETTINGS']['time_scale']
