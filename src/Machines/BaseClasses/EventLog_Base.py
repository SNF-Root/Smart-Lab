import os
from abc import ABC, abstractmethod


class EventLog_Base(ABC):

    def __init__(self, dataPath):
        """
        Constructor for the EventLog class.

            Parameters
            ----------
                dataPath : str
                    Path from Tool-Data to the data folder of the machine
        """
        # Run Info (String / datetime)
        self.recipe = ""
        self.wafer = ""
        self.moduleName = ""
        self.startTime = None
        self.endTime = None
        self.durationSec = None

        # Events for the bounded run (list of dicts: time, module, event, info)
        self.events = []
        # Fault/alarm events encountered during the run (subset of events)
        self.faults = []

        # File Paths (String)
        self.dataPath = dataPath
        self.eventLogFilePath = os.path.join(dataPath, "EventLog-Data", "CurrentEvents.csv")
        self.plotpath = os.path.join(dataPath, "Output_Plots")
        self.textpath = os.path.join(dataPath, "Output_Text")

        # Recipe Info
        self.recipeIgnores = []

        # Identifier for the most recent run, used for process_stack.txt dedup
        self.runKey = ""

        self.outString = ""


    def ignoreRecipe(self):
        """
        Helper method that checks if the current run's recipe is in the ignore list.

            Parameters
            ----------
                None

            Returns
            -------
                True (bool): if the recipe is in the ignore list
                False (bool): if the recipe is not in the ignore list
        """
        recipe = (self.recipe or "").lower()
        for i in self.recipeIgnores:
            if recipe.find(i) != -1:
                return True
        return False


    def initialize(self):
        """
        Initializes the EventLog stack with the most recent process run found in the
        event log.

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        self.runKey = self.mostRecentRun()
        print("Initialized EventLog Data Stack")


    def run(self):
        """
        Runs the EventLog algorithm and returns whether or not there is new data.

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
        Runs the EventLog algorithm and returns the path of the raw data export if there
        is new data.

            Parameters
            ----------
                None

            Returns
            -------
                str: the file path of the new raw data export
        """
        self.initialize()
        return self.sendDataRaw()


    @abstractmethod
    def mostRecentRun(self):
        """
        Scans the event log for the most recent process run and returns a unique
        identifier for it (used both to key process_stack.txt dedup and to re-locate
        the run when reading its full detail).

            Parameters
            ----------
                None

            Returns
            -------
                str: an identifier for the most recent run, or None if there are none
        """
        pass


    @abstractmethod
    def readRun(self):
        """
        Reads the full detail (recipe, wafer, module, start/end time, events, faults) of
        the run identified by runKey. Creates the output text string for the report and
        saves it to outString.

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
        Generates a report for the run and saves it to a text file at textpath

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        pass


    @abstractmethod
    def plotEventLog(self):
        """
        Plots the run's event timeline and saves it to a plot file at plotpath

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
        Exports the run's raw event rows to a file if there is new data. Returns the
        file path.

            Parameters
            ----------
                None

            Returns
            -------
                str: the file path of the new raw data export
        """
        pass


def main():
    return


if __name__ == "__main__":
    main()
