import os
import sqlite3
import time
import uuid
from abc import ABC, abstractmethod


class Job_Base(ABC):

    def __init__(self, dataPath):
        """
        Constructor for the Job class.

            Parameters
            ----------
                dataPath : str
                    Path from Tool-Data to the data folder of the machine
        """
        # Job/Task Info (String / datetime)
        self.taskID = ""
        self.recipe = ""
        self.lotID = ""
        self.status = ""
        self.startTime = ""
        self.endTime = ""
        self.durationSec = 0.0

        # Wafers processed by this job (list of dicts)
        self.wafers = []
        # Recipe steps for this job's process action (list of dicts)
        self.steps = []
        # Recipe phases (cycle sub-steps) for this job's process action (list of dicts)
        self.phases = []

        # File Paths (String)
        self.dataPath = dataPath
        self.dbPath = os.path.join(dataPath, "Databases-Data", "Jobs.db")
        self.plotpath = os.path.join(dataPath, "Output_Plots")
        self.textpath = os.path.join(dataPath, "Output_Text")

        # Recipe Info
        self.recipeIgnores = []

        self.outString = ""


    def openConnection(self, retries=3, delay=1.0):
        """
        Opens a read-only connection to the Jobs.db database, retrying briefly if the
        database is locked by the PTIQ software actively writing to it.

            Parameters
            ----------
                retries: int
                    Number of times to retry connecting if the database is locked.
                delay: float
                    Seconds to wait between retries.

            Returns
            -------
                sqlite3.Connection: a read-only connection to the database
        """
        uri = f"file:{self.dbPath}?mode=ro"
        last_error = None
        for attempt in range(retries):
            try:
                return sqlite3.connect(uri, uri=True)
            except sqlite3.OperationalError as e:
                last_error = e
                time.sleep(delay)
        print(f"DATABASE UNAVAILABLE, PROCESS ABORTED AT METHOD: openConnection(). \n Hint: Check that {self.dbPath} exists and is not exclusively locked.")
        raise last_error


    def guidToStr(self, blob):
        """
        Helper method to convert a 16-byte .NET-style GUID blob (as stored by PTIQ) into
        its standard string representation.

            Parameters
            ----------
                blob: bytes
                    the 16-byte GUID blob

            Returns
            -------
                str: the GUID string, or None if blob is None
        """
        if blob is None:
            return None
        return str(uuid.UUID(bytes_le=blob))


    def guidToBytes(self, guidStr):
        """
        Helper method to convert a GUID string back into the 16-byte .NET-style blob
        used as a key in the Jobs.db tables.

            Parameters
            ----------
                guidStr: str
                    the GUID string

            Returns
            -------
                bytes: the 16-byte GUID blob
        """
        return uuid.UUID(guidStr).bytes_le


    def ignoreRecipe(self):
        """
        Helper method that checks if the current job's recipe is in the ignore list.

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
        Initializes the Job stack with the most recently completed job in Jobs.db.

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        self.taskID = self.mostRecentJob()
        print("Initialized Job Data Stack")


    def mostRecentJob(self):
        """
        Returns the TaskID of the most recently completed job in Jobs.db.

            Parameters
            ----------
                None

            Returns
            -------
                str: the TaskID GUID of the most recently completed job, or None if there are none
        """
        if not os.path.exists(self.dbPath):
            print("DATABASE NOT FOUND, PROCESS ABORTED AT METHOD: mostRecentJob(). \n Hint: Ansible may have trouble copying Jobs.db.")
            return None

        con = self.openConnection()
        try:
            cur = con.cursor()
            cur.execute("SELECT TaskID FROM Jobs WHERE EndDate IS NOT NULL ORDER BY EndDate DESC LIMIT 1;")
            row = cur.fetchone()
        finally:
            con.close()

        if row is None:
            print("NO JOBS FOUND, PROCESS ABORTED AT METHOD: mostRecentJob(). \n Hint: Ansible may have trouble copying Jobs.db.")
            return None
        return self.guidToStr(row[0])


    def run(self):
        """
        Runs the Job algorithm and returns whether or not there is new data.

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
        Runs the Job algorithm and returns the path of the raw data export if there is new data.

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
    def readJob(self):
        """
        Reads the most recently completed job's info, wafers, recipe steps, and recipe
        phases from Jobs.db. Creates the output text string for the report and saves it
        to outString.

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
        Generates a report for the job data and saves it to a text file at textpath

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        pass


    @abstractmethod
    def plotJob(self):
        """
        Plots the job data and saves it to a plot file at plotpath

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
        Exports the job data to a raw file if there is new data. Returns the file path.

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
