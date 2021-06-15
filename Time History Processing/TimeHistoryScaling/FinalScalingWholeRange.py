# -*- coding: utf-8 -*-
"""

This script scale time history records using k1 and k2.
Those values are needed to be find using K1Finder and K2Finder scripts.

As the output, this script creates a CSV file
with multiple time history records.
However, those time history records need to have identical period,
and if that is not the case, it will produce a file with inaccuracy.

If the target record has different period, that needs to be added to
the final csv manually using Excel. 

"""

import csv
import matplotlib.pyplot as plt


class FinalScaler:
    def __init__(self, fileName, k1, k2):
        
        pList = []        
        scaledH1List = []#component
        scaledH2List = []

        
        with open(fileName, mode="r", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                pList.append(float(row[0]))
                scaledH1List.append(float(row[1])*k1*k2)
                scaledH2List.append(float(row[2])*k1*k2)
                               

        
        plt.plot(pList, scaledH1List, "--", pList, scaledH2List, "--")
        plt.xlabel("second")
        plt.ylabel("g")
        
        rows = zip(pList, scaledH1List, scaledH2List)
        name = fileName.split("Ready.", 1)[0]#removing .csv
        print(name)
        with open(name + "Final.csv", mode="w", newline='') as myFile:
            fileWriter = csv.writer(myFile)
            for row in rows:
                fileWriter.writerow(row)
                
        self.scaledH1List = scaledH1List
        self.scaledH2List = scaledH2List
        self.pList = pList        
                
    def plotTarget(self, fileName):
        
        pList = []        
        targetH1List = []
        targetH2List = []
        
        with open(fileName, mode="r", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                pList.append(float(row[0]))
                targetH1List.append(float(row[1]))
                targetH2List.append(float(row[2]))
                
        plt.plot(pList, targetH1List, pList, targetH2List)
        
        self.targetpList = pList
        self.targetH1List = targetH1List
        self.targetH2List = targetH2List
        
#====================Main==========================-
plt.figure(dpi = 300)
#plt.xlim(0, 5)
plt.xlim(0.16, 0.52)
k2 = 1.001# k2 is from RSN1176
k2Finder1 = FinalScaler("RSN1176.csv", 0.715, k2)#k1value = 0.595
k2Finder2 = FinalScaler("RSN6889.csv", 0.715, k2)#k1value = 0.715
k2Finder3 = FinalScaler("RSN8161.csv", 0.395, k2)#k1value = 0.395
k2Finder1.plotTarget("kaikoura.csv")

#rows = zip(k2Finder1.targetpList, k2Finder1.targetH1List, k2Finder1.targetH2List, k2Finder1.pList, k2Finder1.scaledH1List, k2Finder1.scaledH2List, k2Finder2.scaledH1List, k2Finder2.scaledH2List, k2Finder3.scaledH1List, k2Finder3.scaledH2List)
rows = zip(k2Finder1.pList, k2Finder1.scaledH1List, k2Finder1.scaledH2List, k2Finder2.scaledH1List, k2Finder2.scaledH2List, k2Finder3.scaledH1List, k2Finder3.scaledH2List)

with open("FinalCombined.csv", mode="w", newline='') as myFile:
    fileWriter = csv.writer(myFile)
    for row in rows:
        fileWriter.writerow(row)
