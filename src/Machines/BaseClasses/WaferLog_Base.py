import os
from abc import ABC, abstractmethod


class WaferLog_Base(ABC):

    def __init__(self, dataPath):
        """
        Constructor for the WaferLog class.

            Parameters
            ----------
                dataPath : str
                    Path from Tool-Data to the data folder of the machine
        """
        # Run Metadata (String / datetime in ms from run start)
        self.machineID = ""
        self.waferID = ""
        self.loggingSpec = ""
        self.startTime = ""
        self.endTime = ""
        self.durationSec = 0.0

        # Step Data (list of dicts, one per recipe step, keyed by "<name> (<unit>)")
        self.steps = []
        self.numStepsDeclared = 0

        # Process sequence summary (dict of step number -> {"set": float, "actual": float})
        self.processSummary = {}

        # Historical Channel Data (Float ms) and (Float or None)
        self.channelNames = []
        self.channelUnits = []
        self.channelTime = []
        self.channelData = []

        # File Paths (String)
        self.dataPath = dataPath
        self.waferLogFilePath = ""
        self.waferLogDirPath = os.path.join(dataPath, "WaferLog-Data")
        self.plotpath = os.path.join(dataPath, "Output_Plots")
        self.textpath = os.path.join(dataPath, "Output_Text")

        # Recipe Info
        self.recipe = ""
        self.recipeIgnores = []
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
        path = self.waferLogDirPath
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
            print("DIRECTORY IS EMPTY, PROCESS ABORTED AT METHOD: parseTitles(). \n Hint: Try putting in a directory with files.")
            pass


    def initialize(self):
        """
        Initializes the WaferLog Data Stack with the most recent files

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        self.waferLogFilePath = self.mostRecent()
        print("Initialized WaferLog Data Stack")


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
            filepath = os.path.join(self.waferLogDirPath, i)
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
        filename = os.path.basename(self.waferLogFilePath).lower()
        for i in self.recipeIgnores:
            if filename.find(i) != -1:
                return True
        return False


    def run(self):
        """
        Runs the WaferLog algorithm and returns whether or not there is new data.

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
        Runs the WaferLog algorithm and returns the file path if there is new data.

            Parameters
            ----------
                None

            Returns
            -------
                waferLogFilePath (str): the file path of the new data
        """
        self.initialize()
        return self.sendDataRaw()


    @abstractmethod
    def readFile(self):
        """
        Reads through the historical wafer log file and parses the run metadata, step table,
        channel history, and process sequence summary. Creates the output text string for the
        report and saves it to outString.

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
        Generates a report for the WaferLog data and saves it to a text file at textpath

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        pass


    @abstractmethod
    def plotWaferLog(self):
        """
        Plots the WaferLog data and saves it to a plot file at plotpath

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
                waferLogFilePath (str): the file path of the new data
        """
        pass


def main():
    return


if __name__ == "__main__":
    main()
