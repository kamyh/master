##
#   Created by: Deruaz Vincent
#   wrapper of configuration
#   13.10.2016
##

import configparser

class Config:
    def __init__(self, filename):
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    def check_config(self):
        pass

    def create_default_config(self):
        pass

    def load_config(self):
        for section in self.config.sections():
            print(section)


    def load_config_test(self):
        self.config.sections()
        test = self.config.get('TEST','val1')
        print(test)

    def get_path_to_core(self):
        return self.config.get('ENV','path_to_core')

    def get_temp_file_p_seqs(self):
        return self.config.get('ENV','temp_file_pseqs')

    def get_detailed_logs(self):
        return self.config.get('ENV','detailed_logs')

