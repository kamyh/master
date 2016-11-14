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
from core import DetectDomaines


##                      ##
#   Auxiliary tests      #
##                      ##

def test_10102016_docker_ps():
    h = HmmerScan()
    h.docker_ps()


def test_13102016():
    h = HmmerScan()
    h.compute_domaine_from_host()


def test_14112016_use_of_hmmer_from_core_with_seq_raw():
    h = HmmerScan()

    info_prot = '2abl_A mol:protein length:163  ABL TYROSINE KINASE'
    seq_prot = 'MGPSENDPNLFVALYDFVASGDNTLSITKGEKLRVLGYNHNGEWCEAQTKNGQGWVPSNYITPVNSLEKHSWYHGPVSRNAAEYLLSSGINGSFLVRESESSPGQRSISLRYEGRVYHYRINTASDGKLYVSSESRFNTLAELVHHHSTVADGLITTLHYPAP'

    h.detecter_PFAM(info_prot, seq_prot)

def test_14112016_get_all_id_bacts():
    db = DBUtilties()
    print db.get_id_all_bacts()

def test_14112016_run_detect_domaine():
    dd = DetectDomaines()
    dd.run()



##                      ##
#   Units tests          #
#   To format            #
##                      ##

def test_03112016_config_basic():
    c = Config('inphinity/default.ini')
    c.load_config()
    #c.load_config_test()

def test_08112016_db():
    db = DBUtilties()
    db.show_tables_of_phage_bact()




if __name__ == '__main__':
    # test_10102016()
    # test_13102016()

    #test_03112016_config_basic()

    #test_08112016_db()

    #test_14112016_use_of_hmmer_from_core_with_seq_raw()

    #test_14112016_get_all_id_bacts()

    test_14112016_run_detect_domaine()