# -*- coding: utf-8 -*-
"""
Change the unit of GeoNet structural analysis files for QUAKE/W
The unit of the GeoNet file is in mm/s2.
The unit needs to be converted to cm/s2 for QUAKE/W.

V2A files from GeoNet is not suitable to be opened using programs like excel,
so the files need to be converted using CSV Conversion Program from GeoNet.
https://www.geonet.org.nz/data/supplementary/strong_motion_file_formats
After the conversion was finished,
the second and third columns are for horizontal acceleration in mm/s2.
The record starts from the 6th row. 
The timestep is 0.005s but it needs to be checked as that is not the always the case.

"""


import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


def CheckData(fileName):

    pList = []
    H1List = []
    H2List = []
    timeList = []
    timeStep = 0.005
    timeCounter = 0

    with open(fileName, mode="r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if isfloat(row[0]):#Ignore the first 5 lines without numbers               
                pList.append(float(row[0]))
                H1List.append(float(row[1])/10)#Converting mm/s2 to cm/s2
                H2List.append(float(row[2])/10)#Converting mm/s2 to cm/s2
                timeList.append(timeCounter)
                timeCounter += timeStep
    

    #Preparing lists to create a modified csv file.
    

                
        name = fileName.split("_")[2]
        
        plt.plot(timeList, H1List, label = name + " H1", linewidth = 0.5)
        plt.plot(timeList, H2List, label = name + " H2", linewidth = 0.5)
        #plt.plot(pList, H1List, label = name + " H1")
        #plt.plot(pList, H2List, label = name + "H2")
    


    
    

#=====================Main==========================

fig = plt.figure(dpi = 300)
plt.xlim(0, 300)
#plt.xlim(0, 10)

#ax = fig.add_subplot(111)
#plt.subplots.xaxis.set_major_locator(MultipleLocator(20))
#plt.subplots.yaxis.set_major_locator(MultipleLocator(20))
#ax.xaxis.set_major_locator(MultipleLocator(50))
#ax.yaxis.set_major_locator(MultipleLocator(50))

#ax.xaxis.set_minor_locator(AutoMinorLocator(10))
#ax.yaxis.set_minor_locator(AutoMinorLocator(10))


CheckData("20161113_110330_TEPS_20_V2A.csv")
#CheckData("20161113_110336_PIPS_20_V2A.csv")
#CheckData("20161113_110333_FKPS_20_V2A.csv")
#CheckData("20161113_110330_VUWS_20_V2A.csv")
#CheckData("20161113_110330_TFSS_20_V2A.csv")




plt.grid()
plt.legend()
plt.xlabel("Time(sec)")
plt.ylabel("Acceleration(cm/s2)")
#plt.title(name + " Comparison")

print("finished")

