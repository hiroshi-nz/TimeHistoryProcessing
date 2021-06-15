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


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


def CheckData(fileName, fileName2):

    tList = []
    H1AList = []
    H1VList = []
    H1DList = []
    
    H2AList = []
    H2VList = []
    H2DList = []
    

    timeStep = 0.005
    timeCounter = 0

    rowCounter = 0
    timeCounter = 0

    with open(fileName, mode="r", newline='') as f:
        reader = csv.reader(f, delimiter = ' ', skipinitialspace=True)
        for row in reader:
            if rowCounter < 5760:
                i = 0
                while i < 10:
                    H1AList.append(float(row[i]))
                    i += 1
            elif rowCounter < 11520:
                i = 0
                while i < 10:
                    H1VList.append(float(row[i]))
                    i += 1
            elif rowCounter < 17280:
                i = 0
                while i < 10:
                    H1DList.append(float(row[i]))
                    i += 1  
            rowCounter += 1
            
    rowCounter = 0
    with open(fileName2, mode="r", newline='') as f:
        reader = csv.reader(f, delimiter = ' ', skipinitialspace=True)
        for row in reader:
            if rowCounter < 5760:
                i = 0
                while i < 10:
                    H2AList.append(float(row[i]))
                    i += 1
            elif rowCounter < 11520:
                i = 0
                while i < 10:
                    H2VList.append(float(row[i]))
                    i += 1
            elif rowCounter < 17280:
                i = 0
                while i < 10:
                    H2DList.append(float(row[i]))
                    i += 1  
            rowCounter += 1
            
    while timeCounter < 57600:
        tList.append(timeCounter * timeStep)
        timeCounter += 1
          
    #print(len(H1AList))
    #print(len(H1VList))
    #print(len(H1DList))
    #print(tList)
    #print(H1AList)
    print(len(H2AList))
                     
    plt.plot(tList, H1AList, linewidth = 0.5)
    plt.plot(tList, H2AList, linewidth = 0.5)
    

#=====================Main==========================


fig = plt.figure(dpi = 300)
plt.xlim(0, 300)

CheckData("1st.txt", "2nd.txt")


print("finished")

