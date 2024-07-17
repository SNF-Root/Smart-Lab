from src.Machines.Fiji202.Pressure import Pressure
from src.Machines.Fiji202.Heating import Heating
from src.Machines.Fiji202.Plasma import Plasma
from src.uploader import Uploader

from datetime import datetime
import timeit
import os

# Iterates through all Fiji202 Machines and runs all algorithms
class Fiji202:
    # Constructor
    def __init__(self):
        pass

    
    # Changes the name of a file
    # specifically for renaming raw files
    def changeName(self, filepath, append):
        # RENAME FILE
        # CHANGE FILE PATH TO LINUX FORMAT
        filepath = filepath.replace("\\", "/")
        filename = filepath.split("/")
        name = filename[-1]
        newpath = filepath.replace(name, f"({append}) {name}")
        # CHANGE FILE NAME
        try:
            os.rename(filepath, newpath)
        except:
            print("Error: File not found, Rename failed")
            return
        return newpath


    # Runs the Pressure, Heating, and Plasma algorithms for all Fiji202 machines
    def run(self):
        # RUN ALGS
        start = timeit.default_timer()
        file = open("src/register.txt", "r")
        runMachine = []
        raw = []
        for line in file:
            m = tuple(line.strip().split())
            if m[0] == "Fiji202":
                runMachine.append(m)
                if m[4] == "raw":
                    raw.append(True)
                else:
                    raw.append(False)
        file.close()
        # Raw file handling
        for machine in runMachine:
            dataPath = f"src/Machines/{machine[0]}/data({machine[1]})"
            p = Pressure(dataPath)
            h = Heating(dataPath)
            pl = Plasma(dataPath)
            # Uploading raw files
            if raw[runMachine.index(machine)]:
                newp = p.runRaw()
                newh = h.runRaw()
                newpl = p.runRaw()
                # If new raw files are found, change their names and upload them
                if newp and newh and newpl:
                    newp = self.changeName(newp, "Pressure")
                    newh = self.changeName(newh, "Heating")
                    newpl = self.changeName(newpl, "Plasma")
                    dirname = datetime.now().strftime("%m:%d:%Y") + "~" + datetime.now().strftime("%H:%M")
                    file = open("src/rclone.txt", "r")
                    root = file.readline().strip()
                    file.close()
                    up = Uploader(newp, f"{root}/{machine[0]}/{machine[1]}/{dirname}")
                    up.rclone()
                    print("Uploaded Pressure")
                    up2 = Uploader(newh, f"{root}/{machine[0]}/{machine[1]}/{dirname}")
                    up2.rclone()
                    print("Uploaded Heating")
                    up3 = Uploader(newpl, f"{root}/{machine[0]}/{machine[1]}/{dirname}")
                    up3.rclone()
                    print("Uploaded Plasma")
            # Uploading normal output files
            else:
                newp = p.run()
                newh = h.run()
                newpl = pl.run()
                stop = timeit.default_timer()
                print('Data Processing Runtime: ', stop - start)
                if newp and newh and newpl:
                    # ADD DATE TIME TO NEW DIRECTORY NAME
                    dirname = datetime.now().strftime("%m:%d:%Y") + "~" + datetime.now().strftime("%H:%M")
                    # FIND ROOT DIRECTORY OF CLOUD STORAGE
                    file = open("src/rclone.txt", "r")
                    root = file.readline().strip()
                    file.close()
                    # UPLOAD TO CLOUD STORAGE
                    up = Uploader(f"src/Machines/{machine[0]}/data({machine[1]})/Output_Text", f"{root}/{machine[0]}/{machine[1]}/{dirname}")
                    up.rclone()
                    up2 = Uploader(f"src/Machines/{machine[0]}/data({machine[1]})/Output_Plots", f"{root}/{machine[0]}/{machine[1]}/{dirname}")
                    up2.rclone()
                    up3 = Uploader(f"src/Machines/{machine[0]}/data({machine[1]})/Output_Text", f"{root}/{machine[0]}/{machine[1]}/{dirname}")


# Main function for testing
def main():
    f = Fiji202()
    f.run()


if __name__ == "__main__":
    main()
