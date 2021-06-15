# -*- coding: utf-8 -*-
"""

Edit PSA file from GeoNet. 
2nd column period(s), 4th column horizontal PSA 1(m/s2), 5th column horizontal PSA 2(m/s2). The horizontal PSA 1 and 2 need to be in unit g, divide m/s2 by 9.81m/s2 to get g.
The first 4 rows describe the format of the data, and the actual record starts from the 5th row.
The period of the data is from 0.025s to 10s.
Interpolate PSA files using python "Interpolator" script.
Create a python script to compare PSA from different strong motion stations(SMS).



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
        H1List = []
        H2List = []
        
        newPList = []
        newH1List = []
        newH2List = []
        
        g = 9.81 #m/s2

        #Opening CSV file with data which needs to be interpolated
        with open(fileName, mode="r", newline='') as f:
            reader = csv.reader(f)
            for row in reader:               
                #Ignore comments in the file
                if row[0][0] != "#":
                    #This ignores the first row with strings
                    if isfloat(row[1]):
                        pList.append(float(row[1])) 
                        H1List.append(float(row[3])/g)#Convert m/s2 to g
                        H2List.append(float(row[4])/g)#Convert m/s2 to g                   

        #Creating interpolation function
        funcH1 = interp1d(pList, H1List)
        funcH2 = interp1d(pList, H2List)
        
        #print(pList)
        #print(H1List)
        #print(H2List)
        
        #for the first period 0.025.
        newPList.append(pList[0])
        newH1List.append(H1List[0])
        newH2List.append(H2List[0])
        
        #Interpolate only in 2nd decimal place(no 0.005 etc.).
        i = 0.03
        
        while i <= 10:
            newPList.append(i)
            newH1List.append(funcH1(i))
            newH2List.append(funcH2(i))
            #print((round(i, 3), funcH1(i).round(4), funcH2(i).round(4)))
            i += 0.01
            i = round(i,3)#while using float is unstable, so round it.
            
        
        #print(newPList)
        
        #plt.figure(dpi = 1200)
        #"plt.plot(pList, H1List, "-b", newPList, newH1List, "o")
        #"plt.plot(pList, H2List, "-r", newPList, newH2List, "o")
        #plt.xlim([0, 10])
        
        #Preparing lists to create a modified csv file.
        
        rows = zip(newPList, newH1List, newH2List)
        name = fileName.split("_")[2]#removing .csv
        #print(name)
        with open(name + "_Interpolated.csv", mode="w", newline='') as myFile:
            fileWriter = csv.writer(myFile)
            for row in rows:
                fileWriter.writerow(row)
        

#=====================Main==========================
interpolator = Interpolator("20161113110256_NZ_FKPS_20HN_BP4_0.025_80.psa5.csv")
interpolator = Interpolator("20161113110256_NZ_PIPS_20HN_BP4_0.025_80.psa5.csv")
interpolator = Interpolator("20161113110256_NZ_TEPS_20HN_BP4_0.025_80.psa5.csv")
interpolator = Interpolator("20161113110256_NZ_TFSS_20HN_BP4_0.025_80.psa5.csv")
interpolator = Interpolator("20161113110256_NZ_VUWS_20HN_BP4_0.025_80.psa5.csv")