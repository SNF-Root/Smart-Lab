import matplotlib.pyplot as plt
import os
from datetime import datetime


class Heating:
    """
    A class to represent the Heating algorithm for the Fiji ALD (F202) Machine

    Attributes
    ----------
    hTime : list
        a list of the time data for the heater
    cone : list
        a list of the cone data for the heater
    reactor1 : list
        a list of the reactor1 data for the heater
    reactor2 : list
        a list of the reactor2 data for the heater
    chuck : list
        a list of the chuck data for the heater
    pDelivery : list
        a list of the pDelivery data for the heater
    aldValves : list
        a list of the aldValves data for the heater
    precursors : list
        a list of lists of the precursor data for the heater
    mfc1 : list
        a list of the mfc1 data for the heater
    numPrecursors : int
        the number of precursors in the data
    cycles : list
        a list of the cycles data for the heater
    dataPath : str
        the path to the directory that contains the data for the machine
    heatingFilePath : str
        the path to the file that contains the heating data for the machine
    heatingDirPath : str
        the path to the directory that contains the heating data for the machine
    plotpath : str
        the path to the directory that contains the output plots for the machine
    textpath : str
        the path to the directory that contains the output text for the machine
    currentRecipe : str
        the name of the recipe for the machine
    recipes : list
        a list of the names of the recipes for the machine
    recipeIgnores : list
        a list of the names of the recipes to ignore for the machine
    ingredientStack : list
        a list of the names of the ingredients for the machine
    fileStack : list
        a list of the file paths for the machine
    dir_list : list
        a list of the file names in the directory for the machine
    outString : str
        the string that contains the output text for the machine

    Methods
    -------
    readDir():
        Reads through directory and prints out how many of each recipe is in the directory
    readFile():
        Reads through the txt file and prints out the recipe, pressure, time, and cycles
    parseTitles():
        Parses through the titles of the files and counts how many of each recipe is in the directory
    averageTemp():
        Helper method to calculate the average temperature of each precursor
    genReport():
        Generates the report and returns it as a string
    plotHeating():
        Generates a plot of the data and saves it to the Output_Plots directory
    initialize():
        Initializes the data stack with the most recent files
    sendData():
        Pops the most recent file from the stack and generates the full report
    sendDataRaw():
        Pops the most recent file from the stack and generates the full report
    run():
        Runs the Heating algorithm
    runRaw():
        Runs the Heating algorithm
    """
    
    def __init__(self, dataPath):
        """
        Constructor for the Heating class

            Parameters
            ----------
                dataPath : str
                    Path from Tool-Data to the data folder of the machine
        """
        # Heater Data (Floats in Celcius) and Time (Float in s)
        self.hTime = []
        self.cone = []
        self.reactor1 = []
        self.reactor2 = []
        self.chuck = []
        self.pDelivery = []
        self.aldValves = []
        self.precursors = [[], [], [], [], []]
        self.mfc1 = []
        self.numPrecursors = 0
        # Cycles (int)
        self.cycles = []

        # File Paths (String)
        self.dataPath = dataPath
        self.heatingFilePath = ""
        self.heatingDirPath = dataPath + "/Heating-Data"
        self.plotpath = dataPath + "/Output_Plots"
        self.textpath = dataPath + "/Output_Text"

        # Recipe Info
        self.currentRecipe = ""
        self.recipes = ["Al2O3", "HfO2", "InOx", "NiO", "Pt", "Ru", "SiO2", "Ta2O5", "TaN", "TiN", "TiO2", "WN", "ZrO2"]
        self.recipeIgnores = ["standby", "pulse"]
        self.ingredientStack = []
        self.fileStack = []
        self.dir_list = []

        self.outString = ""


    def readDir(self):
        """
        Reads through directory and prints out how many of each recipe is in the directory.
        Calls parseTitles() to parse through the titles of the files and count how many of each recipe is in the directory.

            Parameters
            ----------
                None
            
            Returns
            -------
                None
        """
        path = self.heatingDirPath
        try:
            self.dir_list = os.listdir(path)
            self.parseTitles()
        except NotADirectoryError:
            print("DIRECTORY NOT FOUND, PROCESS ABORTED. \n Hint: Try putting in a valid directory path.")
            return


    def readFile(self):
        """
        Reads through the txt file and reads data for the heater.
        
            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        path = self.heatingFilePath
        self.hTime = []
        self.cone = []
        self.reactor1 = []
        self.reactor2 = []
        self.chuck = []
        self.pDelivery = []
        self.aldValves = []
        self.precursors = [[], [], [], [], []]
        self.mfc1 = []
        self.numPrecursors = 0
        self.cycles = []
        self.currentRecipe = ""

        chuckMax = 0
        reactor1Max = 0
        reactor2Max = 0
        precursorsMax = [0, 0, 0, 0, 0]
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
                self.cone.append(float(data[1]))
                self.reactor1.append(float(data[2]))
                self.reactor2.append(float(data[3]))
                self.chuck.append(float(data[4]))
                self.pDelivery.append(float(data[5]))
                self.aldValves.append(float(data[6]))
                
                if data[2] > reactor1Max:
                    reactor1Max = data[2]
                if data[3] > reactor2Max:
                    reactor2Max = data[3]
                if data[4] > chuckMax:
                    chuckMax = data[4]

                # Find the number of precursors
                for i in range(5):
                    self.precursors[i].append(float(data[i + 7]))
                    if data[i + 7] > precursorsMax[i]:
                        precursorsMax[i] = data[i + 7]

                # record mfc1 and cycles data which is after the precursor data
                self.mfc1.append(float(data[14]))
                self.cycles.append(int(data[16]))

                iter += 1
                # Find the recipe name
                if iter == 1:
                    for j in range(17, data.__len__()):
                        self.currentRecipe += data[j] + " "
                    self.currentRecipe = self.currentRecipe.strip()
                    for key in self.ingredientStack:
                        if self.currentRecipe.find(key) != -1:
                            self.currentRecipe = key


        errorMessage = ""

        if reactor1Max >= 275:
            errorMessage += f"Reactor 1 Max Temp Exceeded At {reactor1Max}" + "\u00b0 C" + "\n\n"
        if reactor2Max >= 275:
            errorMessage += f"Reactor 2 Max Temp Exceeded At {reactor2Max}" + "\u00b0 C" + "\n\n"
        if chuckMax >= 275:
            errorMessage += f"Chuck Max Temp Exceeded At {chuckMax}" + "\u00b0 C" + "\n\n"
        for i in range(5):
            if precursorsMax[i] >= 275:
                errorMessage += f"Precursor {i+1} Max Temp Exceeded At {precursorsMax[i]}" + "\u00b0 C" + "\n\n"
            if precursorsMax[i] != 0.0:
                self.numPrecursors += 1
                
            
        # if the file is not empty, print out the data
        if not empty:
            if (self.cycles[0] - self.cycles[-1] + 1) > self.cycles[0]:
                self.outString += "Completed Cycles: " + str(self.cycles[0]) + "/" + str(self.cycles[0]) + "\n\n"
            else:
                self.outString += "Completed Cycles: " + str(self.cycles[0] - self.cycles[-1] + 1) + "/" + str(self.cycles[0]) + "\n\n"
            self.outString += "Number of Precursors Heated: " + str(self.numPrecursors) + "\n\n"
            self.outString += "Cone Final Temp: " + str(self.cone[-1]) + "\u00b0 C" + "\n\n"
            self.outString += "Reactor 1 Final Temp: " + str(self.reactor1[-1]) + "\u00b0 C" + "\n\n"
            self.outString += "Reactor 2 Final Temp: " + str(self.reactor2[-1]) + "\u00b0 C" + "\n\n"
            self.outString += "Chuck Final Temp: " + str(self.chuck[-1]) + "\u00b0 C" + "\n\n"
            self.outString += "Precursor Delivery Final Temp: " + str(self.pDelivery[-1]) + "\u00b0 C" + "\n\n"
            self.outString += "ALD Valves Final Temp: " + str(self.aldValves[-1]) + "\u00b0 C" + "\n\n"
            self.averageTemp(precursorsMax)
            if errorMessage != "":
                self.outString += "ERRORS: \n" + errorMessage
        file.close()


    def parseTitles(self):
        """
        Parses through the titles of the files and counts how many of each recipe is in the directory.
        
            Parameters
            ----------
                None
            
            Returns
            -------
                None
        """
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


    def averageTemp(self, precursorMax):
        """
        Helper method to calculate the average temperature of each precursor.

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        for i in range(5):
            if precursorMax[i] == 0.0:
                continue
            else:
                sum = 0
                for j in self.precursors[i]:
                    sum += j
            self.outString += "Average Temp of Precursor " + str(i+1) + ": " + str(round(sum/self.precursors[i].__len__(), 1)) + "\u00b0 C" + "\n\n"
            # print("Average Temp of Precursor", i+1, ":", str(round(sum/precursors[i].__len__(), 1)) +  "\u00b0 C")


    def genReport(self):
        """
        Generates a report of the heating data into output text file.

            Parameters
            ----------
                None
            
            Returns
            -------
                None
        """
        self.outString = "----------------------------------------------\n\nHEATING REPORT AT " + datetime.now().strftime("%H:%M:%S") + " ON " + datetime.now().strftime("%m/%d/%Y") + "\n\n----------------------------------------------\n\n"
        self.readFile()
        self.outString += "Recipe: " + self.currentRecipe.upper() + "\n\n----------------------------------------------\n\n"
        # self.readDir()
        file_path = self.textpath + "/Heating Report.txt"
        with open(file_path, "w") as file:
            file.write(self.outString)
        file.close()


    def plotHeating(self):
        """
        Generates a plot of the heating data and saves it to the Output_Plots directory.

            Parameters
            ----------
                None
            
            Returns
            -------
                None
        """
        p_path = self.plotpath + "/Precursor Heating Data.png"
        np_path = self.plotpath + "/Non-Precursor Heating Data.png"
        try:
            os.remove(np_path)
        except FileNotFoundError:
            pass
        try:
            os.remove(p_path)
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
        fig.savefig(np_path)
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
            fig.savefig(p_path)
            # plt.show()

        else:
            fig = plt.figure()
            fig.suptitle('Precursor Heating Data')
            fig.set_size_inches(8, 8)
            fig.supxlabel('Time (s)')
            fig.supylabel('Temperature (C)')
            fig.tight_layout()
            fig.savefig(p_path)
            # plt.show()
            print("Graphing Aborted: No Precursor Data")


    def initialize(self):
        """
        Initializes the Heating Data Stack with the most recent files

            Parameters
            ----------
                None
            
            Returns
            -------
                None
        """
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
        self.heatingFilePath = times[-1][0]
        print("Initialized Heating Data Stack")


    def ignoreRecipe(self):
        """
        Helper method that checks if the current recipe is in the ignore list.

            Parameters
            ----------
                None
            
            Returns
            -------
                True (bool): if the recipe is in the ignore list
                False (bool): if the recipe is not in the ignore list
        """
        filename = self.heatingFilePath.replace("\\", "/").lower()
        filename =filename.split("/")
        filename = filename[-1]
        for i in self.recipeIgnores:
            if filename.find(i) != -1:
                return True
        return False

    def sendData(self):
        """
        Pops the most recent file from the stack and generates the full report.
            
            Parameters
            ----------
                None
            
            Returns
            -------
                True (bool): if there is new data
                False (bool): if there is no new data
        """
        stack = []
        with open(self.dataPath + "/process_stack.txt", "r") as file:
            stack = file.read().splitlines()
            file.close()
        if self.ignoreRecipe():
            return False
        elif stack.__len__() == 0:
            print("process stack empty")
            with open(self.dataPath + "/process_stack.txt", "a+") as file:
                file.write(self.heatingFilePath + "\n")
                file.close()
        elif stack.count(self.heatingFilePath) > 0:
            return False
        else:
            with open(self.dataPath + "/process_stack.txt", "a+") as file:
                file.write(self.heatingFilePath + "\n")
                file.close()

        self.genReport()
        self.plotHeating()
        print("Sent data for:", self.heatingFilePath)
        return True

    
    def sendDataRaw(self):
        """
        Saves the data to proper output folders if there is new data.
        Returns the file path.
        
            Parameters
            ----------
                None

            Returns
            -------
                heatingFilePath (str): the file path of the new data
        """
        stack = []
        print("RECIPE:", self.currentRecipe)
        with open(self.dataPath + "/process_stack.txt", "r") as file:
            stack = file.read().splitlines()
            file.close()
        if self.ignoreRecipe():
            return None
        elif stack.__len__() == 0:
            print("THE P STACK IS EMPTY")
            with open(self.dataPath + "/process_stack.txt", "a+") as file:
                file.write(self.heatingFilePath + "\n")
                file.close()
        elif stack.count(self.heatingFilePath) > 0:
            return None
        else:
            with open(self.dataPath + "/process_stack.txt", "a+") as file:
                file.write(self.heatingFilePath + "\n")
                file.close()

        print("Sent data for:", self.heatingFilePath)
        return self.heatingFilePath


    def run(self):
        """
        Runs the Heating algorithm and returns whether or not there is new data.

            Parameters
            ----------
                None

            Returns
            -------
                True (bool): if there is new data
                False (bool): if there is no new data
        """
        self.initialize()
        return self.sendData()
    

    def runRaw(self):
        """
        Runs the Heating algorithm and returns the file path if there is new data.

            Parameters
            ----------
                None

            Returns
            -------
                heatingFilePath (str): the file path of the new data
        """
        self.initialize()
        return self.sendDataRaw()



# Main function to test the Heating class
def main():
    heating = Heating("src/Machines/Fiji202/data")
    heating.initialize()
    heating.sendData()


if __name__ == "__main__":
    main()