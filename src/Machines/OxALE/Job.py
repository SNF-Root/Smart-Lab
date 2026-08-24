import matplotlib.pyplot as plt
import json
import os
from datetime import datetime
from src.Machines.BaseClasses.Job_Base import Job_Base


class Job(Job_Base):
    """
    A class to represent the Job algorithm for the Ox-ALE (Oxford Instruments Cobra ALE)
    Machine.

    Unlike the file-per-run tools in this project, the Cobra's PTIQ control software keeps
    its process history in a set of SQLite databases (PTIQ/Databases on the tool PC). This
    class reads the most recently completed job from Jobs.db: the job/lot info, the wafers
    it moved, the recipe's process steps, and (for ALE recipes) the per-cycle phase timeline
    for each step (RecipePhaseEntries.StepID references RecipeStepEntries.ID).

    Attributes
    ----------
    taskID : str
        the GUID of the most recently completed job
    recipe : str
        the name of the recipe for the job
    lotID : str
        the lot identifier for the job
    status : str
        the final status of the job (e.g. "Finished", "Aborted")
    startTime : str
        the job start timestamp as stored in Jobs.db
    endTime : str
        the job end timestamp as stored in Jobs.db
    durationSec : float
        the total job duration in seconds
    wafers : list
        a list of dicts describing each wafer processed by the job, including its transfers
    steps : list
        a list of dicts describing each recipe step run during the job's process action
    phases : list
        a list of dicts describing each recipe phase (ALE cycle sub-step) run within a step
    dataPath : str
        the path to the directory that contains the data for the machine
    dbPath : str
        the path to the Jobs.db database for the machine
    plotpath : str
        the path to the directory that contains the output plots for the machine
    textpath : str
        the path to the directory that contains the output text for the machine
    recipeIgnores : list
        a list of recipe name substrings to ignore for the machine
    outString : str
        the string that contains the output text for the machine

    Methods
    -------
    readJob():
        Reads the most recently completed job's info, wafers, steps, and phases from Jobs.db
    genReport():
        Generates the report and saves it to the Output_Text directory
    plotJob():
        Generates plots of the step timeline and phase duration trend and saves them to the
        Output_Plots directory
    initialize():
        Initializes the job stack with the most recently completed job
    sendData():
        Generates the full report for the most recently completed job
    sendDataRaw():
        Exports the most recently completed job's data to a JSON file and returns its path
    run():
        Runs the Job algorithm
    runRaw():
        Runs the Job algorithm in raw mode
    """

    def __init__(self, dataPath):
        """
        Constructor for the Job class

            Parameters
            ----------
                dataPath : str
                    Path from Tool-Data to the data folder of the machine
        """
        super().__init__(dataPath)
        self.recipeIgnores = ["manual recipe run", "chamber clean"]


    def parseDatetime(self, value):
        """
        Helper method to parse a Jobs.db datetime string (ISO-like, with a variable-precision
        fractional-second component and an optional trailing "Z") into a datetime object.

            Parameters
            ----------
                value: str
                    the datetime string to parse

            Returns
            -------
                datetime: the parsed datetime, or None if value is empty/unparseable
        """
        if not value:
            return None
        v = value.strip()
        if v.endswith("Z"):
            v = v[:-1]
        if "." in v:
            base, frac = v.split(".", 1)
            frac = (frac + "000000")[:6]
            v = f"{base}.{frac}"
            fmt = "%Y-%m-%d %H:%M:%S.%f"
        else:
            fmt = "%Y-%m-%d %H:%M:%S"
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            return None


    def computeDurationSec(self, start, end):
        """
        Helper method to compute the number of seconds between two Jobs.db datetime strings.

            Parameters
            ----------
                start: str
                    the start datetime string
                end: str
                    the end datetime string

            Returns
            -------
                float: the duration in seconds, or None if either value is unparseable
        """
        s = self.parseDatetime(start)
        e = self.parseDatetime(end)
        if s is None or e is None:
            return None
        return (e - s).total_seconds()


    def readJob(self):
        """
        Reads the most recently completed job's info, wafers, recipe steps, and recipe
        phases from Jobs.db.

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        self.recipe = ""
        self.lotID = ""
        self.status = ""
        self.startTime = ""
        self.endTime = ""
        self.durationSec = None
        self.wafers = []
        self.steps = []
        self.phases = []

        if not self.taskID:
            print("NO JOB SELECTED, PROCESS ABORTED AT: \"src/Machines/OxALE/Job.py\" AT METHOD: readJob(). \n Hint: Try running initialize() first.")
            return

        taskBytes = self.guidToBytes(self.taskID)

        con = self.openConnection()
        try:
            cur = con.cursor()
            cur.execute("SELECT LotID, StartDate, EndDate, Status, Recipe FROM Jobs WHERE TaskID = ?;", (taskBytes,))
            row = cur.fetchone()
            if row is None:
                print(f"JOB NOT FOUND, PROCESS ABORTED AT: \"src/Machines/OxALE/Job.py\" AT METHOD: readJob(). \n Hint: TaskID {self.taskID} was not found in Jobs.db.")
                return
            self.lotID, self.startTime, self.endTime, self.status, self.recipe = row
            self.durationSec = self.computeDurationSec(self.startTime, self.endTime)

            cur.execute("SELECT WaferID, Name, SourceLocation, SourceSlot, DestinationLocation, DestinationSlot, Status FROM Wafers WHERE TaskID = ?;", (taskBytes,))
            waferRows = cur.fetchall()

            for waferID, name, srcLoc, srcSlot, dstLoc, dstSlot, wStatus in waferRows:
                waferEntry = {
                    "waferID": self.guidToStr(waferID),
                    "name": name,
                    "source": f"{srcLoc} slot {srcSlot}" if srcLoc else "",
                    "destination": f"{dstLoc} slot {dstSlot}" if dstLoc else "",
                    "status": wStatus,
                    "transfers": [],
                }

                cur.execute("SELECT ActionID, ActionType, Source, Destination, Result FROM WaferActions WHERE WaferID = ? ORDER BY ID;", (waferID,))
                actionRows = cur.fetchall()

                for actionID, actionType, src, dst, result in actionRows:
                    if actionType == "Process":
                        cur.execute("SELECT ID, StepID, StartTime, EndTime, Name, ModuleID FROM RecipeStepEntries WHERE ActionID = ? ORDER BY StepID;", (actionID,))
                        stepRows = cur.fetchall()
                        for rowID, stepIdx, sStart, sEnd, sName, moduleID in stepRows:
                            self.steps.append({
                                "stepIndex": stepIdx,
                                "name": sName,
                                "startTime": sStart,
                                "endTime": sEnd,
                                "durationSec": self.computeDurationSec(sStart, sEnd),
                                "moduleID": moduleID,
                            })

                            cur.execute("SELECT PhaseID, StartTime, EndTime, Name FROM RecipePhaseEntries WHERE StepID = ? ORDER BY PhaseID, StartTime;", (rowID,))
                            for phaseID, pStart, pEnd, pName in cur.fetchall():
                                self.phases.append({
                                    "stepIndex": stepIdx,
                                    "phaseID": phaseID,
                                    "name": pName,
                                    "startTime": pStart,
                                    "endTime": pEnd,
                                    "durationSec": self.computeDurationSec(pStart, pEnd),
                                })
                    else:
                        waferEntry["transfers"].append({
                            "type": actionType,
                            "source": src,
                            "destination": dst,
                            "result": result,
                        })

                self.wafers.append(waferEntry)
        finally:
            con.close()


    def genReport(self):
        """
        Generates a report of the job data into an output text file.

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        self.outString = "----------------------------------------------\n\nJOB REPORT AT " + datetime.now().strftime("%H:%M:%S") + " ON " + datetime.now().strftime("%m/%d/%Y") + "\n\n----------------------------------------------\n\n"
        self.readJob()

        self.outString += "Recipe: " + (self.recipe or "") + "\n"
        self.outString += "Lot ID: " + (self.lotID or "") + "\n"
        self.outString += "Status: " + (self.status or "") + "\n\n"
        self.outString += "Start: " + (self.startTime or "") + "\n"
        self.outString += "End: " + (self.endTime or "") + "\n"
        if self.durationSec is not None:
            self.outString += f"Duration: {self.durationSec:.1f} sec\n\n"
        else:
            self.outString += "Duration: N/A\n\n"
        self.outString += "----------------------------------------------\n\n"

        for wafer in self.wafers:
            self.outString += f"Wafer: {wafer['name']} (ID {wafer['waferID']})\n"
            self.outString += f"  Source: {wafer['source']}  Destination: {wafer['destination']}  Status: {wafer['status']}\n"
            for t in wafer["transfers"]:
                self.outString += f"  Transfer [{t['type']}]: {t['source']} -> {t['destination']} : {t['result']}\n"
            self.outString += "\n"

        if self.steps:
            self.outString += "Process Steps:\n\n"
            for step in self.steps:
                self.outString += f"  Step {step['stepIndex']}: {step['name']}"
                if step["durationSec"] is not None:
                    self.outString += f" ({step['durationSec']:.1f} sec)"
                self.outString += "\n"

                stepPhases = [p for p in self.phases if p["stepIndex"] == step["stepIndex"]]
                if stepPhases:
                    byName = {}
                    for p in stepPhases:
                        if p["durationSec"] is None:
                            continue
                        byName.setdefault(p["name"], []).append(p["durationSec"])
                    for name, durs in byName.items():
                        self.outString += f"    {name}: {len(durs)}x, avg = {sum(durs) / len(durs):.3f} sec, min = {min(durs):.3f} sec, max = {max(durs):.3f} sec\n"
                self.outString += "\n"
        else:
            self.outString += "No recipe step data recorded for this job.\n"

        file_path = os.path.join(self.textpath, "Job Report.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(self.outString)


    def plotJob(self):
        """
        Plots the step timeline and the per-phase duration trend for the busiest step and
        saves them to the Output_Plots directory.

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        step_path = os.path.join(self.plotpath, "Step Timeline.png")
        phase_path = os.path.join(self.plotpath, "Phase Duration Trend.png")
        for p in (step_path, phase_path):
            try:
                os.remove(p)
            except FileNotFoundError:
                pass

        # Plotting the Step Timeline
        jobStart = self.parseDatetime(self.startTime)
        if self.steps and jobStart is not None:
            fig, ax = plt.subplots()
            fig.suptitle('Step Timeline')
            fig.set_size_inches(8, max(2, 0.6 * len(self.steps)))
            colors = plt.get_cmap('tab10').colors
            for i, step in enumerate(self.steps):
                s = self.parseDatetime(step["startTime"])
                dur = step["durationSec"]
                if s is None or dur is None:
                    continue
                offset = (s - jobStart).total_seconds()
                ax.barh(i, dur, left=offset, color=colors[i % len(colors)])
                ax.text(offset, i, f" {step['name']}", va='center', fontsize=8)
            ax.set_yticks(range(len(self.steps)))
            ax.set_yticklabels([f"Step {s['stepIndex']}" for s in self.steps])
            ax.invert_yaxis()
            ax.set_xlabel('Time Since Job Start (s)')
            fig.tight_layout()
            fig.savefig(step_path)
        else:
            fig = plt.figure()
            fig.suptitle('Step Timeline')
            fig.set_size_inches(8, 4)
            fig.tight_layout()
            fig.savefig(step_path)
            print("GRAPHING ABORTED AT: \"src/Machines/OxALE/Job.py\" AT METHOD: plotJob(), No Step Data")

        # Plotting the Phase Duration Trend for the step with the most phases
        if self.phases:
            stepCounts = {}
            for p in self.phases:
                stepCounts[p["stepIndex"]] = stepCounts.get(p["stepIndex"], 0) + 1
            busiestStep = max(stepCounts, key=stepCounts.get)
            relevant = [p for p in self.phases if p["stepIndex"] == busiestStep and p["durationSec"] is not None]

            byName = {}
            for p in relevant:
                byName.setdefault(p["name"], []).append(p["durationSec"])

            fig, ax = plt.subplots()
            fig.suptitle(f'Phase Duration Trend (Step {busiestStep})')
            fig.set_size_inches(8, 5)
            for name, durs in byName.items():
                ax.plot(range(len(durs)), durs, marker='o', markersize=2, linestyle='-', label=name)
            ax.set_xlabel('Occurrence Index (per phase name)')
            ax.set_ylabel('Duration (s)')
            ax.legend(fontsize=8)
            fig.tight_layout()
            fig.savefig(phase_path)
        else:
            fig = plt.figure()
            fig.suptitle('Phase Duration Trend')
            fig.set_size_inches(8, 5)
            fig.tight_layout()
            fig.savefig(phase_path)
            print("GRAPHING ABORTED AT: \"src/Machines/OxALE/Job.py\" AT METHOD: plotJob(), No Phase Data")


    def sendData(self):
        """
        Generates the full report for the most recently completed job if it is new.

            Parameters
            ----------
                None

            Returns
            -------
                recipe (str): the name of the recipe for the job, or False if there is no new data
        """
        if not self.taskID:
            return False

        stack = []
        process_path = os.path.join(self.dataPath, "process_stack.txt")
        with open(process_path, "r") as file:
            stack = file.read().splitlines()

        self.readJob()
        if self.ignoreRecipe():
            return False
        elif stack.__len__() == 0:
            with open(process_path, "a+") as file:
                file.write(self.taskID + "\n")
        elif stack.count(self.taskID) > 0:
            return False
        else:
            with open(process_path, "a+") as file:
                file.write(self.taskID + "\n")

        self.genReport()
        self.plotJob()
        print("Sent data for job:", self.taskID)
        return self.recipe


    def sendDataRaw(self):
        """
        Exports the most recently completed job's data (job info, wafers, steps, phases)
        to a JSON file if it is new. Returns the file path.

            Parameters
            ----------
                None

            Returns
            -------
                str: the file path of the new raw data export, or None if there is no new data
        """
        if not self.taskID:
            return None

        stack = []
        process_path = os.path.join(self.dataPath, "process_stack.txt")
        with open(process_path, "r") as file:
            stack = file.read().splitlines()

        self.readJob()
        if self.ignoreRecipe():
            return None
        elif stack.__len__() == 0:
            with open(process_path, "a+") as file:
                file.write(self.taskID + "\n")
        elif stack.count(self.taskID) > 0:
            return None
        else:
            with open(process_path, "a+") as file:
                file.write(self.taskID + "\n")

        export = {
            "taskID": self.taskID,
            "recipe": self.recipe,
            "lotID": self.lotID,
            "status": self.status,
            "startTime": self.startTime,
            "endTime": self.endTime,
            "durationSec": self.durationSec,
            "wafers": self.wafers,
            "steps": self.steps,
            "phases": self.phases,
        }

        safeID = self.taskID.replace("-", "")
        export_path = os.path.join(self.dataPath, f"Job_{safeID}.json")
        with open(export_path, "w", encoding="utf-8") as file:
            json.dump(export, file, indent=2)

        print("Sent data for job:", self.taskID)
        return export_path


# Main function to test the Job class
def main():
    job = Job(os.path.join("src", "Machines", "OxALE", "data"))
    job.initialize()
    job.sendData()


if __name__ == "__main__":
    main()
