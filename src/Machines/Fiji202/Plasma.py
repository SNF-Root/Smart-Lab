import matplotlib.pyplot as plt
import os
from datetime import datetime


class Plasma:
    """
        A class to represent the Plasma algorithm for the Fiji ALD (F202) Machine.
        
        Attributes:
        -----------
        rfTime : list
            Plasma Data (Float in Watts) and Time (Float in ms)
        Plasma : list
            Plasma Data (Float in Watts) and Time (Float in ms)
        PlasmaReflect : list
            Plasma Reflect Data (Float in Watts) and Time (Float in ms)
        cycles : list
            Cycles (int)
        dataPath : string
            Path from Tool-Data to the data folder of the machine
        plasmaFilePath : string
            File path of the plasma data
        plasmaDirPath : string
            File path of the plasma data directory
        plotpath : string
            File path of the plot directory
        textpath : string
            File path of the text directory
        recipe : string
            Recipe Info
        recipes : list
            List of recipes
        recipeIgnores : list
            a list of the names of the recipes to ignore for the machine
        ingredientStack : list
            List of ingredients
        fileStack : list
            List of files
        dir_list : list
            List of directories
        outString : string
            Output string

        Methods:
        --------
        readDir():
            Reads through directory and prints out how many of each recipe is in the directory.
        readFile():
            Reads through the txt file and prints out the recipe, plasma, time, and cycles.
        parseTitles():
            Parses through the titles of the files and counts how many of each recipe is in the directory.
        genReport():
            Generates a report of the plasma data into output text file.
        plotPlasma():
            Plots the Plasma vs Time and saves it as a png file.
        initialize():
            Initializes the Plasma Data Stack with the most recent files.
        sendData():
            Sends the data to the GUI and returns whether or not there is new data.
        sendDataRaw():
            Sends the data to the GUI and returns the file path.
        run():
            Runs the Plasma algorithm and returns whether or not there is new data.
        runRaw():
            Runs the Plasma algorithm and returns the file path.
        """
    
    def __init__(self, dataPath):
        """
        Constructor for the Plasma class.
        
            Parameters
            ----------
                dataPath : str
                    Path from Tool-Data to the data folder of the machine
        """
        # Plasma Data (Float in Watts) and Time (Float in ms)
        self.rfTime = []
        self.Plasma = []
        self.PlasmaReflect = []
        # Cycles (int)
        self.cycles = []

        # File paths (String)
        self.dataPath = dataPath
        self.plasmaFilePath = ""
        self.plasmaDirPath = os.path.join(dataPath, "Plasma-Data")
        self.plotpath = os.path.join(dataPath, "Output_Plots")
        self.textpath = os.path.join(dataPath, "Output_Text")

        # Recipe Info
        self.recipe = ""
        self.recipes = ["Al2O3", "HfO2", "InOx", "NiO", "Pt", "Ru", "SiO2", "Ta2O5", "TaN", "TiN", "TiO2", "WN", "ZrO2"]
        self.recipeIgnores = ["standby", "pulse", "purge"]
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
        path = self.plasmaDirPath
        try:
            self.dir_list = os.listdir(path)
            self.parseTitles()
        except NotADirectoryError:
            print("DIRECTORY NOT FOUND, PROCESS ABORTED AT: \"src/Machines/Fiji202/Plasma.py\" AT METHOD: readDir(). \n Hint: Try putting in a valid directory path.")
            raise NotADirectoryError


    def readFile(self):
        """
        Reads through the txt file and reads data into the rfTime, Plasma, outString, and cycles lists.
        
            Parameters
            ----------
                None
            
            Returns
            -------
                None
        """
        path = self.plasmaFilePath
        self.rfTime = []
        self.Plasma = []
        self.PlasmaReflect = []
        self.cycles = []
        self.recipe = ""
   
        checkPlasma = True
        plasmaCycles = 0

        # If the file is empty
        empty = True
        # Iterator to find line 1 of file, which contains the recipe name at the end
        iter = 0

        try:
            foobar = open(path)
        except FileNotFoundError:
            print("FILE NOT FOUND, PROCESS ABORTED AT: \"src/Machines/Fiji202/Plasma.py\" AT METHOD: readFile(). \n Hint: Try putting in a valid file path.")
            raise FileNotFoundError

        # main loop to read through the file line by line
        with open(path, "r") as file:
            for line in file:
                data = line.strip().replace(" - ", " ").split()
                try:
                    foobar = data[0]
                except IndexError:
                    continue
                # Skip the first line of the file
                if data[0] == "RF":
                    continue

                # If the file is not empty, record the data
                empty = False
                self.rfTime.append(float(data[0]))
                self.Plasma.append(float(data[1]))
                self.PlasmaReflect.append(float(data[2]))
                self.cycles.append(int(data[3]))

                # Find the cycles before plasma starts
                if self.Plasma[-1] != 0 and checkPlasma:
                    plasmaCycles = self.cycles[0] - self.cycles[-1] + 1
                    checkPlasma = False
                    
                iter += 1
                # Find the recipe name
                if iter == 1:
                    for i in range(data.__len__() - 4):
                        self.recipe += data[i+4] + " "
                    self.recipe = self.recipe.strip()
                    for key in self.ingredientStack:
                        if self.recipe.find(key) != -1:
                            self.recipe = key


        # if the file is not empty, structure the report in outString
        if not empty:
            if (self.cycles[0] - self.cycles[-1] + 1) > self.cycles[0]:
                self.outString += "Completed Cycles: " + str(self.cycles[0]) + "/" + str(self.cycles[0]) + "\n\n"
            else:
                self.outString += "Completed Cycles: " + str(self.cycles[0] - self.cycles[-1] + 1) + "/" + str(self.cycles[0]) + "\n\n"
            self.outString += "Cycles Before Plasma Starts: " + str(plasmaCycles) + "\n\n"
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
            print("DIRECTORY IS EMPTY, PROCESS ABORTED AT: \"src/Machines/Fiji202/Plasma.py\" AT METHOD: parseTitles(). \n Hint: Try putting in a directory with files.")
            raise IndexError

        for i in self.dir_list:
            title = i.lower()
            for j in range(self.recipes.__len__()):
                if title.find(self.recipes[j].lower()) != -1:
                    self.ingredientStack.append(self.recipes[j])
                    break
            if (title.find("standby") == -1) and (title.find("pulse") == -1):
                self.ingredientStack.append("Unknown")
        
        # self.outString += "Most Recent: " + str(self.ingredientStack) + "\n\n"


    def genReport(self):
        """
        Generates a report of the plasma data into output text file.

            Parameters
            ----------
                None
            
            Returns
            -------
                None
        """
        self.outString = self.outString = "----------------------------------------------\n\nPLASMA REPORT AT " + datetime.now().strftime("%H:%M:%S") + " ON " + datetime.now().strftime("%m/%d/%Y") + "\n\n----------------------------------------------\n\n"
        self.readFile()
        self.outString += "Recipe: " + self.recipe.upper() + "\n\n----------------------------------------------\n\n"
        # self.readDir()
        file_path = os.path.join(self.textpath, "Plasma Report.txt")
        with open(file_path, "w") as file:
            file.write(self.outString)
        file.close()


    def plotPlasma(self):
        """
        Plots the Plasma vs Time and saves it as a png file at self.plotpath.
            
            Parameters
            ----------
                None
            
            Returns
            -------
                None
        """
        path = os.path.join(self.plotpath, "PlasmaData.png")
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

        # Plotting the Plasma vs Time and Plasma Reflect vs Time
        if (self.rfTime.__len__() > 0):
            if (self.rfTime.__len__() < 1500):
                fig, ax = plt.subplots(2, 1)
                fig.suptitle('Plasma Data')
                fig.set_size_inches(8, 8)
                fig.supxlabel('Time (ms)')
                fig.supylabel('Plasma (Watts)')
                ax[0].plot(self.rfTime, self.Plasma, 'tab:blue')
                ax[1].set_title('Plasma Reflect Data')
                ax[1].plot(self.rfTime, self.PlasmaReflect, 'tab:orange')
                fig.tight_layout()
                # plt.show()
                fig.savefig(path)

            else:
                lastP = self.Plasma[-1500:]
                lastT = self.rfTime[-1500:]
                fig, ax = plt.subplots(3, 1)
                fig.suptitle('Plasma Data')
                fig.set_size_inches(8, 8)
                fig.supxlabel('Time (ms)')
                fig.supylabel('Plasma (Watts)')
                ax[0].plot(self.rfTime, self.Plasma, 'tab:blue')
                ax[1].set_title('Plasma Reflect Data')
                ax[1].plot(self.rfTime, self.PlasmaReflect, 'tab:orange')
                ax[2].set_title('Plasma Last 1500ms')
                ax[2].plot(lastT, lastP, 'tab:green', linestyle='solid')
                fig.tight_layout()
                # plt.show()
                fig.savefig(path)

        else:
            fig = plt.figure()
            fig.suptitle('Plasma Data')
            fig.set_size_inches(8, 8)
            fig.supxlabel('Time (s)')
            fig.supylabel('Plasma (Watts)')
            fig.tight_layout()
            fig.savefig(path)
            # plt.show()
            print("NO DATA TO PLOT, PROCESS ABORTED AT: \"src/Machines/Fiji202/Plasma.py\" AT METHOD: plotPlasma(). \n Hint: Try putting in a file with data.")
            return


    def initialize(self):
        """
        Initializes the Plasma Data Stack with the most recent files.

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        self.plasmaFilePath = self.mostRecent()
        print("Initialized Plasma Data Stack")


    def mostRecent(self):
        """
        Returns the most recent file in the directory.
            
            Parameters
            ----------
                None
            
            Returns
            -------
                times[-1][0] (str): the file path of the most recent file
        """
        # tuples of (filename, creation time)
        self.readDir()
        times = []
        listFiles = self.dir_list
        for i in listFiles:
            filepath = os.path.join(self.plasmaDirPath, i)
            # get creation time
            times.append((filepath, os.path.getctime(filepath)))
        if times.__len__() == 0:
            print("NO FILES FOUND, PROCESS ABORTED AT: \"src/Machines/Fiji202/Plasma.py\" AT METHOD: mostRecent(). \n Hint: Ansible may have trouble copying files.")
            return None
        # sort by creation time
        times.sort(key=lambda x: x[1])
        return times[-1][0]


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
        filename = os.path.basename(self.plasmaFilePath).lower()
        for i in self.recipeIgnores:
            if filename.find(i) != -1:
                return True
        return False
    

    def sendData(self):
        """
        Saves the data to proper output folders if there is new data.
        Returns whether or not there is new data.

            Parameters
            ----------
                None
            
            Returns
            -------
                True (bool): If there is new data
                False (bool): If there is no new data
        """
        stack = []
        process_path = os.path.join(self.dataPath, "process_stack.txt")
        with open(process_path, "r") as file:
            stack = file.read().splitlines()
            file.close()
        if self.ignoreRecipe():
            return False
        elif stack.__len__() == 0:
            with open(process_path, "a+") as file:
                file.write(self.plasmaFilePath + "\n")
                file.close()
        elif stack.count(self.plasmaFilePath) > 0:
            return False
        else:
            with open(process_path, "a+") as file:
                file.write(self.plasmaFilePath + "\n")
                file.close()

        self.genReport()
        self.plotPlasma()
        print("Sent data for:", self.plasmaFilePath)
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
                plasmaFilePath (str): The file path of the plasma data
        """
        stack = []
        process_path = os.path.join(self.dataPath, "process_stack.txt")
        with open(process_path, "r") as file:
            stack = file.read().splitlines()
            file.close()
        if self.ignoreRecipe():
            return None
        elif stack.__len__() == 0:
            with open(process_path, "a+") as file:
                file.write(self.plasmaFilePath + "\n")
                file.close()
        elif stack.count(self.plasmaFilePath) > 0:
            return None
        else:
            with open(process_path, "a+") as file:
                file.write(self.plasmaFilePath + "\n")
                file.close()

        print("Sent data for:", self.plasmaFilePath)
        return self.plasmaFilePath


    def run(self):
        """
        Runs the Plasma algorithm and returns whether or not there is new data.
            
            Parameters
            ----------
                None
            
            Returns
            -------
                True (bool): If there is new data
                False (bool): If there is no new data
        """
        self.initialize()
        return self.sendData()
    

    def runRaw(self):
        """
        Runs the Plasma algorithm and returns the file path if there is new data.
                
            Parameters
            ----------
                None
            
            Returns
            -------
                plasmaFilePath (str): The file path of the plasma data
        """
        self.initialize()
        return self.sendDataRaw()


# Main function to test the Plasma class
def main():
    plasma = Plasma("src/Machines/Fiji202/data(fiji1)")
    plasma.initialize()
    plasma.sendData()


if __name__ == "__main__":
    main()