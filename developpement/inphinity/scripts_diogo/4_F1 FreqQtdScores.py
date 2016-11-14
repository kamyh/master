#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 11:34:04 2016

@author: diogo
"""

import MySQLdb
from Bio import SeqIO

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
    
#Execute Insert
def executeInsert(commandeExecuter,params, numDb):
    connection = connectionOpen(numDb)
    cursor = connection.cursor()
    try:
        cursor.execute(commandeExecuter, params)
        connection.commit()
        #print "Insert OK"
    except MySQLdb.Error, e:
        connection.rollback()
        print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        print "Inert error"
    connectionClose(connection)
    return cursor

#Fin Fonctions DB

####Fonctions non DB


#Inserer la frequence d un score dans le tableau qtdScore
def insertQtdsScores(idInteraction, classInteraction, ScoreNumber, QuantityScore):
    aux = [idInteraction, classInteraction, ScoreNumber, QuantityScore]
    executeInsert("INSERT INTO QtdScores (Interaction_Id, Positiv_Interaction, ScoreNumber, QuantityScore) VALUES (%s, %s, %s, %s)", aux, 1)

#Retourner les interactions positives
def getInteractionsPositives():
    rslt = executeSelect("SELECT * from Interactions", 1)
    resultats = []
    resultats = rslt.fetchall()
    return resultats
    
#Retouner les interactions negatives
def getInteractionsNegatives():
    rslt = executeSelect("SELECT * from Negative_Interactions", 1)
    resultats = []
    resultats = rslt.fetchall()
    return resultats

#Retourne les score d une interaction    
def getResutladosByIntClassBDD(idInteraction, positivClass):
    query = "select distinct Score_result  from Score_interactions Where Positiv_Interaction =" + str(positivClass) + " AND Interaction_Id =" + str(idInteraction) + " ORDER BY Score_result"
    rslt = executeSelect(query, 1)
    resultats = rslt.fetchall()
    return resultats

#retourn la frequence d un score dans une interaction
def getQtdScores(idInteraction, positivClass, scoreValue):
    query = "select count(*) from Score_interactions WHERE Positiv_Interaction =" + str(positivClass) + " AND Interaction_Id =" + str(idInteraction) + " AND Score_result ="+ str(scoreValue)
    rslt = executeSelect(query, 1)
    return int(rslt.fetchone()[0])

#Retourne les ids de toutes les bacteries
def getIdAllBacteries():
    query = "select Bacterium_id from Bacteria"
    rslt = executeSelect(query, 1)
    idBacts = rslt.fetchall()
    bactsIdRet = []
    for resultat in idBacts:
        bactsIdRet.append(resultat[0])
    return bactsIdRet

#Retourne les ids de tous bacteriophage    
def getIdAllPhages():
    query = "select Phage_id from Phages"
    rslt = executeSelect(query, 1)
    idPhage = rslt.fetchall()
    PhageIdRet = []
    for resultat in idPhage:
        PhageIdRet.append(resultat[0])
    return PhageIdRet
    
#Retourne la sequence proteomique d un organisme
# 1 = bacterie
# 2 = phage
def getSequenceProteines(idCellule, tipeCellule):
    if tipeCellule == 1:
        query = 'SELECT Bacterium_id, GI, Nb_proteins, prot_seq FROM Bacteria WHERE Bacterium_id = ' + str(idCellule)
    else:
        query = 'SELECT Phage_id, GI, Nb_proteins, prot_seq FROM Phages WHERE Phage_id = '+ str(idCellule)
    rslt = executeSelect(query, 1)
    resultats = []
    resultats = rslt.fetchall()
    return resultats

#Retourner toutes les interactions
def getAllIntractions():
    listInteractionP = []
    listInteractionN = []
    listInteractions = []
    listInteractionP = getInteractionsPositives()
    listInteractionN = getInteractionsNegatives()
    listInteractions = listInteractionP + listInteractionN
    return listInteractions

#Retourner le nombre de proteines d un organisme
def getNumberProteins(sequence):
    text_file = open(tempFilePSeqs, "w")
    text_file.write(sequence)
    text_file.close()

    fasta_sequences = SeqIO.parse(open(tempFilePSeqs),'fasta')
    qtdProts = sum(1 for x in fasta_sequences)    
    return qtdProts
    
def getAllScoresByIdInterClass(idInteraction, positivClass):
    aux = getResutladosByIntClassBDD(idInteraction, positivClass)
    results = []
    for rst in aux:
        results.append(rst[0])
    return results
    
    
####Fin Fonctions non DB



####MAIN

idsBact = getIdAllBacteries()
idsPhages = getIdAllPhages()
BactQtdProts = {}
PhageQtdProts = {}


for idBact in idsBact:
    resultatsBact = getSequenceProteines(idBact,1)
    size = getNumberProteins(resultatsBact[0][3])
    BactQtdProts[(int(idBact))] = size
    print "QTD Prot Bact: " + str(size)
    
for idPhage in idsPhages:
    resultatsPhage = getSequenceProteines(idPhage,2)
    size = getNumberProteins(resultatsPhage[0][3])
    PhageQtdProts[(int(idPhage))] = size
    print str(idPhage) + " : QTD Prot Phage: " + str(size)


listInteract = getAllIntractions()  

#Calculer les frequences de chaque score pour chacune des interactions  
SommeQtd = 0
qtdOfZeros = 0
for interact in listInteract:
    SommeQtd = 0
    qtdOfZeros = 0
    
    idInteraction = interact[0]
    idbacterie = interact[1]
    idPhage = interact[2]
    typeClass = interact[3]
    allScors = getAllScoresByIdInterClass(idInteraction, typeClass)
    for Score in allScors:
        qtdScors = getQtdScores(idInteraction,typeClass,Score)
        insertQtdsScores(idInteraction, typeClass, Score, qtdScors)
        SommeQtd = SommeQtd + qtdScors
    #Le nombre de fois qu apparait 0 est equivalant au nombre d IPP moin la freq des autres scores
    qtdOfZeros = (BactQtdProts[(int(idbacterie))] * PhageQtdProts[(int(idPhage))]) - SommeQtd
    insertQtdsScores(idInteraction, typeClass, 0, qtdOfZeros)

