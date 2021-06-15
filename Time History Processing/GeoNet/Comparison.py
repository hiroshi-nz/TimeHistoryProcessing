# -*- coding: utf-8 -*-
"""

This file compares spectral acceleration calculated by GeoNet and Python.

RotD50FromGeoNet -> InterpolatorFromPython -> Comparison(to check) or RotDComparison
Raw file         -> _RotD50.csv            -> _RotD50_Interpolated.csv

"""

import matplotlib.pyplot as plt
import csv


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

#pyrotd.processes = 1

class Comparison:
    def __init__(self, fileName, fileName2):
        
        pList = []
        rotDList = []
        H1List = []
        H2List = []
        
        pList2 = []
        H1List2 = []
        H2List2 = []
        

        with open(fileName, mode="r", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                
                pList.append(float(row[0]))
                rotDList.append(float(row[1]))     
                H1List.append(float(row[2]))
                H2List.append(float(row[3]))

        with open(fileName2, mode="r", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                
                pList2.append(float(row[0]))    
                H1List2.append(float(row[1]))
                H2List2.append(float(row[2]))                    


        plt.figure(dpi = 1200)
        plt.xlim(0, 10)
        #plt.xlim(0, 10)
                
        plt.plot(pList, rotDList, "-c", label = "Computed RotD50")
        plt.plot(pList, H1List, "-y", label = "Computed SA H1")
        plt.plot(pList, H2List, "-b", label = "Computed SA H2")
        plt.plot(pList2, H1List2, "--g", label = 'GeoNet SA H1')
        plt.plot(pList2, H2List2, "--r", label = "GeoNet SA2 H2")
        

        plt.xlabel("Period(sec)")
        plt.ylabel("5% Damping Spectral Acceleration(g)")
        name = fileName.split("_")[0]
        plt.title(name + " Comparison")

        plt.grid()
        plt.legend()
        
        

#=====================Main==========================

#comparison = Comparison("PIPS_RotD50.csv", "PIPS_Interpolated.csv")
comparison = Comparison("FKPS_RotD50_Interpolated.csv", "FKPS_Interpolated.csv")
comparison = Comparison("PIPS_RotD50_Interpolated.csv", "PIPS_Interpolated.csv")
comparison = Comparison("TEPS_RotD50_Interpolated.csv", "TEPS_Interpolated.csv")
comparison = Comparison("TFSS_RotD50_Interpolated.csv", "TFSS_Interpolated.csv")
comparison = Comparison("VUWS_RotD50_Interpolated.csv", "VUWS_Interpolated.csv")
print("finished")

