import matplotlib.pyplot as plt
import os
from datetime import datetime


class Heating:

    def __init__(self, heatingFilePath, heatingDirPath):
        # Heater Data (Floats in Celcius) and Time (Float in s)
        self.hTime = []
        self.trap = []
        self.stopValve = []
        self.outerHeater = []
        self.innerHeater = []
        self.pManifold = []
        self.precursors = [[], [], [], [], []]
        self.mfc1 = []
        self.numPrecursors = 0

        # Cycles (int)
        self.cycles = []

        # File Paths (String)
        self.heatingFilePath = heatingFilePath
        self.heatingDirPath = heatingDirPath

        # Recipe Info
        self.currentRecipe = ""
        self.ingredientStack = []
        self.recipes = ["Al2O3", "TiO2", "HfO2", "ZrO2", "ZnO", "Ru", "Pt", "Ta2O5"]

        self.outString = ""

    # Reads through directory and prints out how many of each recipe is in the directory
    def readDir(self):
        path = self.heatingDirPath
        try:
            dir_list = os.listdir(path)
            self.parseTitles(dir_list)
        except NotADirectoryError:
            print("DIRECTORY NOT FOUND, PROCESS ABORTED. \n Hint: Try putting in a valid directory path.")
            return


    # Reads through the txt file and prints out the recipe, pressure, time, and cycles
    def readFile(self):
        path = self.heatingFilePath
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
                self.hTime.append(float(data[0]))
                self.trap.append(float(data[1]))
                self.stopValve.append(float(data[2]))
                self.outerHeater.append(float(data[3]))
                self.innerHeater.append(float(data[4]))
                self.pManifold.append(float(data[5]))
                

                # Find the number of precursors
                index = 6
                while float(data[index]) < 1000:
                    index += 1
                self.numPrecursors = index - 6
                # Record the precursor data
                for j in range(self.numPrecursors):
                    self.precursors[j].append(float(data[j+6]))

                # record mfc1 and cycles data which is after the precursor data
                self.mfc1.append(float(data[index+1]))
                self.cycles.append(int(data[index+3]))

                iter += 1
                # Find the recipe name
                if iter == 1:
                    for j in range(index + 4, data.__len__(), 1):
                        self.currentRecipe += data[j] + " "
                    self.currentRecipe = self.currentRecipe.strip()
                    for key in self.ingredientStack:
                        if self.currentRecipe.find(key) != -1:
                            self.currentRecipe = key


        # if the file is not empty, print out the data
        if not empty:
            print("bruh")
            self.outString += "Completed Cycles: " + str(self.cycles[0] - self.cycles[-1] + 1) + "/" + str(self.cycles[0]) + "\n\n"
            self.outString += "Number of Precursors: " + str(self.numPrecursors) + "\n\n"
            self.outString += "Inner Heater Final Temp: " + str(self.innerHeater[-1]) + "\u00b0 C" + "\n\n"
            self.outString += "Outer Heater Final Temp: " + str(self.outerHeater[-1]) + "\u00b0 C" + "\n\n"
            self.averageTemp()

            # print("Completed Cycles:", (cycles[0] - cycles[-1] + 1),  "/", cycles[0])
            # print("Number of Precursors:", numPrecursors)
            # print("Inner Heater Final Temp:", str(innerHeater[-1]) + "\u00b0 C")
            # print("Outer Heater Final Temp:", str(outerHeater[-1]) + "\u00b0 C")
            # averageTemp()


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


    # Helper method to calculate the average temperature of each precursor
    def averageTemp(self):
        self.outString
        for i in range(self.numPrecursors):
            sum = 0
            for j in range(self.precursors[i].__len__()):
                sum += self.precursors[i][j]
            self.outString += "Average Temp of Precursor " + str(i+1) + ": " + str(round(sum/self.precursors[i].__len__(), 1)) + "\u00b0 C" + "\n\n"
            # print("Average Temp of Precursor", i+1, ":", str(round(sum/precursors[i].__len__(), 1)) +  "\u00b0 C")


    def genReport(self):
        self.outString = "----------------------------------------------\n\nHEATING REPORT AT " + datetime.now().strftime("%H:%M:%S") + " ON " + datetime.now().strftime("%m/%d/%Y") + "\n\n----------------------------------------------\n\n"
        self.readFile()
        self.outString += "Recipe: " + self.currentRecipe.upper() + "\n\n----------------------------------------------\n\n"
        # self.readDir()
        return self.outString


def main():
    # print("HEATING REPORT AT" , datetime.now().strftime("%H:%M:%S"), 
    #       "ON", datetime.now().strftime("%m/%d/%Y"))
    # print("----------------------------------------")
    
    heating = Heating("/Users/andrew/Desktop/SNF Projects/Tool-Data/Heating-Data/2024_06_13-21-21_MV standard Al2O3 4wtr pulse first 80deg.txt", "/Users/andrew/Desktop/SNF Projects/Tool-Data/Heating-Data")
    print(heating.genReport())


if __name__ == "__main__":
    main()