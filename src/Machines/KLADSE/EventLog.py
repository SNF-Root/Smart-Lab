import matplotlib.pyplot as plt
import csv
import os
import re
from datetime import datetime
from src.Machines.BaseClasses.EventLog_Base import EventLog_Base


TERMINATING_EVENTS = {"State Changed To Ready", "State Changed To Idle", "State Changed To Aborted"}
FAULT_KEYWORDS = ("Fault", "Alarm")


class EventLog(EventLog_Base):
    """
    A class to represent the EventLog algorithm for the KLA-DSE (Trikon/SPTS "fxPLPXTMC"
    cluster tool control software) Machine.

    Unlike the other machines in this project, KLA-DSE's detailed per-step measured-value
    process trace (Dataloggingscripts\\freshdatabase.sql: WAFER_DATA/STEP_DATA/STEP_MV_DATA/
    STEP_SUMMARY_DATA/MV_DATA) lives in a live SQL Server database, not a portable file -
    the connection details (server/instance, credentials) weren't available in the copy
    this was built from, so that data is not read here. See tool_data/KLA-DSE/notes.txt.

    What IS portable and read here is EventLog\\CurrentEvents.csv: a continuously-growing,
    newest-first log of every module state change, command, transfer, and fault on the
    tool. Each wafer process run shows up as a "DO PROCESS" event (on whichever module ran
    it, e.g. "Rapier") followed - earlier in the file, since it's newest-first - by that
    same module transitioning to Ready/Idle/Aborted. This class bounds and reports on the
    most recent such run.

    Attributes
    ----------
    recipe : str
        the name of the recipe for the run
    wafer : str
        the wafer identifier for the run
    moduleName : str
        the process module that ran the recipe (e.g. "Rapier")
    startTime : datetime
        the run's DO PROCESS timestamp
    endTime : datetime
        the timestamp of the module's next Ready/Idle/Aborted transition
    durationSec : float
        the run duration in seconds
    events : list
        the CSV rows spanning the run, in chronological order
    faults : list
        the subset of events whose Event field mentions a fault or alarm
    dataPath : str
        the path to the directory that contains the data for the machine
    eventLogFilePath : str
        the path to CurrentEvents.csv for the machine
    plotpath : str
        the path to the directory that contains the output plots for the machine
    textpath : str
        the path to the directory that contains the output text for the machine
    recipeIgnores : list
        a list of recipe name substrings to ignore for the machine
    runKey : str
        an identifier for the most recent run, used for process_stack.txt dedup
    outString : str
        the string that contains the output text for the machine

    Methods
    -------
    mostRecentRun():
        Scans CurrentEvents.csv for the most recent DO PROCESS run and returns its identifier
    readRun():
        Reads the full detail of the run identified by runKey
    genReport():
        Generates the report and saves it to the Output_Text directory
    plotEventLog():
        Generates an event timeline plot and saves it to the Output_Plots directory
    initialize():
        Initializes the data stack with the most recent run
    sendData():
        Generates the full report for the most recent run
    sendDataRaw():
        Exports the most recent run's raw event rows to a CSV file and returns its path
    run():
        Runs the EventLog algorithm
    runRaw():
        Runs the EventLog algorithm in raw mode
    """

    def __init__(self, dataPath):
        """
        Constructor for the EventLog class

            Parameters
            ----------
                dataPath : str
                    Path from Tool-Data to the data folder of the machine
        """
        super().__init__(dataPath)
        self.recipeIgnores = ["idle_"]


    def readCsvRows(self):
        """
        Reads CurrentEvents.csv into a list of dicts, in the file's own (newest-first) order.

            Parameters
            ----------
                None

            Returns
            -------
                list: a list of dicts with keys Date/Time, Module, Event, Info
        """
        try:
            with open(self.eventLogFilePath, "r", encoding="utf-8-sig", errors="replace", newline="") as file:
                return list(csv.DictReader(file))
        except FileNotFoundError:
            print("FILE NOT FOUND, PROCESS ABORTED AT: \"src/Machines/KLADSE/EventLog.py\" AT METHOD: readCsvRows(). \n Hint: Try putting in a valid file path.")
            raise FileNotFoundError


    def parseTimestamp(self, value):
        """
        Helper method to parse a CurrentEvents.csv timestamp (DD/MM/YYYY HH:MM:SS).

            Parameters
            ----------
                value: str
                    the timestamp string to parse

            Returns
            -------
                datetime: the parsed timestamp, or None if unparseable
        """
        try:
            return datetime.strptime(value.strip(), "%d/%m/%Y %H:%M:%S")
        except (ValueError, AttributeError):
            return None


    def mostRecentRun(self):
        """
        Scans CurrentEvents.csv for the most recent "DO PROCESS" event and returns a
        unique identifier for it.

            Parameters
            ----------
                None

            Returns
            -------
                str: an identifier for the most recent run, or None if there are none
        """
        rows = self.readCsvRows()
        for row in rows:
            if row.get("Event") == "DO PROCESS":
                return f"{row['Date/Time']}|{row['Module']}|{row['Info']}"
        print("NO PROCESS RUNS FOUND, PROCESS ABORTED AT METHOD: mostRecentRun(). \n Hint: Ansible may have trouble copying CurrentEvents.csv.")
        return None


    def readRun(self):
        """
        Reads the full detail of the run identified by runKey: the recipe, wafer, module,
        start/end time, and the bounded sequence of events between the DO PROCESS event
        and the module's next Ready/Idle/Aborted transition.

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        self.recipe = ""
        self.wafer = ""
        self.moduleName = ""
        self.startTime = None
        self.endTime = None
        self.durationSec = None
        self.events = []
        self.faults = []

        if not self.runKey:
            print("NO RUN SELECTED, PROCESS ABORTED AT: \"src/Machines/KLADSE/EventLog.py\" AT METHOD: readRun(). \n Hint: Try running initialize() first.")
            return

        rows = self.readCsvRows()
        startIdx = None
        for i, row in enumerate(rows):
            key = f"{row['Date/Time']}|{row['Module']}|{row['Info']}"
            if row.get("Event") == "DO PROCESS" and key == self.runKey:
                startIdx = i
                break

        if startIdx is None:
            print(f"RUN NOT FOUND, PROCESS ABORTED AT: \"src/Machines/KLADSE/EventLog.py\" AT METHOD: readRun(). \n Hint: runKey {self.runKey} was not found in CurrentEvents.csv.")
            return

        startRow = rows[startIdx]
        self.moduleName = startRow["Module"]
        self.startTime = self.parseTimestamp(startRow["Date/Time"])

        m = re.search(r"Recipe\s*:\s*(.+?)\s*-\s*Wafer:\s*(.+)$", startRow.get("Info", "").strip())
        if m:
            self.recipe = m.group(1).strip()
            self.wafer = m.group(2).strip()
        else:
            self.recipe = startRow.get("Info", "").strip()

        endIdx = 0
        for i in range(startIdx - 1, -1, -1):
            if rows[i]["Module"] == self.moduleName and rows[i]["Event"] in TERMINATING_EVENTS:
                endIdx = i
                break

        self.endTime = self.parseTimestamp(rows[endIdx]["Date/Time"])
        if self.startTime is not None and self.endTime is not None:
            self.durationSec = (self.endTime - self.startTime).total_seconds()

        self.events = list(reversed(rows[endIdx:startIdx + 1]))
        self.faults = [e for e in self.events if any(k in e["Event"] for k in FAULT_KEYWORDS)]


    def genReport(self):
        """
        Generates a report of the run into an output text file.

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        self.outString = "----------------------------------------------\n\nEVENT LOG REPORT AT " + datetime.now().strftime("%H:%M:%S") + " ON " + datetime.now().strftime("%m/%d/%Y") + "\n\n----------------------------------------------\n\n"
        self.readRun()

        self.outString += "Recipe: " + self.recipe + "\n"
        self.outString += "Wafer: " + self.wafer + "\n"
        self.outString += "Module: " + self.moduleName + "\n\n"
        self.outString += "Start: " + (self.startTime.strftime("%Y-%m-%d %H:%M:%S") if self.startTime else "N/A") + "\n"
        self.outString += "End: " + (self.endTime.strftime("%Y-%m-%d %H:%M:%S") if self.endTime else "N/A") + "\n"
        self.outString += "Duration: " + (f"{self.durationSec:.1f} sec" if self.durationSec is not None else "N/A") + "\n\n"
        self.outString += "----------------------------------------------\n\n"

        if self.faults:
            self.outString += f"Faults/Alarms During Run ({len(self.faults)}):\n\n"
            for f in self.faults:
                self.outString += f"  {f['Date/Time']}  {f['Module']}  {f['Event']}  {f['Info']}\n"
            self.outString += "\n----------------------------------------------\n\n"
        else:
            self.outString += "No faults or alarms during this run.\n\n----------------------------------------------\n\n"

        self.outString += f"Event Sequence ({len(self.events)} events):\n\n"
        for e in self.events:
            self.outString += f"  {e['Date/Time']}  {e['Module']:<10s}  {e['Event']:<24s}  {e['Info']}\n"

        file_path = os.path.join(self.textpath, "EventLog Report.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(self.outString)


    def plotEventLog(self):
        """
        Plots the run's event timeline (time since run start vs. module, colored by
        whether the event was a fault/alarm) and saves it to the Output_Plots directory.

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        path = os.path.join(self.plotpath, "Event Timeline.png")
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

        if self.events and self.startTime is not None:
            modules = sorted({e["Module"] for e in self.events})
            moduleIndex = {m: i for i, m in enumerate(modules)}

            fig, ax = plt.subplots()
            fig.suptitle(f"Event Timeline: {self.recipe} ({self.wafer})")
            fig.set_size_inches(10, max(3, 1.2 * len(modules)))

            for e in self.events:
                t = self.parseTimestamp(e["Date/Time"])
                if t is None:
                    continue
                offset = (t - self.startTime).total_seconds()
                isFault = any(k in e["Event"] for k in FAULT_KEYWORDS)
                color = "tab:red" if isFault else "tab:blue"
                y = moduleIndex[e["Module"]]
                ax.scatter(offset, y, color=color, zorder=3)
                ax.annotate(e["Event"], (offset, y), fontsize=7, rotation=30,
                            xytext=(2, 6), textcoords="offset points")

            ax.set_yticks(range(len(modules)))
            ax.set_yticklabels(modules)
            ax.set_xlabel("Time Since Run Start (s)")
            ax.margins(y=0.4)
            fig.tight_layout()
            fig.savefig(path)
        else:
            fig = plt.figure()
            fig.suptitle("Event Timeline")
            fig.set_size_inches(8, 4)
            fig.tight_layout()
            fig.savefig(path)
            print("GRAPHING ABORTED AT: \"src/Machines/KLADSE/EventLog.py\" AT METHOD: plotEventLog(), No Event Data")


    def sendData(self):
        """
        Generates the full report for the most recent run if it is new.

            Parameters
            ----------
                None

            Returns
            -------
                recipe (str): the name of the recipe for the run, or False if there is no new data
        """
        if not self.runKey:
            return False

        stack = []
        process_path = os.path.join(self.dataPath, "process_stack.txt")
        with open(process_path, "r") as file:
            stack = file.read().splitlines()

        self.readRun()
        if self.ignoreRecipe():
            return False
        elif stack.__len__() == 0:
            with open(process_path, "a+") as file:
                file.write(self.runKey + "\n")
        elif stack.count(self.runKey) > 0:
            return False
        else:
            with open(process_path, "a+") as file:
                file.write(self.runKey + "\n")

        self.genReport()
        self.plotEventLog()
        print("Sent data for run:", self.runKey)
        return self.recipe


    def sendDataRaw(self):
        """
        Exports the most recent run's raw event rows to a CSV file if it is new.
        Returns the file path.

            Parameters
            ----------
                None

            Returns
            -------
                str: the file path of the new raw data export, or None if there is no new data
        """
        if not self.runKey:
            return None

        stack = []
        process_path = os.path.join(self.dataPath, "process_stack.txt")
        with open(process_path, "r") as file:
            stack = file.read().splitlines()

        self.readRun()
        if self.ignoreRecipe():
            return None
        elif stack.__len__() == 0:
            with open(process_path, "a+") as file:
                file.write(self.runKey + "\n")
        elif stack.count(self.runKey) > 0:
            return None
        else:
            with open(process_path, "a+") as file:
                file.write(self.runKey + "\n")

        safeStart = re.sub(r"[^0-9A-Za-z]", "-", self.startTime.isoformat() if self.startTime else "unknown")
        export_path = os.path.join(self.dataPath, f"Run_{safeStart}.csv")
        with open(export_path, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Date/Time", "Module", "Event", "Info"])
            writer.writeheader()
            writer.writerows(self.events)

        print("Sent data for run:", self.runKey)
        return export_path


# Main function to test the EventLog class
def main():
    eventlog = EventLog(os.path.join("src", "Machines", "KLADSE", "data"))
    eventlog.initialize()
    eventlog.sendData()


if __name__ == "__main__":
    main()
