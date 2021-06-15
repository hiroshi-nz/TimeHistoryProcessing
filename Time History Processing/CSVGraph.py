# -*- coding: utf-8 -*-
"""
9:50~ damping ratio graph

"""


import csv
import matplotlib.pyplot as plt

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


def SimplePlot(fileName, title, xColumn, yColumn, xLabel, yLabel):

    xList = []
    yList = []

    with open(fileName, mode="r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if isfloat(row[0]):              
                xList.append(float(row[xColumn]))
                yList.append(float(row[yColumn]))
   
    plt.figure(dpi = 300)
    #plt.xlim(0, 10)
            
    plt.plot(xList, yList, "-")
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.grid()
    
def LabelFromFile(fileName, xColumn, yColumn):

    xList = []
    yList = []
    
    plt.figure(dpi = 300)

    with open(fileName, mode="r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if isfloat(row[0]):              
                xList.append(float(row[xColumn]))
                yList.append(float(row[yColumn]))
            else:
                plt.xlabel((row[xColumn]))
                plt.ylabel((row[yColumn]))
                
    #plt.xlim(0, 10)          
    plt.plot(xList, yList, "-")
    #plt.title(title)

    plt.grid()
            
def GraphsWithYColumnList(fileName, xColumn, yColumnIndexList):
    for yColumnIndex in yColumnIndexList:
        LabelFromFile(fileName, xColumn, yColumnIndex)
        
        
def Subplots(fileName, xColumn, yColumn, axs, axsIndex):

    xList = []
    yList = []
    
    with open(fileName, mode="r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if isfloat(row[0]):              
                xList.append(float(row[xColumn]))
                yList.append(float(row[yColumn]))
                        
    axs[axsIndex].plot(xList, yList, "-")
    axs[axsIndex].grid()

def CreateTitle(fileName, xColumn, yColumn):  
    with open(fileName, mode="r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if isfloat(row[0])==False:              
               #return row[xColumn] +" vs "+ row[yColumn]
               return row[yColumn]

def MultipleGraphs(fileNameList, xColumn, yColumnIndexList):
    
    for yColumnIndex in yColumnIndexList:
        plt.figure(dpi = 300)
        fig, axs = plt.subplots(1, len(fileNameList), figsize = (12, 3))
        fig.suptitle(CreateTitle(fileNameList[0], xColumn, yColumnIndex))
        axsIndex = 0
        for fileName in fileNameList:
            Subplots(fileName, xColumn, yColumnIndex, axs, axsIndex)
            axsIndex += 1
    plt.tight_layout()
    
    
def SortAndPlot(fileName, xColumn, yColumn):

    xList = []
    yList = []
    
    plt.figure(dpi = 300)

    with open(fileName, mode="r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if isfloat(row[0]):              
                xList.append(float(row[xColumn]))
                #To get rid of comma from number
                yList.append(float(row[yColumn].replace(",", "")))
                
            else:
                plt.xlabel((row[xColumn]))
                plt.ylabel((row[yColumn]))
                
    zipped = zip(xList, yList)
    zippedAndSorted = sorted(zipped, reverse = True)
    unZipped = zip(*zippedAndSorted)
    print(unZipped)
    sortedXList, sortedYList = map(list, unZipped)    
    
    #https://stackoverflow.com/questions/19931975/sort-multiple-lists-simultaneously
    
    #plt.xlim(0, 10)          
    plt.plot(sortedXList, sortedYList, "-")
    #plt.title(title)

    plt.grid()

def SortAndPlotWithYColumnList(fileName, xColumn, yColumnIndexList):
    for yColumnIndex in yColumnIndexList:
        SortAndPlot(fileName, xColumn, yColumnIndex)
        
def GRatio(fileName, xColumn, GIndex, GmaxIndex):
    xList = []
    GList = []
    GmaxList = []
    
    plt.figure(dpi = 300)

    with open(fileName, mode="r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if isfloat(row[0]):              
                xList.append(float(row[xColumn]))
                #To get rid of comma from number
                GList.append(float(row[GIndex].replace(",", ""))/1000000)
                GmaxList.append(float(row[GmaxIndex].replace(",", ""))/1000000)
            else:
                plt.xlabel((row[xColumn]))
                plt.ylabel("G/Gmax Ratio")
                
    zipped = zip(xList, GList, GmaxList)
    zippedAndSorted = sorted(zipped, reverse = True)
    unZipped = zip(*zippedAndSorted)
    sortedXList, sortedGList, sortedGmaxList = map(list, unZipped)    
    
    #https://stackoverflow.com/questions/19931975/sort-multiple-lists-simultaneously
    
    sortedGRatioList = []
    
    i = 0
    while i < len(GList):
        sortedGRatioList.append(sortedGList[i]/sortedGmaxList[i])
        i += 1
    
    #plt.xlim(0, 10)          
    plt.plot(sortedXList, sortedGRatioList, "-")
    #plt.title(title)

    plt.grid()
    

    plt.figure(dpi = 1200)
    fig, axs = plt.subplots(1, 2, figsize = (10, 5))
    fig.suptitle("Change in Shear Modulus by Elevation")
        
    axs[0].plot(sortedXList, sortedGRatioList, "-")
    axs[0].set_xlabel("Elevation(m)")
    axs[0].set_ylabel("G/Gmax Ratio")

    axs[0].grid()
    axs[1].plot(sortedXList, sortedGList, "-")
    axs[1].plot(sortedXList, sortedGmaxList, "-")
    axs[1].set_xlabel("Elevation(m)")
    axs[1].set_ylabel("Shear Modulus(GPa)")
    axs[1].grid()
    
    plt.tight_layout()
    
def DampingRatio(fileName, xColumn, dampingRatioColumn):
    xList = []
    dampingRatioList = []
    
    plt.figure(dpi = 300)

    with open(fileName, mode="r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if isfloat(row[0]):              
                xList.append(float(row[xColumn]))
                dampingRatioList.append(float(row[dampingRatioColumn]))
            else:
                plt.xlabel((row[xColumn]))
                plt.ylabel("Damping Ratio")
                
 
    zipped = zip(xList, dampingRatioList)
    zippedAndSorted = sorted(zipped, reverse = True)
    unZipped = zip(*zippedAndSorted)
    sortedXList, sortedDampingRatioList = map(list, unZipped)    
    
    #https://stackoverflow.com/questions/19931975/sort-multiple-lists-simultaneously
      
    #plt.xlim(0, 10)          
    plt.plot(sortedXList, sortedDampingRatioList, "-")
    #plt.title(title)

    plt.grid()
    
"""
    plt.figure(dpi = 1200)
    fig, axs = plt.subplots(1, 2, figsize = (10, 5))
    fig.suptitle("Change in Shear Modulus by Elevation")
        
    axs[0].plot(sortedXList, sortedDampingRatioList, "-")
    axs[0].set_xlabel("Elevation(m)")
    axs[0].set_ylabel("G/Gmax Ratio")

    axs[0].grid()
    axs[1].plot(sortedXList, sortedGList, "-")
    axs[1].plot(sortedXList, sortedGmaxList, "-")
    axs[1].set_xlabel("Elevation(m)")
    axs[1].set_ylabel("Shear Modulus(GPa)")
    axs[1].grid()
    
    plt.tight_layout()

"""

def GRatioAndDamping(fileName, xColumn, GIndex, GmaxIndex, dampingRatioColumn):
    xList = []
    GList = []
    GmaxList = []
    dampingRatioList = []    

    with open(fileName, mode="r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if isfloat(row[0]):              
                xList.append(float(row[xColumn]))
                #To get rid of comma from number
                GList.append(float(row[GIndex].replace(",", ""))/1000000)
                GmaxList.append(float(row[GmaxIndex].replace(",", ""))/1000000)
                dampingRatioList.append(float(row[dampingRatioColumn]))

                
    zipped = zip(xList, GList, GmaxList, dampingRatioList)
    zippedAndSorted = sorted(zipped, reverse = True)
    unZipped = zip(*zippedAndSorted)
    sortedXList, sortedGList, sortedGmaxList, sortedDampingRatioList = map(list, unZipped)    
    
    sortedGRatioList = []
    
    i = 0
    while i < len(GList):
        sortedGRatioList.append(sortedGList[i]/sortedGmaxList[i])
        i += 1
    
    fig, axs = plt.subplots(1, 2, figsize = (10, 5))
    fig.suptitle("Change in Shear Modulus by Elevation")
    
    axs[0].plot(sortedXList, sortedGRatioList, "-")
    #axs[0].plot(sortedXList, sortedDampingRatioList, "-")
    axs[0].set_xlabel("Elevation(m)")
    axs[0].set_ylabel("G/Gmax Ratio")
    axs[0].grid()    

    axs[1].plot(sortedXList, sortedGList, "-", label = "G")
    axs[1].plot(sortedXList, sortedGmaxList, "-", label ="Gmax")
    axs[1].set_xlabel("Elevation(m)")
    axs[1].set_ylabel("Shear Modulus(GPa)")
    axs[1].legend()
    axs[1].grid()
    plt.tight_layout()
    
    
    fig, axs = plt.subplots(1, 2, figsize = (10, 5))
    fig.suptitle("Damping Ratio")

    axs[0].plot(sortedXList, sortedDampingRatioList, "-")
    axs[0].set_xlabel("Elevation(m)")
    axs[0].set_ylabel("Damping Ratio")
    axs[0].grid()    

    
    axs[1].plot(sortedDampingRatioList, sortedGRatioList, "o")    
    axs[1].set_xlabel("Damping Ratio")
    axs[1].set_ylabel("G/Gmax Ratio")
    axs[1].grid()
    plt.tight_layout()
    
    density = 1835
    i = 0;
    while i < len(sortedXList):
        print("Elevation: " + str(sortedXList[i]) + "m  G: " + str(sortedGList[i]) + "GPa  Gmax: " + str(sortedGmaxList[i]) + "GPa ")
        
        
        i += 1
    


def PGA(fileName, xColumn, yColumn):
    xList = []
    yList = []
    
    plt.figure(dpi = 300)

    with open(fileName, mode="r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if isfloat(row[0]):              
                xList.append(float(row[xColumn]))
                yList.append(float(row[yColumn]))
            else:
                plt.xlabel("Peak Horizontal Acceleration (g)")
                plt.ylabel("Elevation (m)")
                
 
    zipped = zip(yList, xList)
    zippedAndSorted = sorted(zipped, reverse = True)
    unZipped = zip(*zippedAndSorted)
    sortedYList, sortedXList = map(list, unZipped)    
    
    #https://stackoverflow.com/questions/19931975/sort-multiple-lists-simultaneously
    
    layers = [14, 0, -24, -85, -190, -330]
    colors = ["yellow", "yellowgreen", "lime", "mediumseagreen", "gray"]
            
    plt.plot(sortedXList, sortedYList, "b-")
    left, right = plt.xlim()
    plt.ylim(-330, 14)
    
    i = 0
    while i < len(colors):    
        plt.fill_between([left, right], layers[i], layers[i + 1], color = colors[i], alpha = 0.5)
        i += 1

    plt.xlim(left, right)
    plt.title("Peak Horizontal Acceleration vs Elevation")
    plt.grid()
    plt.tight_layout()

def PaintLayers(ax, layers, colors):
    left, right = ax.get_xlim()
    i = 0
    while i < len(colors):    
        ax.fill_between([left, right], layers[i], layers[i + 1], color = colors[i], alpha = 0.5)
        i += 1
    
    ax.set_ylim(-330, 14)
    ax.set_xlim(left, right)
    ax.grid() 
    

def GRatioAndDampingNice(fileName, xColumn, GIndex, GmaxIndex, dampingRatioColumn):
    elevationList = []
    GList = []
    GmaxList = []
    dampingRatioList = []    

    with open(fileName, mode="r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if isfloat(row[0]):              
                elevationList.append(float(row[xColumn]))
                #To get rid of comma from number
                GList.append(float(row[GIndex].replace(",", ""))/1000000)
                GmaxList.append(float(row[GmaxIndex].replace(",", ""))/1000000)
                dampingRatioList.append(float(row[dampingRatioColumn]))

                
    zipped = zip(elevationList, GList, GmaxList, dampingRatioList)
    zippedAndSorted = sorted(zipped, reverse = True)
    unZipped = zip(*zippedAndSorted)
    sortedElevationList, sortedGList, sortedGmaxList, sortedDampingRatioList = map(list, unZipped)    
    
    sortedGRatioList = []
    
    i = 0
    while i < len(GList):
        sortedGRatioList.append(sortedGList[i]/sortedGmaxList[i])
        i += 1
    
    
    layers = [14, 0, -24, -85, -190, -330]
    colors = ["yellow", "yellowgreen", "lime", "mediumseagreen", "gray"]
            
    
    fig, axs = plt.subplots(1, 2, figsize = (10, 5))
    fig.suptitle("Change in Shear Modulus by Elevation")
    
    axs[0].plot(sortedGRatioList, sortedElevationList, "b-")
    PaintLayers(axs[0], layers, colors)    
    axs[0].set_ylabel("Elevation(m)")
    axs[0].set_xlabel("G/Gmax Ratio")
   
    
    axs[1].plot(sortedGList, sortedElevationList, "-b", label = "G")
    axs[1].plot(sortedGmaxList, sortedElevationList, "-r", label ="Gmax")
    PaintLayers(axs[1], layers, colors)
    axs[1].set_ylabel("Elevation(m)")
    axs[1].set_xlabel("Shear Modulus(GPa)")
    axs[1].legend()
    plt.tight_layout()
    
    
    fig, axs = plt.subplots(1, 2, figsize = (10, 5))
    fig.suptitle("Damping Ratio")

    axs[0].plot(sortedDampingRatioList, sortedElevationList, "b-")    
    PaintLayers(axs[0], layers, colors)    
    axs[0].set_ylabel("Elevation(m)")
    axs[0].set_xlabel("Damping Ratio")
    
    axs[1].plot(sortedDampingRatioList, sortedGRatioList, "bo")    
    axs[1].set_xlabel("Damping Ratio")
    axs[1].set_ylabel("G/Gmax Ratio")
    axs[1].grid()
    plt.tight_layout()
    
    
    
def PlotSlope(fileName, xColumn, yColumn, title, upperBound, lowerBound):

    xList = []
    yList = []

    with open(fileName, mode="r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if isfloat(row[0]):              
                xList.append(float(row[xColumn]))
                yList.append(float(row[yColumn]))
   
    plt.figure(dpi = 300)
    #plt.xlim(0, 10)
            
    plt.plot(xList, yList, "g-", label ="Displacement (Analysis)")
    plt.title(title)
    plt.xlabel("Distance from Origin (m)")
    plt.ylabel("Vertical Displacement (m)")
    
    left, right = plt.xlim()
    
    plt.hlines(upperBound, left, right, colors="dimgrey", linestyles = "dashed", label = "Min Displacement (Measured)")
    plt.hlines(lowerBound, left, right, colors="dimgrey", linestyles = "dashdot", label = "Max Displacement(Measured)")
    
    bottom, top = plt.ylim()
    
    #plt.xlim(left, right)
    plt.xlim(min(xList), max(xList))
    plt.ylim(bottom, 0.05)
    plt.legend()
    plt.grid()
    
    
def NewmarkTimeAcceleration(fileName, xColumn, yColumn, title, yieldAcceleration):

    xList = []
    yList = []

    with open(fileName, mode="r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if isfloat(row[1]):              
                xList.append(float(row[xColumn]))
                yList.append(float(row[yColumn]))
   
    plt.figure()
     
    fig, ax = plt.subplots(dpi = 300, figsize = (10, 3))
    
    ax.plot(xList, yList, "b-", linewidth = 0.7)
    ax.set_title(title)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Average Acceleration (m/s²)")
    
    left = 0
    right = 100
    #left, right = ax.get_xlim()
    
    ax.hlines(yieldAcceleration, left, right, colors="r", linestyles = "dashed", label = "Yield Acceleration")
    ax.hlines(-yieldAcceleration, left, right, colors="r", linestyles = "dashed")
    
    ax.xaxis.set_major_locator(plt.MultipleLocator(10))
    ax.set_xlim(left, right)
    ax.grid()    
    ax.legend()
    #plt.tight_layout()

def NewmarkTimeDeformation(fileName, xColumn, yColumn, title):

    xList = []
    yList = []

    with open(fileName, mode="r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if isfloat(row[1]):              
                xList.append(float(row[xColumn]))
                yList.append(float(row[yColumn]))
   
    plt.figure()
     
    fig, ax = plt.subplots(dpi = 300, figsize = (10, 2))
    
    ax.plot(xList, yList, "b-", linewidth = 1.0)
    ax.set_title(title)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Deformation")
    
    left = 0
    right = 100
    #left, right = ax.get_xlim()
    
    #ax.hlines(yieldAcceleration, left, right, colors="r", linestyles = "dashed", label = "Yield Acceleration")
    #ax.hlines(-yieldAcceleration, left, right, colors="r", linestyles = "dashed")
    
    ax.xaxis.set_major_locator(plt.MultipleLocator(10))
    ax.set_xlim(left, right)
    ax.grid()
    #plt.tight_layout()
    
def TimeHistoryV2A(fileName, title):

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
                H1List.append(float(row[1])/9810)
                H2List.append(float(row[2])/9810)
                timeList.append(timeCounter)
                timeCounter += timeStep
            
        
        name = fileName.split("_")[2]
        
        fig, ax = plt.subplots(dpi = 300, figsize = (10, 2))
        
        ax.plot(timeList, H1List, "b-", label = name + " H1", linewidth = 0.7)
        ax.plot(timeList, H2List, "r-", label = name + " H2", linewidth = 0.7)
        ax.set_title(title)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Acceleration (g)")
        
        left = min(timeList)
        right = max(timeList)

        ax.xaxis.set_major_locator(plt.MultipleLocator(50))                                                                                                
        ax.yaxis.set_major_locator(plt.MultipleLocator(0.05))
        ax.set_xlim(left, right)
        ax.grid()
        ax.legend()
        #plt.tight_layout()
        
def TimeHistoryGeoStudio(fileName, title):

    HList = []
    timeList = []
    timeStep = 0.005
    timeCounter = 0

    with open(fileName, mode="r", newline='') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if isfloat(row[0]):#Ignore the first 5 lines without numbers               
                HList.append(float(row[0])/980)
                timeList.append(timeCounter)
                timeCounter += timeStep
            
        
        fig, ax = plt.subplots(dpi = 300, figsize = (10, 2))
        
        ax.plot(timeList, HList, "b-", linewidth = 0.7)
        ax.set_title(title)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Acceleration (g)")
        
        left = min(timeList)
        right = max(timeList)

        
        ax.xaxis.set_major_locator(plt.MultipleLocator(10))
        ax.yaxis.set_major_locator(plt.MultipleLocator(0.05))
        ax.set_xlim(left, right)
        ax.set_ylim(-0.2, 0.2)
        ax.grid()
        #plt.tight_layout()        


def FindAbsMax(numList):
    maxNum = abs(max(numList))
    minNum = abs(min(numList))
    if maxNum > minNum:
        return maxNum
    else:
        return minNum

def TimeHistoryGeoStudioH1H2(fileName1, fileName2, title):

    H1List = []
    H2List = []
    timeList = []
    timeStep = 0.005
    timeCounter = 0

    with open(fileName1, mode="r", newline='') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if isfloat(row[0]):            
                H1List.append(float(row[0])/980)
                timeList.append(timeCounter)
                timeCounter += timeStep
                
    with open(fileName2, mode="r", newline='') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if isfloat(row[0]):            
                H2List.append(float(row[0])/980)

        
        name = fileName1.split("/")[1]
        name = name.split("_")[0]
        print(name)
        
        fig, ax = plt.subplots(dpi = 300, figsize = (10, 2))
        
        ax.plot(timeList, H1List, "b-", label = name + " H1", linewidth = 0.7)
        ax.plot(timeList, H2List, "r-", label = name + " H2", linewidth = 0.7)
        ax.set_title(title)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Acceleration (g)")
        
        left = min(timeList)
        right = max(timeList)

        
        ax.xaxis.set_major_locator(plt.MultipleLocator(10))
        ax.yaxis.set_major_locator(plt.MultipleLocator(0.05))
        ax.set_xlim(left, right)
        ax.grid()
        ax.legend()
        #plt.tight_layout()
        
        print("H1 PGA: " + str(FindAbsMax(H1List)) + "  H2 PGA: " + str(FindAbsMax(H2List)))
        

#=====================Main==========================

#====================Horizontal Data===================================

#SimplePlot("RightSlopeTopAll.csv", "Right Slope Lateral Displacement", 1, 4,"X Coordinate(m)","X Displacement(m)")
#SimplePlot("RightSlopeTopAll.csv", "Right Slope Settlement", 1, 5,"X Coordinate(m)","Y Displacement(m)")
#SimplePlot("RightSlopeTopAll.csv", "Mean Effective Stress", 1, 4,"X Coordinate(m)","Mean Effective Stress")
#SimplePlot("RightSlopeTopAll.csv", "Deviatric Stress", 1, 4,"X Coordinate(m)","Deviatric Stress")

#LabelFromFile("RightSlopeTopAll.csv", 1, 4)
#LabelFromFile("RightSlopeTopAll.csv", 1, 5)
#LabelFromFile("RightSlopeTopAll.csv", 1, 21)
#LabelFromFile("RightSlopeTopAll.csv", 1, 24)
#LabelFromFile("RightSlopeTopAll.csv", 1, 33)

fileNameList = ["LeftSlopeTopAll.csv", "MiddleTopAll.csv", "RightSlopeTopAll.csv"]
yColumnList = [4, 5, 21, 24, 33]
xCoord = 1
xDisp = 4
yDisp = 5
meanEffStress = 21
deviatricStress = 24
deviatricStrain = 33


#GraphsWithYColumnList("RightSlopeTopAll.csv", 1, yColumnList)
#GraphsWithYColumnList("LeftSlopeTopAll.csv", 1, yColumnList)
#GraphsWithYColumnList("MiddleTopAll.csv", 1, yColumnList)
#MultipleGraphs(fileNameList, 1, yColumnList)

#PlotSlope("MiddleTopAll.csv", xCoord, yDisp,"Vertical Displacement at Centre", -0.2, -0.3)
#PlotSlope("RightSlopeTopAll.csv", xCoord, yDisp,"Vertical Displacement near Right Slope", -0.4, -0.6)
#PlotSlope("LeftSlopeTopAll.csv", xCoord, yDisp,"Vertical Displacement near Left Slope", -0.4, -0.6)
#==================Vertical Data=====================================
#SortAndPlot("VerticalMiddleAll.csv", 2, 32)

#VerticalYColumnList = [31, 32, 34, 45]
#SortAndPlotWithYColumnList("VerticalMiddleAll.csv", 2, VerticalYColumnList)

G = 31
Gmax = 34
dampingRatio = 32

#GRatio("VerticalMiddleAll.csv", 2, G, Gmax)

#DampingRatio("VerticalMiddleAll.csv", 2, 32)

#GRatioAndDamping("VerticalMiddleAll.csv", 2, G, Gmax, dampingRatio)

#GRatioAndDampingNice("VerticalMiddleAll.csv", 2, G, Gmax, dampingRatio)

relativeXDisp = 35
xDisp = 44
xAcc = 50
pga = 57
#PGA("VerticalMiddleAll.csv", pga, 2)

#=====================Presentation======================
#NewmarkTimeAcceleration("Newmark/H2/AvgAccVsTime.csv", 0, 1, "Time vs Average Acceleration", 0.065)
#NewmarkTimeDeformation("Newmark/H2/Deformation.csv", 0, 1, "Time vs Deformation")

TimeHistoryV2A("Time History/20161113_110330_TEPS_20_V2A.csv", "TEPS Time History")
#TimeHistoryV2A("Time History/20161113_110330_POTS_20_V2A.csv", "POTS Time History")



#TimeHistoryGeoStudioH1H2("Time History/TEPS_Shortened_H1.acc", "Time History/TEPS_Shortened_H2.acc", "TEPS Time History")
#TimeHistoryGeoStudio("Time History/TEPS_Shortened_H1.acc", "TEPS H1 Time History")
#TimeHistoryGeoStudio("Time History/TEPS_Shortened_H2.acc", "TEPS H2 Time History")

#TimeHistoryGeoStudio("Time History/POTS_100s_H1.acc", "POTS H1 Time History")
#TimeHistoryGeoStudio("Time History/POTS_100s_H2.acc", "POTS H2 Time History")
TimeHistoryGeoStudioH1H2("Time History/POTS_100s_H1.acc", "Time History/POTS_100s_H2.acc", "POTS Time History")
print("finished")

