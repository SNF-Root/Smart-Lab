from src.Machines.Savannah.Pressure import Pressure
from src.Machines.Savannah.Heating import Heating
from src.uploader import Uploader


class Savannah:
    def __init__(self):
        pass


    def run():
        # RUN ALGS
        p = Pressure()
        h = Heating()
        p.run()
        h.run()
        # ADD DATE TIME TO NEW DIRECTORY NAME
        up = Uploader("src/Machines/Savannah/data/Output_Text", "SNF-Root-Test:Home/Savannah/Something Something Date Time...")
        up.rclone()
        up2 = Uploader("src/Machines/Savannah/data/Output_Plots", "SNF-Root-Test:Home/Savannah/Same name as above...")
        up2.rclone()


def main():
    s = Savannah()
    s.run()


if __name__ == "__main__":
    main()
