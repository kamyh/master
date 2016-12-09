#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 09:14:04 2016

@author: diogo
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

import MySQLdb
from Bio import SeqIO


####Functions DB

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
    
#Executer Insert
def executeInsert(commandeExecuter,params, numDb):
    connection = connectionOpen(numDb)
    cursor = connection.cursor()
    try:
        cursor.execute(commandeExecuter, params)
        connection.commit()
        print "Insert OK"
    except:
        connection.rollback()
        print "Inert error"
    connectionClose(connection)
    return cursor
    

####Fin Functions DB


####Functions non DB

#Fais le parce d un fichier multifasta
def parseSequencesProt(sequence):
    pid = []
    
    text_file = open(tempFilePSeqs, "w")
    text_file.write(sequence)
    text_file.close()

    fasta_sequences = SeqIO.parse(open(tempFilePSeqs),'fasta')
    for fasta in fasta_sequences:
        pid.append(fasta.id)
    return pid

#Obtenir les ID de toutes les interactions positives
def getInteractionsPositives():
    rslt = executeSelect("SELECT * from Interactions", 1)
    resultats = []
    resultats = rslt.fetchall()
    return resultats

#Obtenir les ID de toutes les interactions negatives
def getInteractionsNegatives():
    rslt = executeSelect("SELECT * from Negative_Interactions", 1)
    resultats = []
    resultats = rslt.fetchall()
    return resultats
    
#Retourne la seq proteique des proteines
#(1 = Bacteria; 2 = Phage)
def getSequenceProteines(idCellule, tipeCellule):
    if tipeCellule == 1:
        query = 'SELECT Bacterium_id, GI, Nb_proteins, prot_seq FROM Bacteria WHERE Bacterium_id = ' + str(idCellule)
    else:
        query = 'SELECT Phage_id, GI, Nb_proteins, prot_seq FROM Phages WHERE Phage_id = '+ str(idCellule)
    rslt = executeSelect(query, 1)
    resultats = []
    resultats = rslt.fetchall()
    return resultats
    
#consulte la db pour obtenir les domains
# boolbact 1 - bacterie 0 - phage
def getDomainesByIdCellOffline(idCell, idProt, bacteriaBool):
    query = "SELECT DomainAcc FROM PROTDOM WHERE ProtId ='" + str(idProt) + "'"
    rslt = executeSelect(query, 1)
    resultats = []
    resultats = rslt.fetchall()
    return resultats
    
#Verifier si le domaine n a pas ete actualiser
#Si oui retourne le nouveau domaine
def getExistAutresDomaines(domaine):
    try:
        query = "SELECT NewDomain FROM PFAM WHERE DomainAcc='" + str(domaine) + "'"
        rslt = executeSelect(query, 2)
        newDomaine = rslt.fetchone()
        if "PF" in newDomaine[0]:
            return newDomaine[0]
        return ""
    except:
        return "--"
        
#Obtenir le scor d interaction entre deux domaines
def interactionExisteDom(domaine1, domaine2):
    query = "SELECT * from INTERACTION WHERE Domain1='"+ str(domaine1) + "' and Domain2='" + str(domaine2) + "'"
    rslt = executeSelect(query, 2)

    qtdRegistre = rslt.rowcount
    if qtdRegistre == 0:
        query = "SELECT * from INTERACTION WHERE Domain1='" + str(domaine2) + "' and Domain2='" + str(domaine1)  + "'"
        rslt = executeSelect(query, 2)
    qtdRegistre = rslt.rowcount
    if qtdRegistre == 1:
        aux = rslt.fetchone()
        return sum(aux[2:16])
    return -1
    
#Inserer le scor de l IPP dans le tableau Score_interactions
def insertScoreIPP(idProtBact, idProtPhage, positivInteraction, interactionId, Score):
    aux = [idProtBact, idProtPhage, positivInteraction, interactionId, float(Score)]
    executeInsert("INSERT INTO Score_interactions (ProtBactId, ProtPhageId, Positiv_Interaction, Interaction_Id, Score_result) VALUES (%s, %s, %s, %s, %s)",aux, 1)
   
#Obtenir les ID de toutes les interactions
def getAllIntractions():
    listInteractionP = []
    listInteractionN = []
    listInteractions = []
    listInteractionP = getInteractionsPositives()
    listInteractionN = getInteractionsNegatives()
    #-----#
    listInteractions = listInteractionP + listInteractionN
    return listInteractions
    
#Retourne les ids de proteines d un organism
#1 - bacterie 2 - phage  
#Les domaines ons en relation avec l id de la protein de chaque organisme 
def getidsSeqProt(idCell, typeOfCell):
    sequence = getSequenceProteines(idCell, typeOfCell)
    idsSeq = parseSequencesProt(sequence[0][3])
    return idsSeq

