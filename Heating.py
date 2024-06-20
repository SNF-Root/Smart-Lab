import matplotlib.pyplot as plt
import os
from datetime import datetime


# Heater Data (Floats in Celcius) and Time (Float in s)
hTime = []
trap = []
stopValve = []
outerHeater = []
innerHeater = []
pManifold = []
precursors = [[], [], [], [], []]
mfc1 = []
numPrecursors = 0

# Cycles (int)
cycles = []

# File Paths (String)
heatingFilePath = "/Users/andrew/Desktop/SNF Projects/Tool-Data/Heating-Data/2024_06_14-11-23_100c_tio2.txt"
heatingDirPath = "/Users/andrew/Desktop/SNF Projects/Tool-Data/Heating-Data"

# Recipe Info
currentRecipe = ""
ingredientStack = []
recipes = ["Al2O3", "TiO2", "HfO2", "ZrO2", "ZnO", "Ru", "Pt", "Ta2O5"]



# Reads through directory and prints out how many of each recipe is in the directory
def readDir():
    path = heatingDirPath
    try:
        dir_list = os.listdir(path)
        parseTitles(dir_list)
    except NotADirectoryError:
        print("DIRECTORY NOT FOUND, PROCESS ABORTED. \n Hint: Try putting in a valid directory path.")
        return


# Reads through the txt file and prints out the recipe, pressure, time, and cycles
def readFile():
    path = heatingFilePath
    global currentRecipe
    global numPrecursors
    # If the file is empty
    empty = True
    # Iterator to find line 1 of file, which contains the recipe name at the end
    iter = 0

    try:
        foobar = open(path)
    except FileNotFoundError:
        print("FILE NOT FOUND, PROCESS ABORTED. \n Hint: Try putting in a valid file path.")
        return

    # main loop to read through the file line by line
    with open(path, "r") as file:
        for line in file:
            data = line.strip().split()
            try:
                foobar = data[0]
            except IndexError:
                continue
            if data[0] == "Heater":
                continue
            
            # If the file is not empty, record the data
            empty = False
            hTime.append(float(data[0]))
            trap.append(float(data[1]))
            stopValve.append(float(data[2]))
            outerHeater.append(float(data[3]))
            innerHeater.append(float(data[4]))
            pManifold.append(float(data[5]))
            

            # Find the number of precursors
            index = 6
            while float(data[index]) < 1000:
                index += 1
            numPrecursors = index - 6
            # Record the precursor data
            for j in range(numPrecursors):
                precursors[j].append(float(data[j+6]))

            # record mfc1 and cycles data which is after the precursor data
            mfc1.append(float(data[index+1]))
            cycles.append(int(data[index+3]))

            iter += 1
            # Find the recipe name
            if iter == 1:
                for j in range(index + 4, data.__len__(), 1):
                    currentRecipe += data[j] + " "
                currentRecipe = currentRecipe.strip()
                for key in ingredientStack:
                    if currentRecipe.find(key) != -1:
                        currentRecipe = key


    # if the file is not empty, print out the data
    if not empty:
        print("Completed Cycles:", (cycles[0] - cycles[-1] + 1),  "/", cycles[0])
        print("Number of Precursors:", numPrecursors)
        print("Inner Heater Final Temp:", str(innerHeater[-1]) + "\u00b0 C")
        print("Outer Heater Final Temp:", str(outerHeater[-1]) + "\u00b0 C")
        averageTemp()


# Parses through the titles of the files and counts how many of each recipe is in the directory
def parseTitles(dir_list):
    try:
        foobar = dir_list[0]
    except IndexError:
        print("DIRECTORY IS EMPTY, PROCESS ABORTED. \n Hint: Try putting in a directory with files.")
        return
    
    for i in dir_list:
        title = i.lower()
        for j in range(recipes.__len__()):
            if title.find(recipes[j].lower()) != -1:
                ingredientStack.append(recipes[j])
                break
        if (title.find("standby") == -1) and (title.find("pulse") == -1):
            ingredientStack.append("Unknown")
    
    print("Most Recent:", ingredientStack)


# Helper method to calculate the average temperature of each precursor
def averageTemp():
    for i in range(numPrecursors):
        sum = 0
        for j in range(precursors[i].__len__()):
            sum += precursors[i][j]
        print("Average Temp of Precursor", i+1, ":", str(round(sum/precursors[i].__len__(), 1)) +  "\u00b0 C")


def main():
    print("HEATING REPORT AT" , datetime.now().strftime("%H:%M:%S"), 
          "ON", datetime.now().strftime("%m/%d/%Y"))
    print("----------------------------------------")
    readFile()
    print("Recipe:", currentRecipe.upper())
    readDir()


if __name__ == "__main__":
    main()