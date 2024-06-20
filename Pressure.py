import matplotlib.pyplot as plt
import timeit
import os
from datetime import datetime


# Pressure Data (Float in Torr) and Time (Float in ms)
pTime = []
Pressure = []
# Cycles (int)
cycles = []

# File paths (String)
pressureFilePath = "/Users/andrew/Desktop/SNF Projects/Tool-Data/Pressure-Data/2024_06_13-12-56_Al2O3 - STANDARD.txt"
pressureDirPath = "/Users/andrew/Desktop/SNF Projects/Tool-Data/Pressure-Data"

# Recipe Info
recipe = ""
recipes = ["Al2O3", "TiO2", "HfO2", "ZrO2", "ZnO", "Ru", "Pt", "Ta2O5"]
ingredientStack = []


# Reads through directory and prints out how many of each recipe is in the directory
def readDir():
    path = pressureDirPath
    try:
        dir_list = os.listdir(path)
        parseTitles(dir_list)
    except NotADirectoryError:
        print("DIRECTORY NOT FOUND, PROCESS ABORTED. \n Hint: Try putting in a valid directory path.")
        return


# Reads through the txt file and prints out the recipe, pressure, time, and cycles
def readFile():

    path = pressureFilePath
    global recipe
    empty = True
    iter = 0

    try:
        foobar = open(path)
    except FileNotFoundError:
        print("FILE NOT FOUND, PROCESS ABORTED. \n Hint: Try putting in a valid file path.")
        return

    with open(path, "r") as file:
        for line in file:
            data = line.strip().replace(" - ", " ").split()
            try:
                foobar = data[0]
            except IndexError:
                continue
            if data[0] == "Pressure":
                continue
            
            if iter == 1:
                for i in range(data.__len__() - 3):
                    recipe += data[i+3] + " "
                recipe = recipe.strip()
                for key in ingredientStack:
                    if recipe.find(key) != -1:
                        recipe = key

            empty = False
            pTime.append(float(data[0]))
            Pressure.append(float(data[1]))
            cycles.append(int(data[2]))

            iter += 1

    if not empty:
        print("Completed Cycles:", (cycles[0] - cycles[-1] + 1),  "/", cycles[0])


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



def main():
    print("PRESSURE REPORT AT" , datetime.now().strftime("%H:%M:%S"), 
          "ON", datetime.now().strftime("%m/%d/%Y"))
    print("-----------------------------------------")
    readFile()
    print("Recipe:", recipe.upper())
    readDir()


if __name__ == "__main__":
    main()