#Obtenir les domaines d une protein d un organisme
# boolBact 1 - bact 0 - phage
def getDomainsCell(idCell, idprot, boolBact):
    listReturnDoms = []
    listDoms = []
    listDoms = getDomainesByIdCellOffline(idCell, idprot, boolBact)
    for dom in listDoms:
        if len(dom[0]) > 2 and "NA" not in dom[0]:
            listReturnDoms.append(dom[0])
    #print listReturnDoms
    return listReturnDoms

#Calcul le score d interaction entre toutes les paire de proteines
#pour chaque IPP entre deux organisme va calculer le score et le retourner
def getScoresDomaines(vecDomBac, vecDomPha):
    ScoreDom = 0
    ScoreIntermediate = 0
    ScoreIntermediateB = 0
    ScoreIntermediateC = 0
    ScoreIntermediateD = 0
    qtdNewInteract = 0.0
    newDomBact = ""
    newDomPhag = ""
    for domBac in vecDomBac:
        newDomBact = getExistAutresDomaines(domBac)
        #if newDomBact != "--":
        for domPhag in vecDomPha:
            #voir si pour ce domaine il en exist un actualise
            newDomPhag = getExistAutresDomaines(domPhag)
            ScoreIntermediate = 0
            ScoreIntermediateB = 0
            ScoreIntermediateC = 0
            ScoreIntermediateD = 0
            qtdNewInteract = 0.0
            #pas de new domains
            if "PF" not in newDomBact and "PF" not in newDomPhag:
                ScoreIntermediate = interactionExisteDom(domBac, domPhag)
                if ScoreIntermediate > 0:
                    qtdNewInteract = 1.0
            #new domaine only for bacteria
            if "PF" in newDomBact and "PF" not in newDomPhag:
                ScoreIntermediate = interactionExisteDom(domBac, domPhag)
                ScoreIntermediateB = interactionExisteDom(newDomBact, domPhag)
                if ScoreIntermediate > 0:
                    qtdNewInteract = 1.0
                if ScoreIntermediateB > 0:
                    qtdNewInteract = qtdNewInteract + 1.0
            #new domaine only for Phages
            if "PF" not in newDomBact and "PF" in newDomPhag:
                ScoreIntermediate = interactionExisteDom(domBac, domPhag)
                ScoreIntermediateB = interactionExisteDom(newDomBact, newDomPhag)
                if ScoreIntermediate > 0:
                    qtdNewInteract = 1.0
                if ScoreIntermediateB > 0:
                    qtdNewInteract = qtdNewInteract + 1.0
            #new domaine for both
            if "PF" not in newDomBact and "PF" in newDomPhag:
                ScoreIntermediate = interactionExisteDom(domBac, domPhag)
                ScoreIntermediateB = interactionExisteDom(newDomBact, domPhag)
                ScoreIntermediateC = interactionExisteDom(domBac, newDomPhag)
                ScoreIntermediateD = interactionExisteDom(newDomBact, newDomPhag)
                if ScoreIntermediate > 0:
                    qtdNewInteract = 1.0
                if ScoreIntermediateB > 0:
                    qtdNewInteract = qtdNewInteract + 1.0
                if ScoreIntermediateC > 0:
                    qtdNewInteract = qtdNewInteract + 1.0
                if ScoreIntermediateD > 0:
                    qtdNewInteract = qtdNewInteract + 1.0
                    
            if qtdNewInteract > 0:
                #print "QTDINteraction: " + str(qtdNewInteract)
                ScoreDom = ScoreDom + ((ScoreIntermediate + ScoreIntermediateB + ScoreIntermediateC + ScoreIntermediateD)/qtdNewInteract)
    return ScoreDom;
    
####Fin Functions non DB


####Main


listInteract = getAllIntractions()



idsSeqBact = getidsSeqProt(0, 1)
newDomBact = getExistAutresDomaines("PF11509")

for interaction in listInteract:
    idInteraction = interaction[0]
    idBacteria = interaction[1]
    idPhage = interaction[2]
    PosNegInteraction = interaction[3]
    idsSeqBact = getidsSeqProt(idBacteria, 1)
    idsSeqPhage = getidsSeqProt(idPhage, 2)
    lisDomainsBac = []    
    lisDomainsPhage = []  
    for idSeqBact in idsSeqBact:
        print "Id Bact: " + idSeqBact
        lisDomainsBac = getDomainsCell(idBacteria, idSeqBact, 1)
        if len(lisDomainsBac) > 0:
            for idSeqPhage in idsSeqPhage:
                lisDomainsPhage = getDomainsCell(idPhage, idSeqPhage, 0)
                if len(lisDomainsPhage) > 0:
                    ScorePPI = getScoresDomaines(lisDomainsBac, lisDomainsPhage)
                    if ScorePPI > 0:
                        print ScorePPI
                        insertScoreIPP(idSeqBact, idSeqPhage, PosNegInteraction, idInteraction, ScorePPI)
            
    print idsSeqBact[0]
    print idsSeqPhage[0]


####Fim main