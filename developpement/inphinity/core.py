##
#   Created by: Deruaz Vincent
#   Core of Inphinity
#   23.10.2016
##

from hmmerScan import HmmerScan
from config import Config
from database_utilities import DBUtilties

class DetectDomaines():
    def __init__(self):
        self.db = DBUtilties()
        self.listIdOrganismes = self.db.get_id_all_bacts()

    def run(self):
        for id in self.listIdOrganismes:
            print id

class Core:
    def __init__(self):
        self.configuration = Config()

    def phase_1(self):
        self.detect_domaines = DetectDomaines()
