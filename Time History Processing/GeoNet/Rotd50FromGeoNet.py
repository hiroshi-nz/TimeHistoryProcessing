# -*- coding: utf-8 -*-
"""
Find why minimum period is 0.1s...

The timestep of a file from GeoNet is 0.005s.
4th and 5th columns are the horizontal components. 
The data starts from the data starts from 5th row. 
The unit is in m/s2, so divide them by 9.81m/s2 to convert the unit into g.

This script is most time consuming and processor intensive.
It takes time to complete.

RotD50FromGeoNet -> InterpolatorFromPython -> Comparison(to check) or RotDComparison
Raw file         -> _RotD50.csv            -> _RotD50_Interpolated.csv

"""

import matplotlib.pyplot as plt
import numpy as np
import csv
import pyrotd
import time


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

#pyrotd.processes = 1

class RotD:
    def __init__(self, fileName):
        
        pList = []
        H1List = []
        H2List = []
        
        g = 9.81 #m/s2
        counter = 0.000

        #Opening CSV file with data which needs to be interpolated
        with open(fileName, mode="r", newline='') as f:
            reader = csv.reader(f)
            for row in reader:               
                #Ignore comments in the file
                if row[0][0] != "#":
                    #This ignores the first row with strings
                    if isfloat(row[3]):
                        pList.append(counter)
                        H1List.append(float(row[3])/g)#Convert m/s2 to g
                        H2List.append(float(row[4])/g)#Convert m/s2 to g                   
                        counter += 0.005
        
        #Interpolate only in 2nd decimal place(no 0.005 etc.).
        """
        i = 0.0000001       
        
        oscFreqs = []
        
        while i <= 10:
            oscFreqs.append(i)
            i += 0.01        
        """
        timeStep = 0.005
        oscDamping = 0.05 #5%
        oscFreqs = np.logspace(-1, 2, 300)
        #oscFreqs = np.logspace(-4, 1, 200)
        
        spectrumH1 = pyrotd.calc_spec_accels(timeStep, H1List, oscFreqs, oscDamping)
        spectrumH2 = pyrotd.calc_spec_accels(timeStep, H2List, oscFreqs, oscDamping)
        
        rotatedResp = pyrotd.calc_rotated_spec_accels(timeStep, H1List, H2List,
                                                       oscFreqs, oscDamping, percentiles=[50],)

        
        #Convert frequency to period
        for x in spectrumH1:
            x[0] = 1 / x[0]
            
        #Convert frequency to period
        for x in spectrumH2:
            x[0] = 1 / x[0]
        
        #Convert frequency to period
        for x in rotatedResp:
            x[0] = 1 / x[0]
            
        
        selectedResp = rotatedResp[rotatedResp.percentile == 50]

        """
        plt.figure(dpi = 1200)
        plt.plot(selectedResp.osc_freq, selectedResp.spec_accel, "-r")
        plt.plot(spectrumH1.osc_freq, spectrumH1.spec_accel, "--y")
        plt.plot(spectrumH1.osc_freq, spectrumH2.spec_accel, "--b")
        #print(selectedResp.osc_freq)

        plt.xlabel("Period(sec)")
        plt.ylabel("5% Damping Spectral Acceleration(g)")
        plt.xlim(0, 10)
        plt.grid()
        """
   
        SAPeriodList = selectedResp.osc_freq.tolist()
        RotDList = selectedResp.spec_accel.tolist()
        SAH1List = spectrumH1.spec_accel.tolist()
        SAH2List = spectrumH2.spec_accel.tolist()
        
        SAPeriodList.reverse()
        RotDList.reverse()
        SAH1List.reverse()
        SAH2List.reverse()
        
     
        #Preparing lists to create a modified csv file. 
        #rows = zip(selectedResp.osc_freq, selectedResp.spec_accel, spectrumH1.spec_accel, spectrumH2.spec_accel)
        rows = zip(SAPeriodList, RotDList,  SAH1List, SAH2List)
        name = fileName.split("_")[2]#removing .csv
        #print(name)
        with open(name + "_RotD50.csv", mode="w", newline='') as myFile:
            fileWriter = csv.writer(myFile)
            for row in rows:
                fileWriter.writerow(row)


#=====================Main==========================

startTime = time.time()
rotD = RotD("20161113110256_NZ_FKPS_20HN_BP4_0.025_80.filtered.csv")
rotD = RotD("20161113110256_NZ_PIPS_20HN_BP4_0.025_80.filtered.csv")
rotD = RotD("20161113110256_NZ_TEPS_20HN_BP4_0.025_80.filtered.csv")
rotD = RotD("20161113110256_NZ_TFSS_20HN_BP4_0.025_80.filtered.csv")
rotD = RotD("20161113110256_NZ_VUWS_20HN_BP4_0.025_80.filtered.csv")
elapsedTime = time.time() - startTime
print("Elapsed Time " + str(round(elapsedTime, 3)) + "s")

print("finished")

