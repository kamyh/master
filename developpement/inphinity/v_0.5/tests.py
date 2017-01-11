##
#   Created by: Deruaz Vincent
#   Core of InphinityUnit tests
#   **If all test pass the core can be run**
#   01.11.2016
##

# TODO Transform it in unit test (use a lib)

from tools import Tools

from core import Core
from Bio import *

import glob, os


##                      ##
#   Auxiliary tests      #
##                      ##
def test_07122016_fusion_parallel_using_core():
    print('Run Test: test_07122016_fusion_parallel_using_core')
    c = Core('inphinity/v_0.5/configs/config_1.ini')
    c.run()


def test_17122016_db_diff():
    tools = Tools('inphinity/v_0.5/config.ini')
    print(tools.db.get_new_domains())


if __name__ == '__main__':
    test_07122016_fusion_parallel_using_core()
