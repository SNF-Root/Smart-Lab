import matplotlib.pyplot as plt
import os
import re
from datetime import datetime
from src.Machines.BaseClasses.WaferLog_Base import WaferLog_Base


class WaferLog(WaferLog_Base):
    """
    A class to represent the WaferLog algorithm for the HDPCVD (Plasma-Therm VersaLine) Machine.

    Parses the "HistoricalDataLogger" text file that VersaLine's HDPCVD/etch process module
    writes out for every wafer it runs (found under HistoricalWaferDataLogs/<Module> on the
    tool PC). Each file describes exactly one wafer run: run metadata, the recipe's step
    table, any endpoint-detector channel history recorded during the run, and a process
    sequence summary of set vs. actual step times.

    Attributes
    ----------
    machineID : str
        the module/chamber identifier reported by the tool (e.g. "CTC")
    waferID : str
        the wafer identifier for the run
    loggingSpec : str
        the name of the logging specification used to record the run
    startTime : str
        the run start timestamp as reported in the file
    endTime : str
        the run end timestamp as reported in the file
    durationSec : float
        the total run duration in seconds
    steps : list
        a list of dicts, one per recipe step, keyed by "<parameter name> (<unit>)"
    numStepsDeclared : int
        the number of steps the recipe declares ("No. of steps = N")
    processSummary : dict
        maps step number -> {"set": float, "actual": float} process time in seconds
    channelNames : list
        the names of the endpoint-detector channels recorded during the run
    channelUnits : list
        the value unit for each channel
    channelTime : list
        a list of per-channel time lists (ms)
    channelData : list
        a list of per-channel value lists
    dataPath : str
        the path to the directory that contains the data for the machine
    waferLogFilePath : str
        the path to the file that contains the wafer log data for the machine
    waferLogDirPath : str
        the path to the directory that contains the wafer log data for the machine
    plotpath : str
        the path to the directory that contains the output plots for the machine
    textpath : str
        the path to the directory that contains the output text for the machine
    recipe : str
        the name of the recipe for the machine
    recipeIgnores : list
        a list of the names of the recipes to ignore for the machine
    dir_list : list
        a list of the file names in the directory for the machine
    outString : str
        the string that contains the output text for the machine

    Methods
    -------
    readFile():
        Reads through the historical wafer log file and parses run metadata, steps,
        channel history, and the process sequence summary
    genReport():
        Generates the report and saves it to the Output_Text directory
    plotWaferLog():
        Generates plots of the step timing and endpoint channel data and saves them
        to the Output_Plots directory
    initialize():
        Initializes the data stack with the most recent file
    sendData():
        Pops the most recent file from the stack and generates the full report
    sendDataRaw():
        Pops the most recent file from the stack and returns its path
    run():
        Runs the WaferLog algorithm
    runRaw():
        Runs the WaferLog algorithm in raw mode
    """

    def __init__(self, dataPath):
        """
        Constructor for the WaferLog class

            Parameters
            ----------
                dataPath : str
                    Path from Tool-Data to the data folder of the machine
        """
        super().__init__(dataPath)
        self.recipeIgnores = ["test", "lav test"]


    def readFile(self):
        """
        Reads through the historical wafer log txt file and parses run metadata, the
        step table, endpoint channel history, and the process sequence summary.

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        path = self.waferLogFilePath
        self.machineID = ""
        self.waferID = ""
        self.loggingSpec = ""
        self.recipe = ""
        self.startTime = ""
        self.endTime = ""
        self.durationSec = 0.0
        self.steps = []
        self.numStepsDeclared = 0
        self.processSummary = {}
        self.channelNames = []
        self.channelUnits = []
        self.channelTime = []
        self.channelData = []

        try:
            foobar = open(path)
            foobar.close()
        except FileNotFoundError:
            print("FILE NOT FOUND, PROCESS ABORTED AT: \"src/Machines/HDPCVD/WaferLog.py\" AT METHOD: readFile(). \n Hint: Try putting in a valid file path.")
            raise FileNotFoundError

        with open(path, "r", encoding="utf-8", errors="replace") as file:
            lines = file.readlines()

        if not lines:
            print("FILE IS EMPTY, PROCESS ABORTED AT: \"src/Machines/HDPCVD/WaferLog.py\" AT METHOD: readFile().")
            return

        self.parseHeader(lines)
        self.parseSteps(lines)
        self.parseHistoricalData(lines)
        self.parseProcessSummary(lines)


    def parseHeader(self, lines):
        """
        Helper method to parse the run metadata (machine/wafer/recipe IDs, logging spec,
        start/end time, duration, and declared step count) from the file's header lines.

            Parameters
            ----------
                lines: list
                    the lines of the wafer log file

            Returns
            -------
                None
        """
        for line in lines:
            stripped = line.strip()

            if stripped.startswith("Logging Specification Name:"):
                self.loggingSpec = stripped.split(":", 1)[1].strip()

            elif stripped.startswith("machineID:"):
                for field in line.rstrip("\n").split("\t"):
                    field = field.strip()
                    if field.startswith("machineID:"):
                        self.machineID = field.split(":", 1)[1].strip()
                    elif field.startswith("waferId:"):
                        self.waferID = field.split(":", 1)[1].strip()
                    elif field.startswith("Recipe:"):
                        self.recipe = field.split(":", 1)[1].strip()

            elif stripped.startswith("Start:"):
                m = re.search(r"Start:\(([^)]+)\)\((\d+)\)\s*End:\(([^)]+)\)\s*\((\d+)\)", stripped)
                if m:
                    self.startTime = m.group(1).strip()
                    self.endTime = m.group(3).strip()
                    self.durationSec = (int(m.group(4)) - int(m.group(2))) / 1000.0

            elif stripped.startswith("No. of steps"):
                m = re.search(r"=\s*(\d+)", stripped)
                if m:
                    self.numStepsDeclared = int(m.group(1))


    def parseSteps(self, lines):
        """
        Helper method to parse the recipe step table into a list of dicts, one per step,
        keyed by "<parameter name> (<unit>)".

            Parameters
            ----------
                lines: list
                    the lines of the wafer log file

            Returns
            -------
                None
        """
        headerIdx = None
        for i, line in enumerate(lines):
            if line.split("\t", 1)[0].strip() == "Step":
                headerIdx = i
                break
        if headerIdx is None or headerIdx + 1 >= len(lines):
            return

        headerFields = [h.strip() for h in lines[headerIdx].rstrip("\n").split("\t")]
        unitFields = [u.strip() for u in lines[headerIdx + 1].rstrip("\n").split("\t")]

        colnames = []
        seen = {}
        for h, u in zip(headerFields, unitFields):
            if h == "Step":
                col = "Step"
            elif u in ("", "()", "(none)", "(Units)"):
                col = h
            else:
                col = f"{h} {u}"
            if col in seen:
                seen[col] += 1
                col = f"{col} #{seen[col]}"
            else:
                seen[col] = 1
            colnames.append(col)

        i = headerIdx + 2
        while i < len(lines):
            raw = lines[i].rstrip("\n")
            if raw.strip() == "":
                i += 1
                continue
            if raw.strip().startswith("HistoricalData:"):
                break
            values = raw.split("\t")
            stepDict = {}
            for name, val in zip(colnames, values):
                stepDict[name] = val.strip()
            self.steps.append(stepDict)
            i += 1


    def parseHistoricalData(self, lines):
        """
        Helper method to parse the endpoint-detector channel history into per-channel
        time (ms) and value lists. Samples marked "nil" or "---" (no reading) are skipped.

            Parameters
            ----------
                lines: list
                    the lines of the wafer log file

            Returns
            -------
                None
        """
        hdIdx = None
        for i, line in enumerate(lines):
            if line.strip().startswith("HistoricalData:"):
                hdIdx = i
                break
        if hdIdx is None or hdIdx + 2 >= len(lines):
            return

        nameFields = lines[hdIdx + 1].rstrip("\n").split("\t")
        unitFields = lines[hdIdx + 2].rstrip("\n").split("\t")
        numChannels = min(len(nameFields), len(unitFields)) // 2
        if numChannels <= 0:
            return

        self.channelNames = [nameFields[2 * c].strip() for c in range(numChannels)]
        self.channelUnits = [unitFields[2 * c + 1].strip() for c in range(numChannels)]
        self.channelTime = [[] for _ in range(numChannels)]
        self.channelData = [[] for _ in range(numChannels)]

        i = hdIdx + 3
        while i < len(lines):
            raw = lines[i].rstrip("\n")
            if raw.strip() == "":
                i += 1
                continue
            if raw.strip().startswith("Process sequence summary"):
                break
            values = raw.split("\t")
            for c in range(numChannels):
                tcol, vcol = 2 * c, 2 * c + 1
                if vcol >= len(values):
                    continue
                traw, vraw = values[tcol].strip(), values[vcol].strip()
                if traw in ("", "---") or vraw in ("", "---", "nil"):
                    continue
                try:
                    t, v = float(traw), float(vraw)
                except ValueError:
                    continue
                self.channelTime[c].append(t)
                self.channelData[c].append(v)
            i += 1


    def parseProcessSummary(self, lines):
        """
        Helper method to parse the trailing process sequence summary (set vs. actual
        process time per step) into the processSummary dict.

            Parameters
            ----------
                lines: list
                    the lines of the wafer log file

            Returns
            -------
                None
        """
        psIdx = None
        for i, line in enumerate(lines):
            if line.strip().startswith("Process sequence summary"):
                psIdx = i
                break
        if psIdx is None:
            return

        for line in lines[psIdx + 1:]:
            raw = line.rstrip("\n")
            if raw.strip() == "":
                continue
            parts = raw.split("\t")
            if len(parts) < 4:
                continue
            tag, value, stepnum = parts[0].strip(), parts[2].strip(), parts[3].strip()
            try:
                stepnumInt, valueFloat = int(stepnum), float(value)
            except ValueError:
                continue
            entry = self.processSummary.setdefault(stepnumInt, {})
            if tag == "SET_TIME":
                entry["set"] = valueFloat
            elif tag == "PROC_TIME":
                entry["actual"] = valueFloat


    def genReport(self):
        """
        Generates a report of the wafer log data into an output text file.

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        self.outString = "----------------------------------------------\n\nWAFER LOG REPORT AT " + datetime.now().strftime("%H:%M:%S") + " ON " + datetime.now().strftime("%m/%d/%Y") + "\n\n----------------------------------------------\n\n"
        self.readFile()

        self.outString += "Recipe: " + self.recipe + "\n"
        self.outString += "Wafer ID: " + self.waferID + "\n"
        self.outString += "Machine ID: " + self.machineID + "\n"
        if self.loggingSpec:
            self.outString += "Logging Specification: " + self.loggingSpec + "\n"
        self.outString += "\n"
        self.outString += "Start: " + self.startTime + "\n"
        self.outString += "End: " + self.endTime + "\n"
        self.outString += "Duration: " + f"{self.durationSec:.1f}" + " sec\n\n"
        self.outString += f"Completed Steps: {len(self.processSummary)}/{self.numStepsDeclared}\n\n----------------------------------------------\n\n"

        gasKeys = ["Ar", "CH4", "N2a", "N2b", "N2c", "N2d", "O2", "SF6", "SiH4"]
        for step in self.steps:
            try:
                stepnum = int(step.get("Step", "").strip())
            except ValueError:
                continue

            name = next((v for k, v in step.items() if k.startswith("name")), "")
            pressure = next((v for k, v in step.items() if k.startswith("Pressure")), "")
            summary = self.processSummary.get(stepnum, {})

            self.outString += f"Step {stepnum}: {name}\n"
            self.outString += "  Process Time: Set = " + str(summary.get("set", "N/A")) + " s, Actual = " + str(summary.get("actual", "N/A")) + " s\n"
            if pressure:
                self.outString += f"  Pressure: {pressure} mTorr\n"

            flows = []
            for key, val in step.items():
                if any(key.startswith(gas + " ") for gas in gasKeys):
                    try:
                        if float(val) != 0.0:
                            flows.append(f"{key.split(' ')[0]} = {val}")
                    except ValueError:
                        pass
            if flows:
                self.outString += "  Gas Flows (sccm): " + ", ".join(flows) + "\n"

            rf = []
            for key, val in step.items():
                if key.startswith("RFICPGeneratorP") or (key.startswith("RFBiasGenerator") and "(W)" in key):
                    try:
                        if float(val) != 0.0:
                            rf.append(f"{key} = {val}")
                    except ValueError:
                        pass
            if rf:
                self.outString += "  RF Power: " + ", ".join(rf) + "\n"

            self.outString += "\n"

        self.outString += "----------------------------------------------\n\n"
        hasData = any(len(v) > 0 for v in self.channelData)
        if hasData:
            for idx, name in enumerate(self.channelNames):
                if len(self.channelData[idx]) == 0:
                    continue
                unit = self.channelUnits[idx]
                avg = sum(self.channelData[idx]) / len(self.channelData[idx])
                self.outString += f"Channel '{name}': {len(self.channelData[idx])} samples, avg = {avg:.3f} {unit}\n"
        else:
            self.outString += "No numeric endpoint channel data recorded for this run.\n"

        file_path = os.path.join(self.textpath, "WaferLog Report.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(self.outString)


    def plotWaferLog(self):
        """
        Plots the step process time (set vs. actual) and endpoint channel data and
        saves them to the Output_Plots directory.

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        step_path = os.path.join(self.plotpath, "Step Process Time.png")
        channel_path = os.path.join(self.plotpath, "Endpoint Channel Data.png")
        for p in (step_path, channel_path):
            try:
                os.remove(p)
            except FileNotFoundError:
                pass

        # Plotting the Step Set vs Actual Process Time
        stepNums = sorted(self.processSummary.keys())
        if stepNums:
            setTimes = [self.processSummary[s].get("set", 0.0) for s in stepNums]
            actualTimes = [self.processSummary[s].get("actual", 0.0) for s in stepNums]

            fig, ax = plt.subplots()
            fig.suptitle('Step Process Time (Set vs. Actual)')
            fig.set_size_inches(8, 5)
            x = list(range(len(stepNums)))
            width = 0.35
            ax.bar([i - width / 2 for i in x], setTimes, width, label='Set', color='tab:blue')
            ax.bar([i + width / 2 for i in x], actualTimes, width, label='Actual', color='tab:orange')
            ax.set_xticks(x)
            ax.set_xticklabels([str(s) for s in stepNums])
            ax.set_xlabel('Step')
            ax.set_ylabel('Time (s)')
            ax.legend()
            fig.tight_layout()
            fig.savefig(step_path)
        else:
            fig = plt.figure()
            fig.suptitle('Step Process Time (Set vs. Actual)')
            fig.set_size_inches(8, 5)
            fig.tight_layout()
            fig.savefig(step_path)
            print("GRAPHING ABORTED AT: \"src/Machines/HDPCVD/WaferLog.py\" AT METHOD: plotWaferLog(), No Process Sequence Data")

        # Plotting the Endpoint Channel Data
        hasData = any(len(v) > 0 for v in self.channelData)
        if hasData:
            n = len(self.channelNames)
            fig, axs = plt.subplots(n, 1, squeeze=False)
            fig.suptitle('Endpoint Channel Data')
            fig.supxlabel('Time (ms)')
            fig.set_size_inches(8, 4 * n)
            for i, name in enumerate(self.channelNames):
                axs[i, 0].plot(self.channelTime[i], self.channelData[i])
                axs[i, 0].set_title(name)
                axs[i, 0].set_ylabel(self.channelUnits[i] if i < len(self.channelUnits) else "")
            fig.tight_layout()
            fig.savefig(channel_path)
        else:
            fig = plt.figure()
            fig.suptitle('Endpoint Channel Data')
            fig.set_size_inches(8, 4)
            fig.tight_layout()
            fig.savefig(channel_path)
            print("GRAPHING ABORTED AT: \"src/Machines/HDPCVD/WaferLog.py\" AT METHOD: plotWaferLog(), No Numeric Channel Data")


    def sendData(self):
        """
        Pops the most recent file from the stack and generates the full report.

            Parameters
            ----------
                None

            Returns
            -------
                recipe (str): the name of the recipe for the machine
        """
        stack = []
        process_path = os.path.join(self.dataPath, "process_stack.txt")
        with open(process_path, "r") as file:
            stack = file.read().splitlines()
        if self.ignoreRecipe():
            return False
        elif stack.__len__() == 0:
            with open(process_path, "a+") as file:
                file.write(self.waferLogFilePath + "\n")
        elif stack.count(self.waferLogFilePath) > 0:
            return False
        else:
            with open(process_path, "a+") as file:
                file.write(self.waferLogFilePath + "\n")

        self.genReport()
        self.plotWaferLog()
        print("Sent data for:", self.waferLogFilePath)
        return self.recipe


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
        stack = []
        process_path = os.path.join(self.dataPath, "process_stack.txt")
        with open(process_path, "r") as file:
            stack = file.read().splitlines()
        if self.ignoreRecipe():
            return None
        elif stack.__len__() == 0:
            with open(process_path, "a+") as file:
                file.write(self.waferLogFilePath + "\n")
        elif stack.count(self.waferLogFilePath) > 0:
            return None
        else:
            with open(process_path, "a+") as file:
                file.write(self.waferLogFilePath + "\n")

        print("Sent data for:", self.waferLogFilePath)
        return self.waferLogFilePath


# Main function to test the WaferLog class
def main():
    waferlog = WaferLog(os.path.join("src", "Machines", "HDPCVD", "data"))
    waferlog.initialize()
    waferlog.sendData()


if __name__ == "__main__":
    main()
