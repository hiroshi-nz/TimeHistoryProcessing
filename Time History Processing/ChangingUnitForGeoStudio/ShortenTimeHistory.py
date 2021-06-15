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


def ShortenTimeHistoryRecord(fileName, startTime, endTime):

    H1List = []
    H2List = []

    timeStep = 0.005
    startIndex = int(startTime/timeStep)
    endIndex = int(endTime/timeStep)
    
    newH1List = []
    newH2List = []
    timeList = []
    timeCounter = 0
    
    with open(fileName, mode="r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if isfloat(row[0]):#Ignore the first 5 lines without numbers               
                H1List.append(float(row[1])/10)#Converting mm/s2 to cm/s2
                H2List.append(float(row[2])/10)#Converting mm/s2 to cm/s2           
               

    i = startIndex
    while i < endIndex:
        newH1List.append(H1List[i])
        newH2List.append(H2List[i])
        timeList.append(timeCounter)
        timeCounter += timeStep
        i += 1
     
        
    print(startIndex, endIndex, len(newH1List), len(H1List))
          
    plt.figure(dpi = 200)
    plt.xlim(0, endTime - startTime)
            
    plt.plot(timeList, newH1List, "-r", label = "H1")
    plt.plot(timeList, newH2List, "-b", label = "H2")

    plt.xlabel("Time(sec)")
    plt.ylabel("Acceleration(cm/s2)")
    name = fileName.split("_")[0]
    #plt.title(name + " Comparison")

    plt.grid()
    plt.legend()
    
    

    #Adding the header for QUAKE/W
    newH1List.insert(0,"===============================================")
    newH1List.insert(1,"1	1	0.005")
    newH1List.insert(2,"===============================================")
    
    newH2List.insert(0,"===============================================")
    newH2List.insert(1,"1	1	0.005")
    newH2List.insert(2,"===============================================")
            
    
    rows = zip(newH1List)
    name = fileName.split("_")[2]
    with open(name + "_100s_H1.acc", mode="w", newline='') as myFile:
        fileWriter = csv.writer(myFile)
        for row in rows:
            fileWriter.writerow(row)
    
    rows = zip(newH2List)
    with open(name + "_100s_H2.acc", mode="w", newline='') as myFile:
        fileWriter = csv.writer(myFile)
        for row in rows:
            fileWriter.writerow(row)
    

#=====================Main==========================
ShortenTimeHistoryRecord("20161113_110330_POTS_20_V2A.csv", 50, 150)
#ShortenTimeHistoryRecord("20161113_110330_TEPS_20_V2A.csv", 90, 125)
#ShortenTimeHistoryRecord("20161113_110330_TEPS_20_V2A.csv", 109, 122)
#ShortenTimeHistoryRecord("20161113_110336_PIPS_20_V2A.csv", 50, 150)
#ShortenTimeHistoryRecord("20161113_110333_FKPS_20_V2A.csv", 50, 150)
#ShortenTimeHistoryRecord("20161113_110330_VUWS_20_V2A.csv", 50, 150)
#ShortenTimeHistoryRecord("20161113_110330_TFSS_20_V2A.csv", 50, 150)
print("finished")

