##
#   Created by: Deruaz Vincent
#   Core of InphinityUnit tests
#   **If all test pass the core can be run**
#   01.11.2016
##

# TODO Transform it in unit test (use a lib)

from hmmerScan import HmmerScan
from config import Config
from database_utilities import DBUtilties
from core import Core
from Bio import *


##                      ##
#   Auxiliary tests      #
##                      ##
def test_07122016_fusion_parallel_using_core():
    c = Core()
    c.run()


if __name__ == '__main__':
    # test_07122016_fusion_parallel()
    test_07122016_fusion_parallel_using_core()
