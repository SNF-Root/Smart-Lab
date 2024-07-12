from src.Machines.Savannah.Pressure import Pressure
from src.Machines.Savannah.Heating import Heating
from src.uploader import Uploader

from datetime import datetime
import timeit

# Iterates through all Savannah Machines and runs all algorithms
class Savannah:
    # Constructor
    def __init__(self):
        pass


    # Runs the Pressure and Heating algorithms for all Savannah machines
    def run(self):
        # RUN ALGS
        start = timeit.default_timer()
        file = open("src/register.txt", "r")
        runMachine = []
        for line in file:
            m = tuple(line.strip().split())
            if m[0] == "Savannah":
                runMachine.append(m)
        file.close()
        for machine in runMachine:
            dataPath = f"src/Machines/{machine[0]}/data({machine[1]})"
            p = Pressure(dataPath)
            h = Heating(dataPath)
            newp = p.run()
            newh = h.run()
            stop = timeit.default_timer()
            print('Data Processing Runtime: ', stop - start)
            if newp or newh:
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


# Main function for testing
def main():
    s = Savannah()
    s.run()


if __name__ == "__main__":
    main()
