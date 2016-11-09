##
#   Created by: Deruaz Vincent
#   Core of Inphinity
#   23.10.2016
##

from hmmerScan import HmmerScan
from config import Config

class DetectDomaines():
    def __init__(self):
        pass

class Core:
    def __init__(self):
        self.configuration = Config()

    def phase_1(self):
        self.detect_domaines = DetectDomaines()
