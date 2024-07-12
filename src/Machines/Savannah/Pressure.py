import matplotlib.pyplot as plt
import os
from datetime import datetime


class Pressure:
    # Constructor
    # dataPath: the path to the directory that contains the data for the machine
    def __init__(self, dataPath):
        # Pressure Data (Float in Torr) and Time (Float in ms)
        self.pTime = []
        self.Pressure = []
        # Cycles (int)
        self.cycles = []

        # File paths (String)
        self.dataPath = dataPath
        self.pressureFilePath = ""
        self.pressureDirPath = dataPath + "/Pressure-Data"
        self.plotpath = dataPath + "/Output_Plots"
        self.textpath = dataPath + "/Output_Text"

        # Recipe Info
        self.recipe = ""
        self.recipes = ["Al2O3", "TiO2", "HfO2", "ZrO2", "ZnO", "Ru", "Pt", "Ta2O5"]
        self.ingredientStack = []
        self.fileStack = []
        self.dir_list = []

        self.outString = ""


    # Reads through directory and prints out how many of each recipe is in the directory
    def readDir(self):
        path = self.pressureDirPath
        try:
            self.dir_list = os.listdir(path)
            self.parseTitles()
        except NotADirectoryError:
            print("DIRECTORY NOT FOUND, PROCESS ABORTED. \n Hint: Try putting in a valid directory path.")
            return


    # Reads through the txt file and prints out the recipe, pressure, time, and cycles
    def readFile(self):
        path = self.pressureFilePath
        self.pTime = []
        self.Pressure = []
        self.cycles = []
        self.recipe = ""
       
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
                data = line.strip().replace(" - ", " ").split()
                try:
                    foobar = data[0]
                except IndexError:
                    continue
                if data[0] == "Pressure":
                    continue

                # If the file is not empty, record the data
                empty = False
                self.pTime.append(float(data[0]))
                self.Pressure.append(float(data[1]))
                self.cycles.append(int(data[2]))

                iter += 1
                # Find the recipe name
                if iter == 1:
                    for i in range(data.__len__() - 3):
                        self.recipe += data[i+3] + " "
                    self.recipe = self.recipe.strip()
                    for key in self.ingredientStack:
                        if self.recipe.find(key) != -1:
                            self.recipe = key


        # if the file is not empty, print out the data
        if not empty:
            if (self.cycles[0] - self.cycles[-1] + 1) > self.cycles[0]:
                self.outString += "Completed Cycles: " + str(self.cycles[0]) + "/" + str(self.cycles[0]) + "\n\n"
            else:
                self.outString += "Completed Cycles: " + str(self.cycles[0] - self.cycles[-1] + 1) + "/" + str(self.cycles[0]) + "\n\n"
        file.close()

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


    # Generates a report of the pressure data and returns it as a string
    def genReport(self):
        self.outString = self.outString = "----------------------------------------------\n\nPRESSURE REPORT AT " + datetime.now().strftime("%H:%M:%S") + " ON " + datetime.now().strftime("%m/%d/%Y") + "\n\n----------------------------------------------\n\n"
        self.readFile()
        self.outString += "Recipe: " + self.recipe.upper() + "\n\n----------------------------------------------\n\n"
        # self.readDir()
        file_path = self.textpath + "/Pressure Report.txt"
        with open(file_path, "w") as file:
            file.write(self.outString)
        file.close()
        return self.outString


    # Plots the Pressure vs Time and saves it as a png file
    def plotPressure(self):
        path = self.plotpath + "/PressureData.png"
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

        # Plotting the Pressure vs Time
        if (self.pTime.__len__() > 0):
            if (self.pTime.__len__() < 1500):
                fig, ax = plt.subplots()
                fig.suptitle('Pressure Data')
                fig.set_size_inches(8, 8)
                fig.supxlabel('Time (ms)')
                fig.supylabel('Pressure (Torr)')
                ax.plot(self.pTime, self.Pressure)
                fig.tight_layout()
                # plt.show()
                fig.savefig(path)

            else:
                lastP = self.Pressure[-1500:]
                lastT = self.pTime[-1500:]
                fig, ax = plt.subplots(2, 1)
                fig.suptitle('Pressure Data')
                fig.set_size_inches(8, 8)
                fig.supxlabel('Time (ms)')
                fig.supylabel('Pressure (Torr)')
                ax[0].plot(self.pTime, self.Pressure, 'tab:blue')
                ax[1].set_title('Pressure Last 1500ms')
                ax[1].plot(lastT, lastP, 'tab:orange', linestyle='solid')
                fig.tight_layout()
                # plt.show()
                fig.savefig(path)

        else:
            fig = plt.figure()
            fig.suptitle('Precursor Heating Data')
            fig.set_size_inches(8, 8)
            fig.supxlabel('Time (s)')
            fig.supylabel('Pressure (Torr)')
            fig.tight_layout()
            fig.savefig(path)
            # plt.show()
            print("NO DATA TO PLOT, PROCESS ABORTED. \n Hint: Try putting in a file with data.")
            return


    # Initializes the Pressure Data Stack with the most recent files
    def initialize(self):
        # tuples of (filename, creation time)
        times = []
        self.readDir()
        listFiles = self.dir_list
        for i in listFiles:
            filepath = self.pressureDirPath + "/" + i
            # get creation time
            times.append((filepath, os.path.getctime(filepath)))
                
        # sort by creation time
        times.sort(key=lambda x: x[1])
        self.pressureFilePath = times[-1][0]
        print("Initialized Pressure Data Stack")


    # Sends the data to the GUI
    # returns whether or not there is new data
    def sendData(self):
        stack = []
        with open(self.dataPath + "/process_stack.txt", "r") as file:
            stack = file.read().splitlines()
            file.close()
        if stack.__len__() == 0:
            print("THE H STACK IS EMPTY")
            with open(self.dataPath + "/process_stack.txt", "a+") as file:
                file.write(self.pressureFilePath + "\n")
                file.close()
        elif stack.count(self.pressureFilePath) > 0:
            return False
        else:
            with open(self.dataPath + "/process_stack.txt", "a+") as file:
                file.write(self.pressureFilePath + "\n")
                file.close()

        self.genReport()
        self.plotPressure()
        print("Sent data for:", self.pressureFilePath)
        return True


    # Runs the Pressure algorithm
    # returns whether or not there is new data
    def run(self):
        self.initialize()
        return self.sendData()


# Main function to test the Pressure class
def main():
    pressure = Pressure("src/Machines/Savannah/data")
    pressure.initialize()
    pressure.sendData()


if __name__ == "__main__":
    main()