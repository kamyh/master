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


##                      ##
#   Auxiliary tests      #
##                      ##

def test_10102016_docker_ps():
    h = HmmerScan()
    h.docker_ps()


def test_13102016():
    h = HmmerScan()
    h.compute_domaine_from_host()


##                      ##
#   Units tests          #
##                      ##

def test_03112016_config_basic():
    c = Config('inphinity/default.ini')
    c.load_config()
    #c.load_config_test()

def test_08112016_db():
    db = DBUtilties()
    db.load_db()


if __name__ == '__main__':
    # test_10102016()
    # test_13102016()

    #test_03112016_config_basic()

    test_08112016_db()