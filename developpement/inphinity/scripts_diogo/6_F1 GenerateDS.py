#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 14:12:31 2016

@author: diogo
"""

import cPickle
import os.path
import numpy as np
import csv

#####Fonctions
#Controle que la freq de tout les scores est egale a la qtd d IPP
def controlNumberInteractionsOnlyOne(vecListQtdInter, position):
    QtdInteractionInt = []   
    onlyZeros = 0
    for i in vecListQtdInter:
        QtdInteractionInt.append(int(i))
        if i == qtdInteractionsAll[position]:
            onlyZeros = 1
    if onlyZeros == 1 and typeConfig ==1:
        QtdInteractionInt = [0] * (len(vecListQtdInter)-3)
        QtdInteractionInt.insert(0,vecListQtdInter[0])
        auxSize = len(vecListQtdInter)-1
        QtdInteractionInt.insert(1, qtdInteractionsAll[position])
        QtdInteractionInt.append(vecListQtdInter[auxSize])
    return QtdInteractionInt

#retourne un vec avec qtd interactions
def createVecSize(matValues):
    qtdInteractions = []
    for nmInteractions in matValues:
        qtdInteractions.append(sum(nmInteractions))
    return qtdInteractions   

#creation de vecteurs
def creatVecNBins(boolNormalizDataSet):
    qtdScoresHisto = []
    SepHisto = []
    vecnormalValues = []
    vecQtdScoresHisto = []
    vecSeqHisto = []
    interIdPreced = vecId[0]
    vecResultsProv = []
    position = 0
    
    
    print str(len(vecId))
    for idInter in vecId:

        if interIdPreced != idInter:
            print "ID: " + str(interIdPreced)
            
            vecIdsDS.append(interIdPreced)
            vecTypeClass.append(vecCla[position])
            interIdPreced = idInter
            print len(vecResultsProv)
            
            if boolNormalizDataSet == True:          
                qtdValues = len(vecResultsProv)
                qtdValues = qtdValues + 0.0
                for valueInter in vecResultsProv:
                    auxScor = valueInter/qtdValues
                    vecnormalValues.append(auxScor)
                qtdScoresHisto, SepHisto = np.histogram(vecnormalValues, bins=binsConfig)
            else:
                qtdScoresHisto, SepHisto = np.histogram(vecResultsProv, bins=binsConfig)
            vecQtdScoresHisto.append(qtdScoresHisto)
            vecSeqHisto.append(SepHisto)
            #print qtdScoresHisto
            #print SepHisto
            vecResultsProv = []
            vecnormalValues = []
        qtdScores = vecQtd[position]
        aux = 0
        while aux < qtdScores:
            vecResultsProv.append(vecScor[position])
            aux = aux +1  
        position = position + 1  
# a l epoque j ai eu des problemes avec la derniere ligne et j ai pas trop perdu de temps avec
# le probleme se trouve dans le premier cycle for dans les conditions IF
    print "last Line"
    position = position -1
    vecIdsDS.append(interIdPreced)
    vecTypeClass.append(vecCla[position])
    
    if boolNormalizDataSet == True:          
        qtdValues = len(vecResultsProv)
        qtdValues = qtdValues + 0.0
        for valueInter in vecResultsProv:
            auxScor = valueInter/qtdValues
            vecnormalValues.append(auxScor)
        qtdScoresHisto, SepHisto = np.histogram(vecnormalValues, bins=binsConfig)
    else:
        qtdScoresHisto, SepHisto = np.histogram(vecResultsProv, bins=binsConfig)
        vecQtdScoresHisto.append(qtdScoresHisto)
        vecSeqHisto.append(SepHisto)
        
    return vecQtdScoresHisto, vecSeqHisto

#Ecrire le fichier
def writeFile(n, binsList, vecid, vecCla, pathFile, boolNormaliz):
    print "Start wrinting"
    position = 0
    binsListR = [round(i,5) for i in binsList]
    
    if boolNormaliz == 1:
        binsListR = [format(i, '.8f') for i in binsListR]
    
    binsListR.insert(0, "ID_interaction")
    binsListR.append("Class_interactions")
    
    with open(pathFile, 'w') as outcsv:   
        writer = csv.writer(outcsv, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerow(binsListR)
        for idInteract, typeClass, listHisto in zip(vecid, vecCla,n ):
            listAux = listHisto.tolist()
            listAux.append(typeClass)
            listAux.insert(0, idInteract)

            listAuxB = controlNumberInteractionsOnlyOne(listAux, position)
            writer.writerow(listAuxB)
            position = position +1


#demander a l utilisateur les configurations des bins
def getUserConfigBinds(maxScorDoms, maxScoreNormDoms, typeDataSet):  
    aux = 1
    x = -1
    while (aux == 1):
        try:
            x = int(input("Number of Bins (1) or Vector of Bins (2) :"))
        except:
            print "Input not legal"
        if(x == 1 or x == 2 ):
            aux = 0
    if(x == 1):
        aux = 1
        while(aux == 1):
            try:
                x = int(input("Number of Bins (1-" + str(maxScorDoms) + ") :"))
            except:
                print "Input not legal"
            if(x>0 and x <= maxScorDoms):
                aux = 0
        return x, 1
    if(x == 2):
        aux = 1
        maxValueAutoriz = 0
        while(aux == 1):
            try:
                if typeDataSet == 0:
                    x = (input("Space Between bins (1-" + str(maxScorDoms) + ") :"))
                    auxMinScore = 0
                    maxValueAutoriz = maxScorDoms
                else:
                    #auxMinScore = maxScoreNormDoms/100
                    maxValueAutoriz = maxScoreNormDoms
                    
                    #valueMinScore = format(auxMinScore, '.15f')
                    valueMaxScore = format(maxScoreNormDoms, '.15f')
                    x = float(input("Space Between bins ( >0.0 [Min. founded: " + str(minScore) + " ] - " + str(valueMaxScore) + " ) :"))
                    auxMinScore = 0
            except:
                print "input not legal"
            if(x>auxMinScore and x < maxValueAutoriz):
                aux = 0
                
        if typeDataSet == 1:
            maxScorDoms = maxScoreNormDoms
        vecBins = []
        while (aux < maxScorDoms):
            vecBins.append(aux)
            aux = aux + x
        if aux >= maxScorDoms:
            vecBins.append(maxScorDoms)
                
        return vecBins, 2

#normaliser les scores
def getmaxScoreNormalized():
    interIdPreced = vecId[0]
    maxScore = 0.00000000001  
    minFinalScor = 1.0
    qtdScoreTot = 0
    position = 0
    vecAuxScores = []
    
    for idInter in vecId:
        if interIdPreced != idInter:
            print qtdScoreTot
            for score in vecAuxScores:
                scoreNormal = score / qtdScoreTot
                
                if scoreNormal < minFinalScor and scoreNormal != 0.0:
                    minFinalScor = scoreNormal
                if scoreNormal > maxScore:
                    maxScore = scoreNormal
            vecAuxScores = []
            qtdScoreTot = 0
            interIdPreced = idInter

           
        qtdScoreTot = qtdScoreTot + vecQtd[position]
        
        vecAuxScores.append(vecScor[position])
        
        
        position = position + 1
    return maxScore, minFinalScor

#demande si l utilisateur veux utiliser les donnees normalisees
def getUserConfigTypeDataSet():  
    aux = 1
    x = -1
    while (aux == 1):
        try:
            x = int(input("Use normal dataSet : (Yes = 1/ No = 0): "))
        except:
            print "Input not legal"
        if(x == 1 or x == 0 ):
            aux = 0
            if x == 1:
                return True
            if x == 0:
                return 0
                
                
#indiquer le chemin ou se trouve le fichier pickle
def pathFilePickle():
    aux = 0
    while(aux == 0):
        filePath = raw_input("File path: ")
        result = os.path.isfile(filePath)
        if(result == True):
            return filePath
        else:
            print "File not exists"
#demander a l utilisateur ou enregistrer le set de donnees
def pathSaveFile():
    filePath = raw_input("Save file: ")
    return filePath
    



####Fin fonctions


####main

maxScore = -1
maxScoreNorm = -1

#va demander a l utilisateur la localisation du fichier pickle
pathFile = pathFilePickle()
#va demander a l utilisateur ou il pretend l'enregistrer
pathFileSave = pathSaveFile()


f = open(pathFile, 'r')
vecId, vecCla, vecScor, vecQtd = cPickle.load(f)
f.close()

maxScore = max(vecScor)

len(vecId)

vecIdsDS = []
vecTypeClass = []
vecQtdProteins = []
vecResultFinal = []
vecResultNormal = []
# demander s'il prétends normalisé les données ipp ou pas
typeDataSet = getUserConfigTypeDataSet()
if typeDataSet == 1:
    #normaliser les donnes en accord avec le nombre d'IPP
    maxScoreNorm,minScore = getmaxScoreNormalized()
    
    
#Demander les infos a l utilisateur et retourne le choix de l user
binsConfig, typeConfig = getUserConfigBinds(maxScore, maxScoreNorm, typeDataSet)  


vecQtdScoresHistoResults = []
vecSeqHistoResults = []

#creer les bins et retourne l intervalle de chacun d eux et les frequence
vecQtdScoresHistoResults, vecSeqHistoResults = creatVecNBins(typeDataSet)

#vec avec qtd interaction
qtdInteractionsAll = createVecSize(vecQtdScoresHistoResults)

#num de bins
vecNumBins = len(vecQtdScoresHistoResults[0])
aux = 0
#vec avec id des bins qui est utilise pour la premiere ligne des datasets
auxVec = []
while(aux < vecNumBins):
    auxVec.append(aux)
    aux = aux +1

#Ecrire le dataset
writeFile(vecQtdScoresHistoResults, auxVec, vecIdsDS, vecTypeClass, pathFileSave, 0)  