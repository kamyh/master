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
        test = self.config.get('TEST', 'val1')
        print(test)

    def get_path_to_core(self):
        return self.config.get('ENV', 'path_to_core')

    def get_temp_file_p_seqs(self):
        return self.config.get('ENV', 'temp_file_pseqs')

    def get_grades_file_pseqs(self):
        return self.config.get('ENV', 'grades_file_pseqs')

    def get_ds_file_save(self):
        return self.config.get('ENV', 'ds_file_save')

    def get_detailed_logs(self):
        return self.config.get('INFORMATION', 'detailed_logs') == '1'

    def is_testing(self):
        return self.config.get('INFORMATION', 'testing') == '1'

    def verbose(self):
        return self.config.get('INFORMATION', 'verbose') == '1'

    def is_reset_db_at_start(self):
        return self.config.get('ENV', 'reset_db_at_start') == '1'

    def get_nbr_process(self):
        return self.config.get('ENV', 'process')

    def get_chunk_size_multiplier(self):
        return int(self.config.get('ENV', 'chunk_size_multiplier'))

    # E-VALUE
    def is_use_e_value_selection(self):
        return self.config.get('DOMS_SELECTION', 'use_e_value_selection') == '1'

    def get_min_e_value(self):
        return int(self.config.get('DOMS_SELECTION', 'min_e_value'))

    def get_max_e_value(self):
        return int(self.config.get('DOMS_SELECTION', 'max_e_value'))

    # SCORE
    def is_use_score_selection(self):
        return self.config.get('DOMS_SELECTION', 'use_score_selection') == '1'

    def get_min_score(self):
        return int(self.config.get('DOMS_SELECTION', 'min_score'))

    def get_max_score(self):
        return int(self.config.get('DOMS_SELECTION', 'max_score'))

    # BIAIS
    def is_use_biais_selection(self):
        return self.config.get('DOMS_SELECTION', 'use_biais_selection') == '1'

    def get_min_biais(self):
        return int(self.config.get('DOMS_SELECTION', 'min_biais'))

    def get_max_biais(self):
        return int(self.config.get('DOMS_SELECTION', 'max_biais'))

    def normalisation(self):
        return int(self.config.get('DATASET_GENERATION', 'normalisation'))
