import matplotlib.pyplot as plt
import os
from datetime import datetime


class Heating:

    def __init__(self, heatingDirPath, heatingFilePath=""):
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
        self.recipes = ["Al2O3", "TiO2", "HfO2", "ZrO2", "ZnO", "Ru", "Pt", "Ta2O5"]
        self.ingredientStack = []
        self.fileStack = []
        self.dir_list = []

        self.outString = ""


    # Reads through directory and prints out how many of each recipe is in the directory
    def readDir(self):
        path = self.heatingDirPath
        try:
            self.dir_list = os.listdir(path)
            self.parseTitles()
        except NotADirectoryError:
            print("DIRECTORY NOT FOUND, PROCESS ABORTED. \n Hint: Try putting in a valid directory path.")
            return


    # Reads through the txt file and prints out the recipe, pressure, time, and cycles
    def readFile(self):
        path = self.heatingFilePath
        self.hTime = []
        self.trap = []
        self.stopValve = []
        self.outerHeater = []
        self.innerHeater = []
        self.pManifold = []
        self.precursors = [[], [], [], [], []]
        self.mfc1 = []
        self.numPrecursors = 0
        self.cycles = []
        self.currentRecipe = ""

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
            if (self.cycles[0] - self.cycles[-1] + 1) > self.cycles[0]:
                self.outString += "Completed Cycles: " + str(self.cycles[0]) + "/" + str(self.cycles[0]) + "\n\n"
            else:
                self.outString += "Completed Cycles: " + str(self.cycles[0] - self.cycles[-1] + 1) + "/" + str(self.cycles[0]) + "\n\n"
            self.outString += "Number of Precursors: " + str(self.numPrecursors) + "\n\n"
            self.outString += "Inner Heater Final Temp: " + str(self.innerHeater[-1]) + "\u00b0 C" + "\n\n"
            self.outString += "Outer Heater Final Temp: " + str(self.outerHeater[-1]) + "\u00b0 C" + "\n\n"
            self.averageTemp()


    # Parses through the titles of the files and counts how many of each recipe is in the directory
    def parseTitles(self):
        try:
            foobar = self.dir_list[0]
        except IndexError:
            print("DIRECTORY IS EMPTY, PROCESS ABORTED. \n Hint: Try putting in a directory with files.")
            return
        
        for i in self.dir_list:
            title = i.lower()
            for j in range(self.recipes.__len__()):
                if title.find(self.recipes[j].lower()) != -1:
                    self.ingredientStack.append(self.recipes[j])
                    break
            if (title.find("standby") == -1) and (title.find("pulse") == -1):
                self.ingredientStack.append("Unknown")
        
        # self.outString += "Most Recent: " + str(self.ingredientStack) + "\n\n"


    # Helper method to calculate the average temperature of each precursor
    def averageTemp(self):
        self.outString
        for i in range(self.numPrecursors):
            sum = 0
            for j in range(self.precursors[i].__len__()):
                sum += self.precursors[i][j]
            self.outString += "Average Temp of Precursor " + str(i+1) + ": " + str(round(sum/self.precursors[i].__len__(), 1)) + "\u00b0 C" + "\n\n"
            # print("Average Temp of Precursor", i+1, ":", str(round(sum/precursors[i].__len__(), 1)) +  "\u00b0 C")


    # Generates the report and returns it as a string
    def genReport(self):
        self.outString = "----------------------------------------------\n\nHEATING REPORT AT " + datetime.now().strftime("%H:%M:%S") + " ON " + datetime.now().strftime("%m/%d/%Y") + "\n\n----------------------------------------------\n\n"
        self.readFile()
        self.outString += "Recipe: " + self.currentRecipe.upper() + "\n\n----------------------------------------------\n\n"
        # self.readDir()
        file_path = "Tool-Data/data/Output_Text/Heating Report.txt"
        with open(file_path, "w") as file:
            file.write(self.outString)
        return self.outString


    # Generates a plot of the data and saves it to the Output_Plots directory
    def plotHeating(self):
        try:
            os.remove('Tool-Data/data/Output_Plots/Non-Precursor Heating Data.png')
        except FileNotFoundError:
            pass
        try:
            os.remove('Tool-Data/data/Output_Plots/Precursor Heating Data.png')
        except FileNotFoundError:
            pass
        
        # Plotting the Heating Data
        # Graph the Non-Precursor Temperature Data
        fig, axs = plt.subplots(3, 2)
        fig.suptitle('Non-Precursor Heating Data')
        fig.supxlabel('Time (s)')
        fig.supylabel('Temperature (C)')
        fig.set_size_inches(8, 8)
        axs[0, 0].plot(self.hTime, self.trap, 'tab:blue')
        axs[0, 0].set_title('Trap/Pump')
        axs[0, 1].plot(self.hTime, self.stopValve, 'tab:orange')
        axs[0, 1].set_title('Stop Valve')
        axs[1, 0].plot(self.hTime, self.outerHeater, 'tab:green')
        axs[1, 0].set_title('Outer Heater')
        axs[1, 1].plot(self.hTime, self.innerHeater, 'tab:red')
        axs[1, 1].set_title('Inner Heater')
        axs[2, 0].plot(self.hTime, self.pManifold, 'tab:purple')
        axs[2, 0].set_title('Precursor Manifold')
        axs[2, 1].plot(self.hTime, self.mfc1, 'tab:brown')
        axs[2, 1].set_title('MFC1')
        fig.tight_layout()
        fig.savefig('Tool-Data/data/Output_Plots/Non-Precursor Heating Data.png')
        # plt.show()
        
        # Plotting the Precursor Data
        if self.numPrecursors > 0:
            fig, axs = plt.subplots(self.numPrecursors, 1)
            fig.suptitle('Precursor Heating Data')
            fig.supxlabel('Time (s)')
            fig.supylabel('Temperature (C)')
            fig.set_size_inches(8, 8)
            colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
            for i in range(self.numPrecursors):
                axs[i].plot(self.hTime, self.precursors[i], colors[i])
                axs[i].set_title('Precursor ' + str(i + 1))
            fig.tight_layout()
            fig.savefig('Tool-Data/data/Output_Plots/Precursor Heating Data.png')
            # plt.show()

        else:
            fig = plt.figure()
            fig.suptitle('Precursor Heating Data')
            fig.set_size_inches(8, 8)
            fig.supxlabel('Time (s)')
            fig.supylabel('Temperature (C)')
            fig.tight_layout()
            fig.savefig('Tool-Data/data/Output_Plots/Precursor Heating Data.png')
            # plt.show()
            print("Graphing Aborted: No Precursor Data")


    # Initializes the data stack with the most recent e files
    def initialize(self, e=5):
        # tuples of (filename, creation time)
        times = []
        self.readDir()
        listFiles = self.dir_list
        for i in listFiles:
            filepath = self.heatingDirPath + "/" + i
            # get creation time
            times.append((filepath, os.path.getctime(filepath)))
                
        # sort by creation time
        times.sort(key=lambda x: x[1])

        for _ in range(e):
            self.heatingFilePath = times[_][0]
            self.fileStack.insert(0, self.heatingFilePath)
        print("Initialized Heating Data Stack")


    # Pops the most recent file from the stack and generates the report
    def sendData(self):
        self.heatingFilePath = self.fileStack.pop()
        print(self.heatingFilePath)
        out = self.genReport()
        # print(self.pTime[0])
        self.plotHeating()
        return out
        

# Main function to test the Heating class
def main():
    heating = Heating("Tool-Data/data/Heating-Data")
    heating.initialize()
    heating.sendData()


if __name__ == "__main__":
    main()