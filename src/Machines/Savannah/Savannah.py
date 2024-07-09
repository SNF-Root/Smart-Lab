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
        print(dirname)
        up = Uploader("src/Machines/Savannah/data/Output_Text", f"SNF-Root-Test:Home/Savannah/{dirname}")
        up.rclone()
        up2 = Uploader("src/Machines/Savannah/data/Output_Plots", f"SNF-Root-Test:Home/Savannah/{dirname}")
        up2.rclone()


def main():
    s = Savannah()
    s.run()


if __name__ == "__main__":
    main()
