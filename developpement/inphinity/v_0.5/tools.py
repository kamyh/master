from config import Config
from toolsIo import ToolsIO
from database_utilities import DBUtilties

class Tools():
    def __init__(self, path_to_config):
        self.configuration = Config(path_to_config)
        self.db = DBUtilties(self.configuration)
        self.io = ToolsIO()

    def get_configuration(self):
        return self.configuration

    def stop_app(self):
        import sys
        sys.exit()