#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 13:36:25 2016

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
tempFilePSeqs = "/home/diogo/Bureau/gradesDict.p"

#####Fin Variables avec fichiers temporaires


import MySQLdb
import cPickle



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

#Close connetion    
def connectionClose(dbConnection):
    dbConnection.close(); 

#Execute Select
def executeSelect(commandeExecuter, numDb):
    connection = connectionOpen(numDb)
    cursor = connection.cursor()
    cursor.execute(commandeExecuter)
    connectionClose(connection)
    return cursor




####Fin Functions DB


#### Fonctions non DB

#retourne le contenu du tableau QtdScore
def getAllInfosScores():
    query = "select * from QtdScores "
    rslt = executeSelect(query, 1)
    resultats = []
    resultats = rslt.fetchall()
    return resultats

#retourne 4 vecteurs contenant id classe score et frequence 
def getInfosInVectors():
    infos = getAllInfosScores()
    vecIdInter = []
    vecClassInter = []
    vecScoreInter = []
    vecQtdScoreInter = []
    for info in infos:
        #print "Information: " + str(info[0])
        vecIdInter.append(int(info[1]))
        vecClassInter.append(int(info[2]))
        vecScoreInter.append(int(info[3]))
        vecQtdScoreInter.append(int(info[4]))
    return vecIdInter, vecClassInter, vecScoreInter, vecQtdScoreInter


####Fin fonctions non DB


####MAIN

vecId, vecCla, vecScor, vecQtd = getInfosInVectors()



f = open(tempFilePSeqs, 'w')   # Pickle file is newly created where foo1.py is
cPickle.dump([vecId, vecCla, vecScor, vecQtd], f)          # dump data to f
f.close()