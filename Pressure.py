import matplotlib.pyplot as plt
import timeit
import os
from datetime import datetime

class Pressure:

    def __init__(self, pressureFilePath, pressureDirPath):
        # Pressure Data (Float in Torr) and Time (Float in ms)
        self.pTime = []
        self.Pressure = []
        # Cycles (int)
        self.cycles = []

        # File paths (String)
        self.pressureFilePath = pressureFilePath
        self.pressureDirPath = pressureDirPath

        # Recipe Info
        self.recipe = ""
        self.recipes = ["Al2O3", "TiO2", "HfO2", "ZrO2", "ZnO", "Ru", "Pt", "Ta2O5"]
        self.ingredientStack = []

        self.outString = ""

    # Reads through directory and prints out how many of each recipe is in the directory
    def readDir(self):
        path = self.pressureDirPath
        try:
            dir_list = os.listdir(path)
            self.parseTitles(dir_list)
        except NotADirectoryError:
            print("DIRECTORY NOT FOUND, PROCESS ABORTED. \n Hint: Try putting in a valid directory path.")
            return


    # Reads through the txt file and prints out the recipe, pressure, time, and cycles
    def readFile(self):

        path = self.pressureFilePath
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
                        self.recipe += data[i+3] + " "
                    self.recipe = self.recipe.strip()
                    for key in self.ingredientStack:
                        if self.recipe.find(key) != -1:
                            self.recipe = key

                empty = False
                self.pTime.append(float(data[0]))
                self.Pressure.append(float(data[1]))
                self.cycles.append(int(data[2]))

                iter += 1

        if not empty:
            self.outString += "Completed Cycles: " + str(self.cycles[0] - self.cycles[-1] + 1) + "/" + str(self.cycles[0]) + "\n\n"

    # Parses through the titles of the files and counts how many of each recipe is in the directory
    def parseTitles(self, dir_list):
        try:
            foobar = dir_list[0]
        except IndexError:
            print("DIRECTORY IS EMPTY, PROCESS ABORTED. \n Hint: Try putting in a directory with files.")
            return

        for i in dir_list:
            title = i.lower()
            for j in range(self.recipes.__len__()):
                if title.find(self.recipes[j].lower()) != -1:
                    self.ingredientStack.append(self.recipes[j])
                    break
            if (title.find("standby") == -1) and (title.find("pulse") == -1):
                self.ingredientStack.append("Unknown")
        
        self.outString += "Most Recent: " + str(self.ingredientStack) + "\n\n"

    def genReport(self):
        self.outString = self.outString = "----------------------------------------------\n\nPRESSURE REPORT AT " + datetime.now().strftime("%H:%M:%S") + " ON " + datetime.now().strftime("%m/%d/%Y") + "\n\n----------------------------------------------\n\n"
        self.readFile()
        self.outString += "Recipe: " + self.recipe.upper() + "\n\n----------------------------------------------\n\n"
        # self.readDir()
        return self.outString



def main():
    pressure = Pressure("/Users/andrew/Desktop/SNF Projects/Tool-Data/Pressure-Data/2024_06_13-12-56_Al2O3 - STANDARD.txt", "/Users/andrew/Desktop/SNF Projects/Tool-Data/Pressure-Data")
    print(pressure.genReport())


if __name__ == "__main__":
    main()