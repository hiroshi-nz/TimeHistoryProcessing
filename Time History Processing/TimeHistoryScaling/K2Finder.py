# -*- coding: utf-8 -*-
"""
This script find k2 by at first calculating differences
between target record and component record which was multiplied by k1.
The differences will be calculated for 
2 x 2 combinations(2 target and 2 component horizontal) 
and minimum k1 will be picked.

That part will be repeated for all three records, then the ultimate minimum
k2 will be chosen.

The requirement of NZS1170.5 is at least one of records need to exceed 
the values between 0.4T and 1.3T.

By finding the ultimate minimum k2, 
it ensures one component will meet this criteria.

"""

import csv
import matplotlib.pyplot as plt


class K2Finder:
    def __init__(self, fileName, k1):
        
        pList = []
        targetH1List = []#target
        targetH2List = []
        
        componentH1List = []#component
        componentH2List = []
        differenceList1 = []
        differenceList2 = []
        differenceList3 = []
        differenceList4 = []
        
        with open(fileName, mode="r", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                pList.append(float(row[0]))
                targetH1List.append(float(row[1]))
                targetH2List.append(float(row[2]))
                newH1 = float(row[3])*k1
                newH2 = float(row[4])*k1
                
                componentH1List.append(newH1)
                componentH2List.append(newH2)
                differenceList1.append(newH1 - float(row[1]))
                differenceList2.append(newH2 - float(row[1]))
                differenceList3.append(newH1 - float(row[2]))
                differenceList4.append(newH2 - float(row[2]))
                       
        k2List = []
                
        index = differenceList1.index(min(differenceList1))
        k2List.append(targetH1List[index] / componentH1List[index])
        
        index = differenceList2.index(min(differenceList2))
        k2List.append(targetH1List[index] / componentH2List[index])
        
        index = differenceList3.index(min(differenceList3))
        k2List.append(targetH2List[index] / componentH1List[index])
        
        index = differenceList4.index(min(differenceList4))
        k2List.append(targetH2List[index] / componentH2List[index])
        
        
        self.k2 = min(k2List)
                
        k2AdjustedComponentH1List = []

        for entry in componentH1List:
            k2AdjustedComponentH1List.append(entry * self.k2 )

        k2AdjustedComponentH2List = []
        
        for entry in componentH2List:
            k2AdjustedComponentH2List.append(entry * self.k2 )
        
        
        print(k2List, round(self.k2, 3))
        plt.plot(pList, targetH1List, pList, k2AdjustedComponentH1List, pList, componentH1List)
        plt.plot(pList, k2AdjustedComponentH2List, pList, componentH2List)
        #plt.plot(pList, targetH1List, "-b", pList, targetH2List, "-r", pList, componentH1List, "-g", pList, componentH2List, "-c")
        #plt.plot(pList, differenceList1, "-b", pList, differenceList2, "-r", pList, differenceList3, "-g", pList, differenceList4, "-c")
        plt.xlabel("second")
        plt.ylabel("g")

#====================Main==========================-

finalK2List = []
k2Finder = K2Finder("RSN1176Ready.csv", 0.715)#k1value = 0.595
finalK2List.append(k2Finder.k2)
k2Finder = K2Finder("RSN6889Ready.csv", 0.715)#k1value = 0.715
finalK2List.append(k2Finder.k2)
k2Finder = K2Finder("RSN8161Ready.csv", 0.395)#k1value = 0.395
finalK2List.append(k2Finder.k2)
print("k2 is " + str(round(min(finalK2List), 3)))#k2value = 1.001
