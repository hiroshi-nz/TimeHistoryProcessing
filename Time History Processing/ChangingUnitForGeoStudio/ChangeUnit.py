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


def ChangeUnit(fileName):

    pList = []
    H1List = []
    H2List = []

    with open(fileName, mode="r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if isfloat(row[0]):#Ignore the first 5 lines without numbers               
                pList.append(float(row[0]))
                H1List.append(float(row[1])/10)#Converting mm/s2 to cm/s2
                H2List.append(float(row[2])/10)#Converting mm/s2 to cm/s2
                timeList.append(counter)
    
    #Preparing lists to create a modified csv file.
    
    plt.figure(dpi = 1200)
    #plt.xlim(0, 10)
    #plt.xlim(0, 10)
            
    #plt.plot(pList, H1List, "-r", label = "H1")
    plt.plot(pList, H2List, "-b", label = "H2")

    plt.xlabel("Time(sec)")
    plt.ylabel("Acceleration(cm/s2)")
    name = fileName.split("_")[0]
    #plt.title(name + " Comparison")

    plt.grid()
    plt.legend()
    
    

    #Adding the header for QUAKE/W
    H1List.insert(0,"===============================================")
    H1List.insert(1,"1	1	0.005")
    H1List.insert(2,"===============================================")
    
    H2List.insert(0,"===============================================")
    H2List.insert(1,"1	1	0.005")
    H2List.insert(2,"===============================================")
            
    
    rows = zip(H1List)
    name = fileName.split("_")[2]
    with open(name + "_CentimetrePerSecondSquared_H1.acc", mode="w", newline='') as myFile:
        fileWriter = csv.writer(myFile)
        for row in rows:
            fileWriter.writerow(row)
    
    rows = zip(H2List)
    with open(name + "_CentimetrePerSecondSquared_H2.acc", mode="w", newline='') as myFile:
        fileWriter = csv.writer(myFile)
        for row in rows:
            fileWriter.writerow(row)
    

#=====================Main==========================
#ChangeUnit("20161113_110330_TEPS_20_V2A.csv")
#ChangeUnit("20161113_110336_PIPS_20_V2A.csv")
#ChangeUnit("20161113_110333_FKPS_20_V2A.csv")
#ChangeUnit("20161113_110330_VUWS_20_V2A.csv")
#ChangeUnit("20161113_110330_TFSS_20_V2A.csv")
print("finished")

