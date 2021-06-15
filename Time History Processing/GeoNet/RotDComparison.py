# -*- coding: utf-8 -*-
"""

This file compares multiple spectral acceleration calculated by Python.

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


def Comparison(fileName, plot):
    
    pList = []
    rotDList = []   

    with open(fileName, mode="r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            
            pList.append(float(row[0]))
            rotDList.append(float(row[1]))        
            
    name = fileName.split("_")[0]
    plot.plot(pList, rotDList, label = name + " RotD50")
           
#=====================Main==========================
plt.figure(dpi = 1200)
plt.xlim(0, 3)
        



Comparison("FKPS_RotD50_Interpolated.csv", plt)
Comparison("PIPS_RotD50_Interpolated.csv", plt)
Comparison("TEPS_RotD50_Interpolated.csv", plt)
Comparison("TFSS_RotD50_Interpolated.csv", plt)
Comparison("VUWS_RotD50_Interpolated.csv", plt)


plt.xlabel("Period(sec)")
plt.ylabel("5% Damping Spectral Acceleration(g)")
plt.title("RotD50 Comparison")

plt.grid()
plt.legend()

print("finished")

