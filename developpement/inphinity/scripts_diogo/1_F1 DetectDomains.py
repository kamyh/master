# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""


#####Données accès BD
dbHost = "127.0.0.1"
dbUser = "root"
dbPasswd = "17061990"

dbnamePb = "phage_bacts"
dbnameDom = "domine"
#####Fin Données accès BD

#####Variables avec fichiers temporaires

#Fichier pour parser les seqs
tempFilePSeqs = "/home/diogo/Bureau/tmpMF.txt"

#####Fin Variables avec fichiers temporaires

import urllib, urllib2

import MySQLdb
from Bio import SeqIO
import json
import sys


####Fonction API HMM
class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        return headers
opener = urllib2.build_opener(SmartRedirectHandler())
urllib2.install_opener(opener);


def detecterPFAM(infoProt, seqProt):

    parameters = {
                  'hmmdb':'pfam',
                  'seq':'>' + infoProt + '\n' + seqProt + '\n'
                  }
    enc_params = urllib.urlencode(parameters);


    request = urllib2.Request('http://www.ebi.ac.uk/Tools/hmmer/search/hmmscan',enc_params)
    
    #get the url where the results can be fetched from
    results_url = urllib2.urlopen(request).getheader('location')
    
    # modify the range, format and presence of alignments in your results here
    res_params = {
                  'output':'json',
                  'range':'1,10'
                  }
                  
                  # add the parameters to your request for the results
    enc_res_params = urllib.urlencode(res_params)
    modified_res_url = results_url + '?' + enc_res_params

    # send a GET request to the server
    results_request = urllib2.Request(modified_res_url)
    data = urllib2.urlopen(results_request)

    donnees = data.read().decode('utf-8')


    j = json.loads(donnees)    
    domaines = ""
    domainesReturn = []
    try:
        auxDoms = j['results']['hits']
        for dom in auxDoms:
            domaines = dom['acc'] + " " + domaines
        
        domainesReturn = speparerDomaines(domaines)
        
    except IndexError:
        domainesReturn = ["--NA--"]
    return domainesReturn
    
####Fin Fonction API HMM

#### Fonctions DB


#Ouvre la connexion a la DB
#1 = Phage_bacts
#2 = domine
def connectionOpen(numDb):
    if numDb == 1:
        dbConnection = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPasswd, db=dbnamePb)
    else:
        dbConnection = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPasswd, db=dbnameDom)
    return dbConnection

#Fermer connexion
def connectionClose(dbConnection):
    dbConnection.close();  

# Executer une simples commande SQL
def executeSelect(commandeExecuter, numDb):
    connection = connectionOpen(numDb)
    cursor = connection.cursor()
    cursor.execute(commandeExecuter)
    connectionClose(connection)
    return cursor

#Executer une commande avec parametre
def executeSelectParam(commandeExecuter, params, numDb):
    connection = connectionOpen(numDb)
    cursor = connection.cursor()
    cursor.execute(commandeExecuter, [params])
    connectionClose(connection)
    return cursor
    
    
#Executer une commande d insertion
def executeInsert(commandeExecuter,params, numDb):
    connection = connectionOpen(numDb)
    cursor = connection.cursor()
    try:
        cursor.execute(commandeExecuter, params)
        connection.commit()
    except:
        connection.rollback()
        print "NO"
    connectionClose(connection)
    return cursor


#####Fin fonctions DB


#####Fonctions non DB


#Obtenir tous les ID des bacteries
def getIdAllBacteries():
    query = "select Bacterium_id from Bacteria"
    rslt = executeSelect(query, 1)
    idBacts = rslt.fetchall()
    bactsIdRet = []
    for resultat in idBacts:
        bactsIdRet.append(resultat[0])
    return bactsIdRet
    
#Obtenir les sequences proteiques multi-fasta:
#1 = Bacterie
#2 = Phage
def getSequenceProteines(idCellule, tipeCellule):
    if tipeCellule == 1:
        query = 'SELECT Bacterium_id, GI, Nb_proteins, prot_seq FROM Bacteria WHERE Bacterium_id = ' + str(idCellule)
    else:
        query = 'SELECT Phage_id, GI, Nb_proteins, prot_seq FROM Phages WHERE Phage_id = '+ str(idCellule)
    rslt = executeSelect(query, 1)
    resultats = []
    resultats = rslt.fetchall()
    return resultats
    
#Parser les sequences multi-fasta
def parseSequencesProt(sequence):
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
 

#Verifier si la seq a deja ete recherchee
def getProteineInProtDom(idProtein):
    reslt = executeSelectParam("SELECT count(*) from PROTDOM WHERE ProtId = %s", idProtein, 1)
    return int(reslt.fetchone()[0])
    
    
#Inserer domaines d interactions d'une proteines
def executeInsertDomains(idProtein, domaines, id_Cell, bool_Bacteria, seqProt):
    domainesNoRep = list(set(domaines))
    for dom in domainesNoRep:
        print dom
        if len(dom) >= 5:
            #print dom
            aux = (idProtein, dom, int(id_Cell), bool_Bacteria, seqProt)
            executeInsert("INSERT INTO PROTDOM (ProtId, DomainAcc, Cell_id, Bacteria_Cell, ProtSeq) VALUES (%s, %s, %s, %s, %s)",aux, 1)

   
#Recherche des domaines pour chaque Prot
def chercherDomaines(vecId, vecSeq, idCell, boolBacteria):
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

#Parse du json        
def speparerDomaines(domainesPass):
    PFdom = []
    domainesVec = domainesPass.split(' ')
    domainesVec = domainesVec[:-1]
    if len(domainesVec) != 0:
        for dom in domainesVec:
            #print "DOM: " + dom
            PFdom.append(dom.split('.')[0])
    else:
        PFdom = ["--NA--"]
    return PFdom

#####Fin Fonction non DB


### Main
#Obtenir les ID des bacteries
listIdOrganismes = getIdAllBacteries()

listIdOrganismes = [0]
#parcourire tous les ids
for value in listIdOrganismes:

    idOrganisme = value
    #print idPhage
    resultatsOrganismes = getSequenceProteines(idOrganisme,1)
    pidssBact = []
    pseqssBact = []
    pidssBact, pseqssBact = parseSequencesProt(resultatsOrganismes[0][3])
    print pidssBact
    print pseqssBact
    chercherDomaines(pidssBact, pseqssBact, idOrganisme, 0)
