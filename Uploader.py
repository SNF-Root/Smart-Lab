import os
import shutil
import glob
from datetime import datetime

from Pressure import Pressure
from Heating import Heating

import time

dir_path = "/Users/andrew/Library/CloudStorage/GoogleDrive-ajchang@ucsb.edu/My Drive/SNF Data/Savannah Data"
newdir= ""
currFile = "foobar"

def upload():
    newdir = dir_path + "/" + datetime.now().strftime("%H;%M;%S") + " | " + datetime.now().strftime("%m:%d:%Y")
    os.makedirs(newdir, exist_ok=True)
    shutil.copy("/Users/andrew/Desktop/SNF Projects/Tool-Data/Output_Plots/Precursor Heating Data.png", newdir)
    shutil.copy("/Users/andrew/Desktop/SNF Projects/Tool-Data/Output_Plots/PressureData.png", newdir)
    shutil.copy("/Users/andrew/Desktop/SNF Projects/Tool-Data/Output_Plots/Non-Precursor Heating Data.png", newdir)
    print("Upload Complete")


def loop():
    global currFile
    while True:
        time.sleep(2)
        list_of_files = glob.glob("/Users/andrew/Desktop/SNF Projects/Tool-Data/Heating-Data/*")
        latest_file = max(list_of_files, key=os.path.getctime)

        if (currFile == None) or (latest_file != currFile):
            currFile = latest_file
            print("New File Detected")
            upload()


def main():
    loop()
    # time.sleep(20)
    # os.remove(newdir)
    

if __name__ == "__main__":
    main()