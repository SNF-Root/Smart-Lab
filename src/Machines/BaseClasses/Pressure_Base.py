import os
from abc import ABC, abstractmethod


class Pressure_Base(ABC):

    def __init__(self, dataPath):
        """
        Constructor for the Pressure class.
        
            Parameters
            ----------
                dataPath : str
                    Path from Tool-Data to the data folder of the machine
        """
        # Pressure Data (Float in Torr) and Time (Float in ms)
        self.pTime = []
        self.Pressure = []
        # Cycles (int)
        self.cycles = []

        # File paths (String)
        self.dataPath = dataPath
        self.pressureFilePath = ""
        self.pressureDirPath = os.path.join(dataPath, "Pressure-Data")
        self.plotpath = os.path.join(dataPath, "Output_Plots")
        self.textpath = os.path.join(dataPath, "Output_Text")

        # Recipe Info
        self.recipe = ""
        # self.recipes = []
        self.recipeIgnores = []
        # self.ingredientStack = []
        # self.fileStack = []
        self.dir_list = []

        self.outString = ""


    def readDir(self):
        """
        Reads through directory and calculates how many of each recipe is in the directory.
        Calls parseTitles() to parse through the titles of the files and count how many of each recipe is in the directory.
        
            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        path = self.pressureDirPath
        try:
            self.dir_list = os.listdir(path)
            self.parseTitles()
        except NotADirectoryError:
            print("DIRECTORY NOT FOUND, PROCESS ABORTED AT METHOD: readDir(). \n Hint: Try putting in a valid directory path.")
            raise NotADirectoryError


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
            print("DIRECTORY IS EMPTY, PROCESS ABORTED AT METHOD: parseTitles. \n Hint: Try putting in a directory with files.")
            pass

        # for i in self.dir_list:
        #     title = i.lower()
        #     for j in range(self.recipes.__len__()):
        #         if title.find(self.recipes[j].lower()) != -1:
        #             self.ingredientStack.append(self.recipes[j])
        #             break
            # if (title.find("standby") == -1) and (title.find("pulse") == -1):
            #     self.ingredientStack.append("Unknown")

    
    def loadBasePressure(self, file_path):
        basePressures = []
        dates = []
        times = []
        with open(file_path, "r") as file:
            for line in file:
                torr, date, time = line.strip().split()
                basePressures.append(float(torr))
                dates.append(date)
                times.append(time)

            if len(basePressures) > 100:
                basePressures = basePressures[-100:]
            file.close()
        return basePressures, dates, times
    

    def initialize(self):
        """
        Initializes the Pressure Data Stack with the most recent files.

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        self.pressureFilePath = self.mostRecent()
        print("Initialized Pressure Data Stack")


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
            filepath = os.path.join(self.pressureDirPath, i)
            # get creation time
            times.append((filepath, os.path.getctime(filepath)))
        if times.__len__() == 0:
            print("NO FILES FOUND, PROCESS ABORTED AT METHOD: mostRecent(). \n Hint: Ansible may have trouble copying files.")
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
        filename = os.path.basename(self.pressureFilePath).lower()
        for i in self.recipeIgnores:
            if filename.find(i) != -1:
                return True
        return False
    

    def run(self):
        """
        Runs the Pressure algorithm and returns whether or not there is new data.
            
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
        Runs the Pressure algorithm and returns the file path if there is new data.
                
            Parameters
            ----------
                None
            
            Returns
            -------
                pressureFilePath (str): The file path of the pressure data
        """
        self.initialize()
        return self.sendDataRaw()
    





    @abstractmethod
    def readFile(self):
        """
        Reads through the txt file and reads data into the pTime, Pressure, outString, and cycles lists.
        
            Parameters
            ----------
                None
            
            Returns
            -------
                None
        """
        pass


    @abstractmethod
    def genReport(self):
        """
        Generates a report of the data and saves it to a the file at textpath.
        
            Parameters
            ----------
                None
            
            Returns
            -------
                None
        """
        pass

    
    @abstractmethod
    def plotPressure(self):
        """
        Plots the Pressure data and saves it to png files at plotpath.
        
            Parameters
            ----------
                None
            
            Returns
            -------
                None
        """
        pass


    @abstractmethod
    def sendData(self):
        """
        Saves the data to proper output folders if there is new data.
        Returns the recipe name.
        
            Parameters
            ----------
                None
            
            Returns
            -------
                None
        """
        pass


    @abstractmethod
    def sendDataRaw(self):
        """
        Saves the data to proper output folders if there is new data.
        Returns the file path.
        
            Parameters
            ----------
                None
            
            Returns
            -------
                pressureFilePath (str): The file path of the pressure data
        """
        pass


def main():
    return


if __name__ == "__main__":
    main()