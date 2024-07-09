from src.Machines.Savannah.Pressure import Pressure
from src.Machines.Savannah.Heating import Heating
from src.uploader import Uploader

from datetime import datetime

class Savannah:
    def __init__(self):
        pass


    def run(self):
        # RUN ALGS
        p = Pressure()
        h = Heating()
        p.run()
        h.run()
        # ADD DATE TIME TO NEW DIRECTORY NAME
        dirname = datetime.now().strftime("%m:%d:%Y") + "~" + datetime.now().strftime("%H:%M")
        # FIND ROOT DIRECTORY OF CLOUD STORAGE
        file = open("src/rclone.txt", "r")
        root = file.readline().strip()
        # UPLOAD TO CLOUD STORAGE
        up = Uploader("src/Machines/Savannah/data/Output_Text", f"{root}/Savannah/{dirname}")
        up.rclone()
        up2 = Uploader("src/Machines/Savannah/data/Output_Plots", f"{root}/Savannah/{dirname}")
        up2.rclone()


def main():
    s = Savannah()
    s.run()


if __name__ == "__main__":
    main()
