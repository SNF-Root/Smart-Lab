import matplotlib.pyplot as plt
import os
from datetime import datetime
from abc import ABC, abstractmethod


class Heating_Base(ABC):

    def __init__(self, dataPath):
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
        self.heatingDirPath = os.path.join(dataPath, "Heating-Data")
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
            print("DIRECTORY NOT FOUND, PROCESS ABORTED AT: \"src/Machines/Fiji202/Heating.py\" AT METHOD: readDir(). \n Hint: Try putting in a valid directory path.")
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
            print("DIRECTORY IS EMPTY, PROCESS ABORTED AT: \"src/Machines/Fiji202/Heating.py\" AT METHOD: parseTitles(). \n Hint: Try putting in a directory with files.")
            raise IndexError
        
        # for i in self.dir_list:
        #     title = i.lower()
        #     for j in range(self.recipes.__len__()):
        #         if title.find(self.recipes[j].lower()) != -1:
        #             self.ingredientStack.append(self.recipes[j])
        #             break
            # if (title.find("standby") == -1) and (title.find("pulse") == -1):
            #     self.ingredientStack.append("Unknown")


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
        self.heatingFilePath = self.mostRecent()
        print("Initialized Heating Data Stack")

    
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
            filepath = os.path.join(self.heatingDirPath, i)
            # get creation time
            times.append((filepath, os.path.getctime(filepath)))
        if times.__len__() == 0:
            print("NO FILES FOUND, PROCESS ABORTED AT: \"src/Machines/Fiji202/Heating.py\" AT METHOD: mostRecent(). \n Hint: Ansible may have trouble copying files.")
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
        filename = os.path.basename(self.heatingFilePath).lower()
        for i in self.recipeIgnores:
            if filename.find(i) != -1:
                return True
        return False


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
    





    @abstractmethod
    def readFile(self):
        """
        Reads through the txt file and reads data from files for the heater.
        Creates full text string for the output file and saves it to outString.
        
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
        Generates a report for the Heating data and saves it to a text file at text path
        
            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        pass


    @abstractmethod
    def plotHeating(self):
        """
        Plots the Heating data and saves it to a plot file at plot path
        
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
        Pops the most recent file from the stack and generates the full report.
        
            Parameters
            ----------
                None

            Returns
            -------
                True (bool): if there is new data
                False (bool): if there is no new data
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
                heatingFilePath (str): the file path of the new data
        """
        pass
    

def main():
    return


if __name__ == "__main__":
    main()