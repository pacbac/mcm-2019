#import scripts\searchDrugCounty
#assume directory mcm-2019
import os, sys
ROOT_WDIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT_WDIR)
from Classes.county import *
import math

getAllCounties()
#findScores corresponding to a drug. Returs a dictionary that maps cnty to its score (DOESN'T CONTAIN ALL COUNTIES)
def findScores(drug):
    
    counties = []
    year = County.yearDrugBegan(allCounties,drug) #to consider only counties that had earliest outbreaks
    
    for e in County.countiesUseDrug(allCounties,drug): #consider only counties that used the drug:
        if year in e.m_drugList[drug]:
            counties.append(e)
    score = {}
    for cnty in counties:
        score[cnty] = getScore(counties,cnty,drug,year)
    return score

#get Score for a single county
def getScore(all,cnty, drug,year):
    otherCounties = []
    for e in all:
        if e != cnty:
            otherCounties.append(e)
    if otherCounties:
        return sumSpatialFactors(cnty,drug,year,otherCounties) + sumTime(cnty,drug)
       
    #if only one county then we assign 0            
    return 0.0

#sum up function that models spatial factors
def sumSpatialFactors(cnty,drug,year,otherCounties):
   return County.sumPop(metaFunc(cnty,drug,year),drug,year,otherCounties)

#sum up time factors
def sumTime(cnty,drug):
    n = 0
    sum = 0.0
    dlt = 0.8
    for e in cnty.m_drugList[drug]:
         sum = sum + (dlt**n)*math.log(cnty.m_drugList[drug][e])
         n = n + 1
    return sum


#meta function that returns a function such that sumpop can be evaluated for each cnty
def metaFunc(cnty,drug,year):
    return lambda x : math.log(
    (
        (cnty.drugCases(drug,year)) / 
        (x.drugCases(drug,year)) + 1
    ) **(1/(1+ 25 * cnty.distanceTo(x)))
)

#function finds the probable origin of drug in the given state
def findStateOrigin(state,drug):
    scores = findScores(drug)
    stateScores = {}
    for e in scores:
        if e.m_state == state:
            stateScores[e] = scores[e]
    
    if stateScores:
        return sorted(stateScores.items(),  key=(lambda x : x[1]))  [-1]
    return "no instate origin"

#function finds greatest drug uses in input state and writes them to         
def findAlldrugsOrigin(state):
    
        d = {}
        for drug in allCounties[0].drugNames():
            top = findStateOrigin(state,drug)
            if isinstance(top, str):
                d[drug] = top
            else:
                d[drug] = top[0].m_name+ ' ' + str(top[1])
        return d

#function that finds the origin of all drugs in all states       
def findAllStateOrigin():
    with open(ROOT_WDIR + "/generated_data/countyRank_model_state_origin.csv", mode='w') as out_file:
        writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fieldns = allCounties[0].drugNames()
        dwriter = csv.DictWriter(out_file,fieldnames=fieldns) 
        for St in STATE_CODES:
            writer.writerow([ '','',St])
            d = findAlldrugsOrigin(STATE_CODES[St])
            
            writer.writerow(fieldns)
            dwriter.writerow(d)



findAllStateOrigin()


