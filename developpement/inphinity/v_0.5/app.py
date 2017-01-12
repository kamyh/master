##
#   Created by: Deruaz Vincent
#   10.01.2017
##

from tools import Tools

from core import Core
from Bio import *

import glob, os

if __name__ == '__main__':
    os.chdir("inphinity/v_0.5/configs")
    configs = glob.glob("*.ini")

    for config_file in configs:
        print('Config file: %s' % config_file)

        c = Core(config_file)
        c.run()
