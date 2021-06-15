# -*- coding: utf-8 -*-
"""
RotD50FromGeoNet -> InterpolatorFromPython -> Comparison(to check) or RotDComparison
Raw file         -> _RotD50.csv            -> _RotD50_Interpolated.csv

"""

from scipy.interpolate import interp1d
import csv
import matplotlib.pyplot as plt

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


class Interpolator:
    def __init__(self, fileName):# t is fundametal period
        
        pList = []
        rotDList = []
        H1List = []
        H2List = []
        
        newPList = []
        newRotDList = []
        newH1List = []
        newH2List = []
        

        #Opening CSV file with data which needs to be interpolated
        with open(fileName, mode="r", newline='') as f:
            reader = csv.reader(f)
            for row in reader:               
                pList.append(float(row[0]))
                rotDList.append(float(row[1]))
                H1List.append(float(row[2]))
                H2List.append(float(row[3]))               

        #Creating interpolation function
        funcRotD = interp1d(pList, rotDList)
        funcH1 = interp1d(pList, H1List)
        funcH2 = interp1d(pList, H2List)
        
        
        #Needs to round and manually add the first elements because of float instability.
        newPList.append(round(pList[0],3))
        newRotDList.append(rotDList[0])
        newH1List.append(H1List[0])
        newH2List.append(H2List[0])
        
        i = 0.11
        while i <= 10:
            newPList.append(i)
            newRotDList.append(funcRotD(i))
            newH1List.append(funcH1(i))
            newH2List.append(funcH2(i)) 
            i += 0.01
            i = round(i,3)#while using float is unstable, so round it.
            
        
        #Preparing lists to create a modified csv file.
        
        rows = zip(newPList, newRotDList, newH1List, newH2List)
        name = fileName.split(".")[0]#removing .csv
        #print(name)
        with open(name + "_Interpolated.csv", mode="w", newline='') as myFile:
            fileWriter = csv.writer(myFile)
            for row in rows:
                fileWriter.writerow(row)
        

#=====================Main==========================
interpolator = Interpolator("FKPS_RotD50.csv")
interpolator = Interpolator("PIPS_RotD50.csv")
interpolator = Interpolator("TEPS_RotD50.csv")
interpolator = Interpolator("TFSS_RotD50.csv")
interpolator = Interpolator("VUWS_RotD50.csv")
print("finished")

