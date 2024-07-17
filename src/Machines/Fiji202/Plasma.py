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
        self.plasmaDirPath = dataPath + "/Plasma-Data"
        self.plotpath = dataPath + "/Output_Plots"
        self.textpath = dataPath + "/Output_Text"

        # Recipe Info
        self.recipe = ""
        self.recipes = ["Al2O3", "TiO2", "HfO2", "ZrO2", "ZnO", "Ru", "Pt", "Ta2O5"]
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
        path = self.plasmaDirPath
        try:
            self.dir_list = os.listdir(path)
            self.parseTitles()
        except NotADirectoryError:
            print("DIRECTORY NOT FOUND, PROCESS ABORTED. \n Hint: Try putting in a valid directory path.")
            return


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
                if data[0] == "Plasma":
                    continue

                # If the file is not empty, record the data
                empty = False
                self.rfTime.append(float(data[0]))
                self.Plasma.append(float(data[1]))
                self.PlasmaReflect.append(float(data[2]))
                self.cycles.append(int(data[3]))

                iter += 1
                # Find the recipe name
                if iter == 1:
                    for i in range(data.__len__() - 4):
                        self.recipe += data[i+4] + " "
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
        file_path = self.textpath + "/Plasma Report.txt"
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
        path = self.plotpath + "/PlasmaData.png"
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
            print("NO DATA TO PLOT, PROCESS ABORTED. \n Hint: Try putting in a file with data.")
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
        # tuples of (filename, creation time)
        times = []
        self.readDir()
        listFiles = self.dir_list
        for i in listFiles:
            filepath = self.plasmaDirPath + "/" + i
            # get creation time
            times.append((filepath, os.path.getctime(filepath)))
                
        # sort by creation time
        times.sort(key=lambda x: x[1])
        self.plasmaFilePath = times[-1][0]
        print("Initialized Plasma Data Stack")


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
        filename = self.plasmaFilePath.replace("\\", "/").lower()
        filename =filename.split("/")
        filename = filename[-1]
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
        with open(self.dataPath + "/process_stack.txt", "r") as file:
            stack = file.read().splitlines()
            file.close()
        if self.ignoreRecipe():
            return False
        elif stack.__len__() == 0:
            print("process stack empty")
            with open(self.dataPath + "/process_stack.txt", "a+") as file:
                file.write(self.plasmaFilePath + "\n")
                file.close()
        elif stack.count(self.plasmaFilePath) > 0:
            return False
        else:
            with open(self.dataPath + "/process_stack.txt", "a+") as file:
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
        with open(self.dataPath + "/process_stack.txt", "r") as file:
            stack = file.read().splitlines()
            file.close()
        if self.ignoreRecipe():
            return None
        elif stack.__len__() == 0:
            print("THE STACK IS EMPTY")
            with open(self.dataPath + "/process_stack.txt", "a+") as file:
                file.write(self.plasmaFilePath + "\n")
                file.close()
        elif stack.count(self.plasmaFilePath) > 0:
            return None
        else:
            with open(self.dataPath + "/process_stack.txt", "a+") as file:
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