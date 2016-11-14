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
        self.configuration = Config()
        self.list_id_organismes = self.db.get_id_all_bacts()

        #Fichier pour parser les seqs
        self.temp_file_pseqs = self.configuration.get_path_to_core()

    #Parser les sequences multi-fasta
    def parse_sequences_prot(sequence):
        pid = []
        pseq = []
        text_file = open(tempFilePSeqs, "w")
        text_file.write(sequence)
        text_file.close()

        fasta_sequences = SeqIO.parse(open(tempFilePSeqs),'fasta')
        for fasta in fasta_sequences:
            pid.append(fasta.id)
            pseq.append(fasta.seq.tostring())
            #new_sequence = some_function(sequence)
            #write_fasta(out_file)

        return pid, pseq

    #Recherche des domaines pour chaque Prot
    def seek_Domaines(vecId, vecSeq, idCell, boolBacteria):
        #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        for idProt, seqProt in zip(vecId, vecSeq):
            try:
                vecDomaines = []
                proteinExist = getProteineInProtDom(idProt)
                print proteinExist
                if proteinExist == 0:
                    print "insert"
                    domainesReturned = detecterPFAM(idProt,seqProt)
                    print domainesReturned
                    executeInsertDomains(idProt, domainesReturned, idCell, boolBacteria, "--")
                else:
                    print "exists"
            except:
                vecDomaines = ['--PN--']
                executeInsertDomains(idProt, vecDomaines, idCell, boolBacteria, seqProt)

    def run(self):
        for id in self.list_id_organismes:
            print 'Organism ID: ' + str(id)
            pidss_bact = []
            pseqss_bact = []

            resultats_organismes = self.db.get_sequence_proteines_bacteria(id)

            pidss_bact, pseqss_bact = self.parse_sequences_prot(resultats_organismes[0][3])

            print pidss_bact
            print pseqss_bact
            seek_domaines(pidss_bact, pseqss_bact, id, 0)


class Core:
    def __init__(self):
        self.configuration = Config()

    def phase_1(self):
        self.detect_domaines = DetectDomaines()
