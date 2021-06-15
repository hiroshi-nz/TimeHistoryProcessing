# -*- coding: utf-8 -*-
"""

These series of python scripts scale time history record to
target time history record following NZS1170.5.
Currently, this is under-development and there might be mistakes.
So caution will be required.

These scripts are used in following sequence,

Interpolator -> K1Finder -> K2Finder -> FinalScalingWholeRange


Horizontal components need to be interpolated to match the period of
target record and component records.

Without matching period, it is quite difficult to calculate k1.

In this script, time history records with different period will be adjusted
to have same internals(0.01s).

The script reads a CSV file and creates a modified CSV file 
with 0.01s intervals. The file name will be appended with "Interpolated".
 
Interpolator class only interpolate between 0.4T and 1.3T.
(T is fundamental period)

After Interpolator, use K1Finder to find k1.


"""

from scipy.interpolate import interp1d
#import numpy
import csv
import matplotlib.pyplot as plt

class Interpolator:
    def __init__(self, fileName, T):# t is fundametal period
        
        pList = []
        H1List = []
        H2List = []
        
        newPList = []
        newH1List = []
        newH2List = []
        

        #Opening CSV file with data which needs to be interpolated
        with open(fileName, mode="r", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                pList.append(float(row[0]))
                H1List.append(float(row[1]))
                H2List.append(float(row[2]))

        #Creating interpolation function
        funcH1 = interp1d(pList, H1List)
        funcH2 = interp1d(pList, H2List)
        
        self.Tmin = 0.4 * T
        if 1.3 * T < 0.4:#the Tmax cannot be lower than 0.4
            self.Tmax = 0.4
        else:
            self.Tmax = 1.3 * T

        #Interpolating between Tmin and Tmax
        i = self.Tmin
        while i < self.Tmax:
            print((round(i, 3), funcH1(i).round(4), funcH2(i).round(4)))
            newPList.append(i)
            newH1List.append(funcH1(i))
            newH2List.append(funcH2(i))
            i += 0.01
        #Float in python is unstable and the last decimal number fluctuate.
        #Because of that, I need to append the final element manually.
        newPList.append(self.Tmax)
        newH1List.append(funcH1(self.Tmax))
        newH2List.append(funcH2(self.Tmax))
        print(self.Tmax, funcH1(self.Tmax).round(4), funcH2(self.Tmax).round(4))
        
        plt.plot(pList, H1List, "-b", newPList, newH1List, "o")
        plt.plot(pList, H2List, "-r", newPList, newH2List, "o")
        plt.xlim([self.Tmin, self.Tmax])
        
        #Preparing lists to create a modified csv file.
        
        rows = zip(newPList, newH1List, newH2List)
        name = fileName.split(".", 1)[0]#removing .csv
        print(name)
        with open(name + "Interpolated.csv", mode="w", newline='') as myFile:
            fileWriter = csv.writer(myFile)
            for row in rows:
                fileWriter.writerow(row)

#=====================Main==========================
interpolator = Interpolator("kaikoura.csv", 0.4)
#interpolator = Interpolator("RSN1176.csv", 0.4)
#interpolator = Interpolator("RSN6889.csv", 0.4)
#interpolator = Interpolator("RSN8161.csv", 0.4)
