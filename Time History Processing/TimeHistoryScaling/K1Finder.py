# -*- coding: utf-8 -*-
"""
This script find k1 value from CSV file.

The CSV file needs to be formatted as follows(H stands for horizontal),
period, target H1, target H2, component H1, component H2.

k1 calculation is mathematically a bit complicated,
therefore, there might be error, so it needs to be verified.
There are ways to check k and d relationship using a graph.
That needs to be fully utilized to find validity of the script.

"""

import numpy as np
import csv
import matplotlib.pyplot as plt
import math




#Period records need to be from Tmin to Tmax before using this class
#This part find optimum k value which minimize D for one pair of target and component horizontal data.
#This part needs to be repeated 4 times to find the minimum k value.
class KDFinder:
    def __init__(self, T, periodList, targetHList, componentHList, kLower, kUpper):
        """
        self.Tmin = 0.4 * T
        if 1.3 * T < 0.4:#the Tmax cannot be lower than 0.4
            self.Tmax = 0.4
        else:
            self.Tmax = 1.3 * T
        """
    #def findOptimumK(self, T, periodList, targetHList, componentHList, kLower, kUpper):
        
        kList = []#this will be plotted against dList
        dList = []
        k = kLower
        while k < kUpper:
            #create loglist of sa component/target between Tmin and Tmax.
            logSquaredList = []
            j = 0
            while j < len(periodList):
                #in python, log is for ln be careful!
                ans = math.log10((k*componentHList[j])/targetHList[j])**2
                logSquaredList.append(ans)
            
                j += 1
            
            #calculating the inside of the square root
            eq1 = 1/((1.3-0.4)*T)
            eq2 = np.trapz(logSquaredList, periodList)#integration using trapedoizal rule
            
            #this is D value
            d = math.sqrt(eq1*eq2)
            #print(k)
            #print(d)
            kList.append(k)
            dList.append(d)
            k += 0.005
        
    
        
        self.minD = min(dList)
        self.minDIndex =dList.index(self.minD)
        self.optK = kList[self.minDIndex]
        
        self.kList = kList
        self.dList = dList
        
        print("the optimum k value is " + str(round(self.optK, 3)) + "  minimum D value is " + str(round(self.minD, 4))) 
        
    def print(self):
        print("the optimum k value is " + str(round(self.optK, 3)) + "  minimum D value is " + str(round(self.minD, 4))) 


#dependant on KDFinder.
#Compares different optium k values and find minimum k value, which is k1.
#The CSV file needs to be formatted as follows(H stands for horizontal),
# period, target H1, target H2, component H1, component H2.
class K1Finder:
    def __init__(self, fileName):
        
        pList = []
        targetH1List = []#target
        targetH2List = []
        
        componentH1List = []#component
        componentH2List = []
        
        with open(fileName, mode="r", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                pList.append(float(row[0]))
                targetH1List.append(float(row[1]))
                targetH2List.append(float(row[2]))
                componentH1List.append(float(row[3]))
                componentH2List.append(float(row[4]))
        
        #check if data is properly loaded or not using graph
        #plt.plot(pList, h1List, "-b", pList, h2List, "-r",pList, h1List2, "-g", pList, h2List2, "-y")
        
        
        T = 0.4
        #Tmin = 0.16
        #Tmax = 0.52
        
        kLower = 0.01
        kUpper = 1
        kdFinder1 = KDFinder(T, pList, targetH1List, componentH1List, kLower, kUpper)
        kdFinder2 = KDFinder(T, pList, targetH2List, componentH2List, kLower, kUpper)
        kdFinder3 = KDFinder(T, pList, targetH2List, componentH1List, kLower, kUpper)
        kdFinder4 = KDFinder(T, pList, targetH1List, componentH2List, kLower, kUpper)
        
        optimumKList = []
        
        optimumKList.append(kdFinder1.optK)
        optimumKList.append(kdFinder2.optK)
        optimumKList.append(kdFinder3.optK)
        optimumKList.append(kdFinder4.optK)

        self.k1 = min(optimumKList)
        print("the k1 value is " + str(round(self.k1, 3)) + " and the list number is " + str(optimumKList.index(self.k1) + 1))

        logCriteria = []# for the log1.5 criteria
        #print(math.log10(1.5))
        i = 0
        while i < len(kdFinder1.kList):
            logCriteria.append(math.log10(1.5))
            i += 1

        plt.plot(kdFinder1.kList, kdFinder1.dList, "-b", kdFinder2.kList, kdFinder2.dList, "-r", kdFinder3.kList, kdFinder3.dList, "-g", kdFinder4.kList, kdFinder4.dList, "-c", kdFinder1.kList, logCriteria, "--y")
        plt.xlabel("k value")
        plt.ylabel("D value")
        plt.ylim(0, math.log10(1.5) + 0.2)

#====================Main==========================-
#k1Finder = K1Finder("combined.csv")
#k1Finder = K1Finder("RSN1176Ready.csv")#k1value = 0.595
#k1Finder = K1Finder("RSN6889Ready.csv")#k1value = 0.715
k1Finder = K1Finder("RSN8161Ready.csv")#k1value = 0.395
