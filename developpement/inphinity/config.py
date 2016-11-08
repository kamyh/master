##
#   Created by: Deruaz Vincent
#   wrapper of configuration
#   13.10.2016
##

import ConfigParser

class Config:
    def __init__(self, filename):
        self.config = ConfigParser.ConfigParser()
        self.config.read(filename)

    def check_config(self):
        pass

    def create_default_config(self):
        pass

    def load_config(self):
        for section in self.config.sections():
            print section


    #Doesn't Working
    def load_config_test(self):
        self.config.sections()
        test = self.config.get('TEST','val1')
        print test