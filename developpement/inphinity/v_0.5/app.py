##
#   Created by: Deruaz Vincent
#   10.01.2017
##

from tools import Tools

from core import Core
from Bio import *

import glob, os

if __name__ == '__main__':
    print('Run Test: test_10012017_multiple_configs')

    # TODO: better way to locate ?
    os.chdir("inphinity/v_0.5/configs")
    configs = glob.glob("*.ini")
    os.chdir("/")

    for config_file in configs:
        # TODO: put in logs file ?
        print('Config file: %s' % config_file)

        '''
        c = Core(config_file)
        c.run()
        '''
