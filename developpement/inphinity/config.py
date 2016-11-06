##
#   Created by: Deruaz Vincent
#   wrapper of configuration
#   13.10.2016
##

import ConfigParser

class Config:
    def __init__(self):
        self.Config = ConfigParser.ConfigParser()
        self.Config.read("./default.ini")
        print self.Config.sections()

    def check_config(self):
        pass

    def create_default_config(self):
        pass

    def load_config(self):
        pass

    #Doesn't Working
    def load_config_test(self):
        test = ConfigSectionMap("test")['val1']
        print test