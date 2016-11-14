# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 11:52:52 2016

@author: diogo
"""


#####Donnees acces BD
dbHost = "127.0.0.1"
dbUser = "root"
dbPasswd = "17061990"

dbnamePb = "phage_bacts"
dbnameDom = "domine"
#####Fin Donnees acces BD


import urllib, urllib2
import json
import MySQLdb



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


####Fonctions DB

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
    
    
# Executer une simple commande SQL
def executeSelect(commandeExecuter, numDb):
    connection = connectionOpen(numDb)
    cursor = connection.cursor()
    cursor.execute(commandeExecuter)
    connection.commit()
    connectionClose(connection)
    return cursor


#Executer une commande avec parametre
def executeInsert(commandeExecuter,params, numDb):
    connection = connectionOpen(numDb)
    cursor = connection.cursor()
    try:
        #print params
        cursor.execute(commandeExecuter, params)
        connection.commit()
        #print "OK"
    except:
        connection.rollback()
        print "NO"
    connectionClose(connection)
    return cursor

####Fin fonctions DB



####Methods non DBs

#Obtenir toutes les proteines dont les domaines n ont pas etes trouves
def getAllNotDomaines():
    query = "select * from PROTDOM WHERE DomainACC = \"--PN--\""
    print query
    reslt = executeSelect(query, 1)
    restResults = reslt.fetchall()
    
    protDomsId = []
    idsSeqs = []
    cellIds = []
    boolBact = []
    protsSeqs = []
    
    sizeData = len(restResults)
    aux = 0
    while aux < sizeData:
        protDomsId.append(restResults[aux][0])
        idsSeqs.append(restResults[aux][1])
        cellIds.append(restResults[aux][3])
        boolBact.append(restResults[aux][4])
        protsSeqs.append(restResults[aux][5])
        aux = aux +1
    return restResults
    
    
#Si le serveur a retourne une reponse alors supprime le PN et insert les domaines ou NA    
def executeUpdateDomaines(idProteinDom, idSeq, id_Cell, bool_Bacteria, seqProt, domaines):
    domainesNoRep = list(set(domaines))
    for dom in domainesNoRep:
        if len(dom) >= 5:
            print idProteinDom
            #dom = "\"" + dom + "\""
            print "Protein: ", idSeq, " Domaines: ", dom
            aux = (idSeq, dom, int(id_Cell),bool_Bacteria, "--")
            queryDelete = "DELETE FROM PROTDOM WHERE ProtDomId=" + str(idProteinDom) + " AND DomainAcc=\"--PN--\""
            executeSelect(queryDelete, 1)            
            executeInsert("INSERT INTO PROTDOM (ProtId, DomainAcc, Cell_id, Bacteria_Cell, ProtSeq) VALUES (%s, %s, %s, %s, %s)",aux, 1)
        else:
            print "NOOOO Protein: ", idSeq, " Domaines: ", dom

#Recherche des domaines pour chaque Prot
def chercherDomaines(vecProtDomsId, vecIdsSeqs, vecCellIds, vecBoolBact, vecProtsSeqs):
    for protDomsId, idsSeqs, cellIds, boolBact, protsSeqs in zip(vecProtDomsId, vecIdsSeqs, vecCellIds, vecBoolBact, vecProtsSeqs):
        try: 
            print "Id seq: " + idsSeqs
            vecDomaines = detecterPFAM(idsSeqs,protsSeqs)
            print vecDomaines
            if vecDomaines == "NA":
                vecDomaines = ['--NA--']
                print "Passe"
                #def executeUpdateDomaines(idProteinDom, idSeq, id_Cell, bool_Bacteria, seqProt, domaines):
            
        except:
            vecDomaines = ['--PN--']
            #print "Erreur pour la proteine: " + str(protDomsId)
        executeUpdateDomaines(protDomsId, idsSeqs,cellIds, boolBact, protsSeqs, vecDomaines)


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

#Fin methods non DB




####Main
#Obtenir les domaines qui n ont pas ete trouves
domainesPN = getAllNotDomaines()

#Vecteurs qui vont contenir l information des domaines pas trouves

sizeVec = len(domainesPN)
aux = 0

protDomsId = []
idsSeqs = []
cellIds = []
bacteriaCells = []
protsSeqs = []


while aux < sizeVec:
    protDomsId.append(domainesPN[aux][0])
    idsSeqs.append(domainesPN[aux][1])
    cellIds.append(domainesPN[aux][3])
    bacteriaCells.append(domainesPN[aux][4])
    protsSeqs.append(domainesPN[aux][5])
    aux = aux + 1

chercherDomaines(protDomsId, idsSeqs, cellIds, bacteriaCells, protsSeqs)
